param([Parameter(Mandatory=$true)][string]$GodotExecutable, [switch]$OfflineRestore)
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$GodotExecutable = (Resolve-Path $GodotExecutable).Path
$env:GODOT_NUPKGS = Join-Path (Split-Path $GodotExecutable -Parent) 'GodotSharp/Tools/nupkgs'
$env:DOTNET_CLI_HOME = Join-Path $repoRoot 'reconstructed/.dotnet'
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
$env:DOTNET_GENERATE_ASPNET_CERTIFICATE = 'false'
$env:DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE = '1'
$env:MSBuildEnableWorkloadResolver = 'false'
# R003-C01: serialize the SDK's exporter child process as well as direct builds.
# Godot's default Publish failed silently at GetTargetFrameworks on this host.
$env:DOTNET_PROCESSOR_COUNT = '1'
# Explicit offline build option: packages must already exist locally. This only
# skips the unreachable online advisory lookup; no test or compiler gate changes.
if ($OfflineRestore) { $env:NuGetAudit = 'false' }
$toolsDir = Join-Path $repoRoot 'reconstructed/out/r002-tools'
$exportDir = Join-Path $repoRoot 'reconstructed/out/r004-windows'
function Invoke-Dotnet {
    param([string[]]$Arguments)
    & dotnet @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'dotnet command failed' }
}
function Invoke-Godot {
    param([string[]]$Arguments)
    $lines = & $GodotExecutable @Arguments 2>&1
    $code = $LASTEXITCODE
    $lines | ForEach-Object { Write-Host $_ }
    # Godot's first failed .NET export returned0 with ERROR lines: inspect both.
    if ($code -ne 0 -or ($lines -match '^ERROR:')) { throw 'Godot reported an execution/export error' }
}
$version = (& $GodotExecutable --version | Out-String).Trim()
if ($version -notlike '4.7.2.stable.mono.*') { throw ('Required Godot4.7.2 .NET; actual '+$version) }
New-Item -ItemType Directory -Force -Path $toolsDir,$exportDir | Out-Null
$archive = Join-Path $toolsDir 'templates.tpz'
if (-not (Test-Path -LiteralPath $archive)) {
    & curl.exe -L --fail --output $archive 'https://downloads.godotengine.org/?flavor=stable&platform=templates&slug=mono_export_templates.tpz&version=4.7.2'
    if ($LASTEXITCODE -ne 0) { throw 'Export-template download failed' }
}
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [IO.Compression.ZipFile]::OpenRead($archive)
try {
    $reader = New-Object IO.StreamReader($zip.GetEntry('templates/version.txt').Open())
    try { $templateVersion = $reader.ReadToEnd().Trim() } finally { $reader.Dispose() }
    if ($templateVersion -ne '4.7.2.stable.mono') { throw 'Wrong .NET export-template version' }
    foreach ($name in @('windows_debug_x86_64.exe','windows_debug_x86_64_console.exe','windows_release_x86_64.exe','windows_release_x86_64_console.exe')) {
        [IO.Compression.ZipFileExtensions]::ExtractToFile($zip.GetEntry('templates/'+$name),(Join-Path $toolsDir $name),$true)
    }
} finally { $zip.Dispose() }
Push-Location $repoRoot
try {
    Invoke-Dotnet -Arguments @('restore','reconstructed/godot/Arconist.Godot.csproj','--configfile','reconstructed/godot/NuGet.Config','-m:1','-nr:false')
    Invoke-Dotnet -Arguments @('build','reconstructed/Arconist.slnx','-c','Release','--configfile','reconstructed/NuGet.Config','-m:1','-nr:false')
    Invoke-Dotnet -Arguments @('reconstructed/tests/bin/Release/net10.0/Arconist.Tests.dll','.')
    foreach ($scenario in @('ordinary','input-first','frame-first')) {
        $chart = if ($scenario -eq 'ordinary') { 'research_harness/fixtures/ordinary_two_tap.aff' } else { 'research_harness/fixtures/native_late_input_expiry.aff' }
        Invoke-Dotnet -Arguments @('reconstructed/headless/bin/Release/net10.0/Arconist.Headless.dll',$chart,('reference_traces/r001/'+$scenario+'.schedule.json'),(Join-Path $toolsDir ($scenario+'.json')),'--reference',('reference_traces/r001/'+$scenario+'.reference.json'))
    }
    Invoke-Dotnet -Arguments @('build','reconstructed/hold-tests/Arconist.Hold.Tests.csproj','-c','Release','-m:1','-nr:false')
    Invoke-Dotnet -Arguments @('reconstructed/hold-tests/bin/Release/net10.0/Arconist.Hold.Tests.dll','.','reconstructed/out/r004-core')
    Push-Location $PSScriptRoot
    try {
        Invoke-Dotnet -Arguments @('build','Arconist.Godot.csproj','-c','Debug','-m:1','-nr:false')
        Invoke-Dotnet -Arguments @('build','tests/Arconist.Bridge.Tests.csproj','-c','Debug','-m:1','-nr:false')
        Invoke-Dotnet -Arguments @('tests/bin/Debug/net10.0/Arconist.Bridge.Tests.dll')
    } finally { Pop-Location }
    Invoke-Godot -Arguments @('--headless','--editor','--path','reconstructed/godot','--import','--quit')
    Invoke-Godot -Arguments @('--headless','--path','reconstructed/godot','--','--spatial-tests')
    Invoke-Godot -Arguments @('--headless','--path','reconstructed/godot','--','--hold-tests')
    Invoke-Godot -Arguments @('--headless','--path','reconstructed/godot','--export-release','Windows x64')
    if (-not (Test-Path (Join-Path $exportDir 'data_Arconist.Godot_windows_x86_64/coreclr.dll'))) { throw 'Self-contained runtime missing' }
    Write-Host ('Built Windows x64 application: '+(Join-Path $exportDir 'Arconist.exe'))
    Write-Host 'Export completed. Use build.py for logged ZIP packaging and integrity verification. Human qualification is pending.'
} finally { Pop-Location }
