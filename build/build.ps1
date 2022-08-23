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

param (
    [Parameter()]
    [switch]$UpdateMetaOnly
)

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
    # Reminder and ask for confirmation based on script arg

    if ($UpdateMetaOnly) {
        $reminder = "About to update project metadata."
    }
    else {
        $reminder = "About to build project source."
    }
    $reminder += " Did you remember to update the JSON metadata file in build/? (y/N) "
    Write-Host $reminder -NoNewline -ForegroundColor Yellow
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

function Update-ProjectMeta {
    # Automate pre-push checklist

    Write-CustomOutput "Running pre-push checklist..." -Level "INFO"

    # Update appropriate files using meta.json content
    $updaterPath = ".\update.py"
    python $updaterPath
    if ($LASTEXITCODE -ne 0) {
        Write-CustomOutput "An error occurred executing $updaterPath" -Level "ERROR"
        return
    }
    else {
        Write-CustomOutput "Finished executing update.py" -Level "INFO"
    }
}

function New-ProjectBuild {
    # Main process of building and cleaning up project source
    Write-Host "Running $SCRIPT_NAME..." -ForegroundColor Green

    # Pre-push checklist things, like updating version strings project-wide
    Update-ProjectMeta
    if ($LASTEXITCODE -ne 0) {
        Exit-ThisScript
    }

    # Build the project source
    $srcDir = "..\src"
    $distDir = Join-Path -Path (Get-Location) -ChildPath "..\dist"
    python -m build $srcDir --outdir $distDir

    # The x.y.z version part of the names orders them, use most updated wheel
    $wheelFiles = (Get-ChildItem -Path $distDir -Filter "*.whl")
    if ($wheelFiles.count -eq 0) {
        Write-CustomOutput "Something went wrong, can't find a whl file, aborted." -Level "ERROR"
        Exit-ThisScript
    }
    $recentWheel = $wheelFiles[-1]  # Assume this was the one just built

    # Install the built wheel in the virtual environment
    pip install $recentWheel.FullName --force-reinstall
    Write-CustomOutput "Finished attempting to pip install $recentWheel" -Level "INFO"

    # CLEANUP: Delete the generated .egg-info directory
    $eggDir = Join-Path -Path $srcDir -ChildPath "*.egg-info"
    Remove-Item -Path $eggDir -Recurse
    Write-CustomOutput "Removed generated egg-info directory" -Level "INFO"

    # Update requirements.txt
    $requirementsPath = "..\requirements.txt"
    pip freeze > $requirementsPath
    Write-CustomOutput "Updated $requirementsPath with state of current venv" -Level "INFO"

    Write-Host "Finished executing $SCRIPT_NAME, no errors detected." -ForegroundColor Green
}

<# MAIN PROCESS HERE #>

# Check these first
Assert-ScriptConditions
Read-Confirmation

# Run pre-push checklist things only if specified
if ($UpdateMetaOnly) {
    Update-ProjectMeta
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Finished executing '$SCRIPT_NAME -UpdateMetaOnly', no errors detected." -ForegroundColor Green
    }
    else {
        Write-Host "Finished executing '$SCRIPT_NAME -UpdateMetaOnly', errors detected." -ForegroundColor Red
    }
    exit
}

# Otherwise do the full build process
# Use Tee-Object to output to both console and log file
New-ProjectBuild | Tee-Object -FilePath $BUILD_LOG_PATH
