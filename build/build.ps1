# build.ps1

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

function New-ProjectBuild {
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

    Write-Host "Running build.ps1..." -ForegroundColor Green

    # Build the project source
    $srcDir = "..\src"
    python -m build $srcDir

    # Build failed or path is wrong, abort immediately
    # Learning note: Join-Path always returns a string instead of FileInfo
    $generatedDir = Join-Path -Path $srcDir -ChildPath "dist"
    if (-Not (Test-Path $generatedDir)) {
        Write-Host "Something went wrong, can't find the generated dist directory, aborted." -ForegroundColor Red
        exit
    }

    # The x.y.z version part of the names orders them, use most updated wheel
    $wheelFiles = (Get-ChildItem -Path $generatedDir -Filter "*.whl")
    if ($wheelFiles.count -eq 0) {
        Write-Host "Something went wrong, can't find a whl file, aborted." -ForegroundColor Red
        exit
    }
    $recentWheel = $wheelFiles[-1]  # Assume this was the one just built

    # Install the built wheel in the virtual environment
    pip install $recentWheel.FullName --force-reinstall
    Write-Host "Finished attempting to pip install $recentWheel" -ForegroundColor Green

    # CLEANUP

    # Move the dist folder contents to the project level dist
    $generatedDirContents = Join-Path -Path $generatedDir -ChildPath "*"
    $rootDistDir = Join-Path -Path (Get-Location) -ChildPath "..\dist"
    Move-Item -Path $generatedDirContents -Destination $rootDistDir -Force

    # Delete the now empty dist folder inside build/
    Remove-Item $generatedDir

    Write-Host "Finished executing build.ps1!" -ForegroundColor Green
}

# Output to both console and log file
New-ProjectBuild | Tee-Object -FilePath ".\build.log"
