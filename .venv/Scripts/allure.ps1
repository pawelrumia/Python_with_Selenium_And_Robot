# PowerShell wrapper for Allure CLI
$userAllure = "$env:USERPROFILE\Documents\allure\bin\allure.bat"
if (Test-Path $userAllure) {
    & $userAllure @args
} else {
    Write-Error "Allure not found at $userAllure"
    exit 1
}

