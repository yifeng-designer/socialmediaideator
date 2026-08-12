$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $projectRoot ".env"

if (-not $env:APIFY_API_TOKEN -and (Test-Path $envFile)) {
    $tokenLine = Get-Content $envFile | Where-Object { $_ -match '^\s*APIFY_API_TOKEN\s*=' } | Select-Object -First 1
    if ($tokenLine) {
        $env:APIFY_API_TOKEN = ($tokenLine -replace '^\s*APIFY_API_TOKEN\s*=\s*', '').Trim()
    }
}

if (-not $env:APIFY_API_TOKEN) {
    throw "APIFY_API_TOKEN is not set. Add it to .env or the environment before running the weekly fetch."
}

& python (Join-Path $PSScriptRoot "fetch_ig_data.py")
if ($LASTEXITCODE -ne 0) { throw "Instagram fetch failed." }

& python (Join-Path $PSScriptRoot "build_idea_context.py")
if ($LASTEXITCODE -ne 0) { throw "Idea context build failed." }

Write-Host "Weekly context is ready. Use workflow_prompt.md to generate ideas."
