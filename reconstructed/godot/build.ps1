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
# Explicit offline build option: packages must already exist locally. This only
# skips the unreachable online advisory lookup; no test or compiler gate changes.
if ($OfflineRestore) { $env:NuGetAudit = 'false' }
$toolsDir = Join-Path $repoRoot 'reconstructed/out/r002-tools'
$exportDir = Join-Path $repoRoot 'reconstructed/out/r003-windows'
function Invoke-Dotnet {
    param([string[]]$Arguments)
    & rtk proxy dotnet @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'dotnet command failed' }
}
function Invoke-Godot {
    param([string[]]$Arguments)
    $lines = & rtk proxy $GodotExecutable @Arguments 2>&1
    $code = $LASTEXITCODE
    $lines | ForEach-Object { Write-Host $_ }
    # Godot's first failed .NET export returned0 with ERROR lines: inspect both.
    if ($code -ne 0 -or ($lines -match '^ERROR:')) { throw 'Godot reported an execution/export error' }
}
$version = (& rtk proxy $GodotExecutable --version | Out-String).Trim()
if ($version -notlike '4.7.2.stable.mono.*') { throw ('Required Godot4.7.2 .NET; actual '+$version) }
New-Item -ItemType Directory -Force -Path $toolsDir,$exportDir | Out-Null
$archive = Join-Path $toolsDir 'templates.tpz'
if (-not (Test-Path -LiteralPath $archive)) {
    & rtk proxy curl.exe -L --fail --output $archive 'https://downloads.godotengine.org/?flavor=stable&platform=templates&slug=mono_export_templates.tpz&version=4.7.2'
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
    & rtk proxy powershell -NoProfile -ExecutionPolicy Bypass -File reconstructed/validate.ps1
    if ($LASTEXITCODE -ne 0) { throw 'R001 regression failed' }
    Push-Location $PSScriptRoot
    try {
        Invoke-Dotnet -Arguments @('build','Arconist.Godot.csproj','-c','Debug','-m:1','-nr:false')
        Invoke-Dotnet -Arguments @('build','tests/Arconist.Bridge.Tests.csproj','-c','Debug','-m:1','-nr:false')
        Invoke-Dotnet -Arguments @('tests/bin/Debug/net10.0/Arconist.Bridge.Tests.dll')
    } finally { Pop-Location }
    Invoke-Godot -Arguments @('--headless','--editor','--path','reconstructed/godot','--import','--quit')
    Invoke-Godot -Arguments @('--headless','--path','reconstructed/godot','--','--spatial-tests')
    Invoke-Godot -Arguments @('--headless','--path','reconstructed/godot','--export-release','Windows x64')
    if (-not (Test-Path (Join-Path $exportDir 'data_Arconist.Godot_windows_x86_64/coreclr.dll'))) { throw 'Self-contained runtime missing' }
    Write-Host ('Built Windows x64 application: '+(Join-Path $exportDir 'Arconist.exe'))
    Write-Host 'Graphical launch/input/results validation must still be performed separately.'
} finally { Pop-Location }
