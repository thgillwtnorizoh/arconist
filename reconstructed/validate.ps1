param([string]$OutputDirectory = (Join-Path $PSScriptRoot 'out'))
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$env:DOTNET_CLI_HOME = Join-Path $PSScriptRoot '.dotnet'
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
$env:DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE = '1'
$env:DOTNET_GENERATE_ASPNET_CERTIFICATE = 'false'
$env:MSBuildEnableWorkloadResolver = 'false'
function Invoke-Checked {
    param([string[]]$CommandArgs)
    Write-Host ('rtk proxy dotnet ' + ($CommandArgs -join ' '))
    & rtk proxy dotnet @CommandArgs
    $code = $LASTEXITCODE
    Write-Host ('Exit code: ' + $code)
    if ($code -ne 0) { throw ('Validation command failed with exit ' + $code) }
}
Push-Location $repoRoot
try {
    New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
    Invoke-Checked -CommandArgs @('build','reconstructed/Arconist.slnx','-c','Release','--configfile','reconstructed/NuGet.Config','-m:1','-nr:false')
    Invoke-Checked -CommandArgs @('reconstructed/tests/bin/Release/net10.0/Arconist.Tests.dll','.')
    foreach ($scenario in @('ordinary','input-first','frame-first')) {
        $chartPath = if ($scenario -eq 'ordinary') { 'research_harness/fixtures/ordinary_two_tap.aff' } else { 'research_harness/fixtures/native_late_input_expiry.aff' }
        Invoke-Checked -CommandArgs @('reconstructed/headless/bin/Release/net10.0/Arconist.Headless.dll',$chartPath,('reference_traces/r001/'+$scenario+'.schedule.json'),(Join-Path $OutputDirectory ($scenario+'.json')),'--reference',('reference_traces/r001/'+$scenario+'.reference.json'))
    }
} finally { Pop-Location }
