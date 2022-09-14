<#
.Synopsis
   Script for automating some development tasks.
.INPUTS
   The first argument should be the name of the task to run, such as "compile". All arguments after that are the arguments to that task.
.NOTES
   This script should be run at the project root and in its activated Python virtual environment.
#>

<# Assert script conditions #>

# Run from project root to not mess up relative paths
if ((Get-Location).ToString() -ne $PSScriptRoot) {
    Write-Host "Script must be run at project root, aborted." -ForegroundColor Red
    exit 1
}
# Run in project's virtual environment to use its interpreter and dependencies
if ($env:VIRTUAL_ENV -ne (Join-Path $PSScriptRoot ".venv")) {
    Write-Host "Script must be run in the project's activated .venv, aborted." -ForegroundColor Red
    exit 1
}

<# Save $args globally for access in function scopes #>

$runArgs = $args

<# Tasks and helper functions #>

function _get_version {
    $loadedObj = Get-Content -Raw .\meta.json | ConvertFrom-Json
    $versionString = $loadedObj.version
    if ($null -eq $versionString) {
        Write-Host "Couldn't get version string from meta.json, aborted." -ForegroundColor Red
        exit 1
    }
    return $versionString
}

function _update_metadata {
    # Update things containing the version string
    Write-Host "Updating project metadata..." -ForegroundColor Yellow
    python .\build\update.py
    if (!$?) {
        Write-Host "An error occurred in update.py, aborted." -ForegroundColor Red
        exit 1
    }

    # Update requirements.txt
    pip freeze | Out-File -Encoding utf8 .\requirements.txt
    Write-Host "Updated requirements.txt with current state of .venv." -ForegroundColor Yellow
}

function _run_package {
    Write-Host "Running the project package..." -ForegroundColor Yellow
    # Use the spread operator to obtain an array "slice"
    $packageArgs = $runArgs[1..($runArgs.Length - 1)]
    python .\src\driver.py $packageArgs
}

function _compile_src {
    # Remind and ask for confirmation
    Write-Host "About to build project source. Did you remember to update meta.json? (y/N) " -ForegroundColor Yellow
    $confirmation = Read-Host
    if ($confirmation -ne "y") {
        Write-Host "Aborted." -ForegroundColor Red
    }

    # Update metadata
    _update_metadata

    # Run pyinstaller
    Write-Host "Compiling project source..." -ForegroundColor Yellow
    $outputName = "waifu_roller-$(_get_version)"
    $distPath = ".\dist\exes"
    $workPath = ".\build\temp"
    $specPath = ".\build\specs"
    pyinstaller .\src\driver.py `
        --onedir --noconfirm `
        --name $outputName `
        --distpath $distPath `
        --workpath $workPath `
        --specpath $specPath

    # Always attempt to remove --workpath stuff from pyinstaller
    try { Remove-Item -Recurse $workPath } catch {}
    # If some error occurred, remove --distpath and --specpath too
    if (!$?) {
        try { Remove-Item -Recurse "$distPath\$outputName" } catch {}
        try { Remove-Item -Recurse "$specPath\$outputName" } catch {}
        Write-Host "An error occurred with pyinstaller, aborted." -ForegroundColor Red
        exit 1
    }

    # Rename the main executable
    $generatedPath = "$distPath\$outputName"
    Rename-Item "$generatedPath\$outputName.exe" "waifu.exe"

    # Compress to zip file
    $destPath = "$generatedPath.zip"
    Compress-Archive -Path $generatedPath `
        -DestinationPath $destPath `
        -CompressionLevel Optimal `
        -Update

    # Remove original directory
    Remove-Item -Recurse $generatedPath
}

function _run_task {
    if ($runArgs.Length -eq 0) {
        Write-Host "Did not specify a task name, aborted." -ForegroundColor Red
        exit 1
    }
    $taskName = $runArgs[0]
    switch ($taskName) {
        "waifu" { _run_package }
        "compile" { _compile_src }
        default {
            Write-Host "Unrecognized task name, aborted." -ForegroundColor Red
            exit 1
        }
    }
}

<# MAIN PROCESS HERE #>

_run_task

Write-Host "Finished running run.ps1." -ForegroundColor Green
exit 0
