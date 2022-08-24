<#
Script for entering a test environment for testing a distribution of
the project.
Usage: At the project <root>/build/ directory.
```
PS> ./test 0.0.1
```
#>

param (
    [Parameter()]
    [string]$Version
)

$SCRIPT_NAME = "test.ps1"

<# Assert that script is being run at build/ directory #>
function Assert-ScriptConditions {
    $folderName = Split-Path -Path (Get-Location) -Leaf
    if ($folderName -ne "build") {
        Write-Host "Script should be run at the project build directory, aborted." -ForegroundColor Red
        exit 1
    }
}

<# Helper function for writing status based on exit code #>
function Write-CompletionStatus {
    if ($?) {
        Write-Host "Done." -ForegroundColor Green
    }
    else {
        Write-Host "Failed." -ForegroundColor Red
    }
}

<# Activate fresh venv .test-venv #>
function Start-VirtualEnv {
    # Create the venv if it doesn't exist
    $testVenvPath = "..\.test-venv"
    if (-Not (Test-Path $testVenvPath)) {
        Write-Host "Creating Python virtual environment .test-venv in parent directory..." -NoNewline -ForegroundColor Yellow
        try { python -m venv $testVenvPath }
        finally { Write-CompletionStatus }
    }

    # Activate the venv
    $activatePath = Join-Path -Path $testVenvPath -ChildPath ".\Scripts\Activate.ps1"
    Write-Host "Activating Python virtual environment .test-venv..." -NoNewline -ForegroundColor Yellow
    try { & $activatePath }
    finally { Write-CompletionStatus }
}

<# Assert that this venv is a fresh environment #>
function Assert-VenvConditions {
    # Use latest version of pip
    Write-Host "Using latest version of pip..." -ForegroundColor Yellow
    try { python -m pip install --upgrade pip }
    finally { Write-CompletionStatus }

    # Test if there's anything installed
    $pipInstalls = & pip freeze
    if ($null -eq $pipInstalls) {
        Write-Host ".test-venv is a clean environment, ready for testing." -ForegroundColor Green
        return
    }
    # If there is, wipe everything
    Write-Host ".test-venv has existing installations, uninstalling all..." -ForegroundColor Yellow
    $tempPath = ".\temp.txt"
    try {
        pip freeze > $tempPath
        pip uninstall -r $tempPath -y
    }
    finally {
        if (Test-Path $tempPath) {
            Remove-Item -Path $tempPath
        }
        Write-CompletionStatus
    }
}

<# Install the specified version of build #>
function Install-BuildVersion {
    # Couldn't pip uninstall properly, probably
    if (-Not $?) { exit 1 }

    $distPath = "..\dist"
    $wheelFiles = (Get-ChildItem -Path $distPath -Filter "*.whl")
    if ($wheelFiles.count -eq 0) {
        Write-Host "Something went wrong, can't find a whl file, aborted." -ForegroundColor Red
        exit 1
    }

    # Learning note: [string]$null is the empty string ""
    # Thus, default value of $Version is the empty string
    # If that's the case, just use the most recent whl file
    if ($Version -eq "") {
        $sortedWheels = ($wheelFiles | Sort-Object -Property { $_.CreationTime })
        $correctWheel = $sortedWheels[-1]
    }
    else {
        $correctWheel = $null
        foreach ($file in $wheelFiles) {
            if ($file.FullName -like "*$Version*") {
                $correctWheel = $file
                break
            }
        }
        if ($null -eq $correctWheel) {
            Write-Host "Can't find a whl file matching the specified version '$Version', aborted." -ForegroundColor Red
            exit 1
        }
    }

    # Install correct whl file
    Write-Host "Installing build $($correctWheel.ToString())..."
    # Since environment is asserted to be clean, no need to --force-reinstall
    try { pip install $correctWheel.FullName }
    finally { Write-CompletionStatus }
}

<# MAIN PROCESS HERE #>

Write-Host "Running $SCRIPT_NAME..." -ForegroundColor Yellow
Assert-ScriptConditions
Start-VirtualEnv
Assert-VenvConditions
Install-BuildVersion
Write-Host "Finished running $SCRIPT_NAME." -ForegroundColor Yellow
