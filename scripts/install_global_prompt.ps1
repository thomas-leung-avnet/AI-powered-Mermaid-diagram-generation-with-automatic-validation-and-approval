param(
    [string]$PromptName = "diagram-standardizer.prompt.md"
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$sourcePrompt = Join-Path $repoRoot "global\diagram-standardizer.prompt.md"

if (-not (Test-Path $sourcePrompt)) {
    throw "Prompt file not found: $sourcePrompt"
}

$userPromptsDir = Join-Path $env:APPDATA "Code\User\prompts"
New-Item -ItemType Directory -Path $userPromptsDir -Force | Out-Null

$targetPrompt = Join-Path $userPromptsDir $PromptName
Copy-Item -Path $sourcePrompt -Destination $targetPrompt -Force

Write-Host "Installed global prompt to: $targetPrompt"
Write-Host "Restart VS Code if the prompt does not appear immediately."
