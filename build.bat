@echo off
echo ==========================================
echo Flutter Icon Generator - Build Script
echo ==========================================
echo.

REM Activar entorno virtual
if exist "venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo Advertencia: No se encontro el entorno virtual venv\
    echo Usando Python del sistema...
)

echo.
echo Verificando dependencias...
python -c "import PIL, yaml" 2>nul
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo Verificando PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

echo.
echo Limpiando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo Construyendo ejecutable...
python -m PyInstaller build.spec --clean

echo.
if exist "dist\FlutterIconGenerator.exe" (
    echo ==========================================
    echo Build exitoso!
    echo Ejecutable: dist\FlutterIconGenerator.exe
    echo ==========================================
) else (
    echo ERROR: No se pudo crear el ejecutable
)

REM Desactivar entorno virtual
if exist "venv\Scripts\deactivate.bat" (
    call venv\Scripts\deactivate.bat
)

echo.
pause
