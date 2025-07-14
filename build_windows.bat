@echo off
REM PDF Extractor - Windows Build Script
REM Creates a single executable for Windows

echo 🔨 Building PDF Extractor for Windows...

REM Activate virtual environment
call pdf_env_new\Scripts\activate.bat

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist pdf_extractor.spec del pdf_extractor.spec

REM Build executable for Windows
echo 🏗️  Building Windows executable...
pyinstaller --onefile ^
    --name "pdf-extractor-windows" ^
    --optimize 2 ^
    --strip ^
    --console ^
    --add-data "README.md;." ^
    pdf_extractor.py

REM Get file size
for %%I in (dist\pdf-extractor-windows.exe) do set FILE_SIZE=%%~zI

echo ✅ Build completed successfully!
echo 📦 Executable: dist\pdf-extractor-windows.exe
echo 📏 File size: %FILE_SIZE% bytes
echo.
echo 🧪 Testing executable...
dist\pdf-extractor-windows.exe --help

echo.
echo 🎉 Windows build ready for distribution!
echo    Location: %cd%\dist\pdf-extractor-windows.exe

pause