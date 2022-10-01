<# Assert script conditions #>

# Run from project root to not mess up relative paths
if ((Get-Location).ToString() -ne $PSScriptRoot) {
    Write-Host "Script must be run at project root, aborted." -ForegroundColor Red
    exit 1
}

# Run in project's virtual environment to use its interpreter
if ($env:VIRTUAL_ENV -ne "$PSScriptRoot\.venv") {
    Write-Host "Script must be run in the project's activated .venv, aborted." -ForegroundColor Red
    exit 1
}

<# Reminder and confirmation#>

Write-Host "About to build project source. Did you remember to update metadata and documentation? (y/N) " -ForegroundColor Yellow
$confirmation = Read-Host
if ($confirmation -ne "y") {
    Write-Host "Aborted." -ForegroundColor Red
    exit 1
}

<# Run build command #>

# Build a whl file and then install globally for myself
python setup.py `
    bdist_wheel --dist-dir .\dist `
    install --user

exit $LASTEXITCODE
