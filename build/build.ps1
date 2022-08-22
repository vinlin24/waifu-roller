<#
Script for automating the build process and installing the generated
wheel in local .venv for testing.
Usage: within the project's activated virtual environment, and at the
project <root>/build/ directory.
```
(.venv) PS> ./build
```
NOTE: This script automatically reinstalls the build with pip in the
venv for development testing, but it ASSUMES that the generated wheel
with the highest version substring is the one just built.
#>

$SCRIPT_NAME = "build.ps1"
$BUILD_LOG_PATH = ".\build.log"

function Assert-ScriptConditions {
    # Assert that script is being run at build/ in an activated venv
    if (-Not $env:VIRTUAL_ENV) {
        Write-Host "Script should be run in a virtual environment, aborted." -ForegroundColor Red
        exit
    }
    $folderName = Split-Path -Path (Get-Location) -Leaf
    if ($folderName -ne "build") {
        Write-Host "Script should be run at the project build directory, aborted." -ForegroundColor Red
        exit
    }
}

function Read-Confirmation {
    # Reminder and ask for confirmation
    Write-Host "About to build project source. Did you remember to update the version string in setup.cfg? (y/N) " -NoNewline -ForegroundColor Yellow
    $confirmation = Read-Host
    # Learning note: PS -eq/-ne is case-insensitive, -ceq/-cne is case-sensitive
    if ($confirmation -ne "y") {
        Write-Host "$SCRIPT_NAME canceled." -ForegroundColor Red
        exit
    }
}

function Write-CustomOutput {
    # Wrapper for writing log-like outputs
    param (
        [Parameter(Mandatory = $true)]
        [System.Object]$Object,
        [Parameter()]  # Learning note: () here is very important
        [string]$Level = "INFO"
    )
    Write-Output "[$SCRIPT_NAME] $($Level): $Object"
}

function Exit-ThisScript {
    # Exit script and notify console that process couldn't be completed
    Write-Host "Could not complete $SCRIPT_NAME." -ForegroundColor Red
    exit
}

function New-ProjectBuild {
    # Build the project source
    $srcDir = "..\src"
    python -m build $srcDir

    # Build failed or path is wrong, abort immediately
    # Learning note: Join-Path always returns a string instead of FileInfo
    $generatedDir = Join-Path -Path $srcDir -ChildPath "dist"
    if (-Not (Test-Path $generatedDir)) {
        Write-CustomOutput "Something went wrong, can't find the generated dist directory, aborted." -Level "ERROR"
        Exit-ThisScript
    }

    # The x.y.z version part of the names orders them, use most updated wheel
    $wheelFiles = (Get-ChildItem -Path $generatedDir -Filter "*.whl")
    if ($wheelFiles.count -eq 0) {
        Write-CustomOutput "Something went wrong, can't find a whl file, aborted." -Level "ERROR"
        Exit-ThisScript
    }
    $recentWheel = $wheelFiles[-1]  # Assume this was the one just built

    # Install the built wheel in the virtual environment
    pip install $recentWheel.FullName --force-reinstall
    Write-CustomOutput "Finished attempting to pip install $recentWheel" -Level "INFO"

    # CLEANUP

    # Move the dist folder contents to the project level dist
    $generatedDirContents = Join-Path -Path $generatedDir -ChildPath "*"
    $rootDistDir = Join-Path -Path (Get-Location) -ChildPath "..\dist"
    Move-Item -Path $generatedDirContents -Destination $rootDistDir -Force

    # Delete the now empty dist folder inside build/
    Remove-Item -Path $generatedDir

    # Delete the generated .egg-info directory as well
    $eggDir = Join-Path -Path $srcDir -ChildPath "*.egg-info"
    Remove-Item -Path $eggDir -Recurse
    
    Write-CustomOutput "Finished cleaning up generated dist and egg-info directories" -Level "INFO"
}

# Check these first
Assert-ScriptConditions
Read-Confirmation

Write-Host "Running $SCRIPT_NAME..." -ForegroundColor Green

# Output to both console and log file
New-ProjectBuild | Tee-Object -FilePath $BUILD_LOG_PATH

Write-Host "Finished executing $SCRIPT_NAME!" -ForegroundColor Green
