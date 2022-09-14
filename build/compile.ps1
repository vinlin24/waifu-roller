<# PyInstaller script #>

pyinstaller ..\src\driver.py --onedir `
    --distpath .\temp\dist --workpath .\temp\build `
    --specpath .\temp --name waifu --noconfirm
