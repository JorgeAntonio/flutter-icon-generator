@echo off
echo ==========================================
echo Flutter Icon Generator - Build Script
echo ==========================================
echo.

REM Verificar si PyInstaller esta instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

echo Limpiando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo Construyendo ejecutable...
pyinstaller build.spec --clean

echo.
if exist "dist\FlutterIconGenerator.exe" (
    echo ==========================================
    echo ¡Build exitoso!
    echo Ejecutable: dist\FlutterIconGenerator.exe
    echo ==========================================
) else (
    echo ERROR: No se pudo crear el ejecutable
)

pause
