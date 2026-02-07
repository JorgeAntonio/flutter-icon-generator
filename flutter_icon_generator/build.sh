#!/bin/bash

echo "=========================================="
echo "Flutter Icon Generator - Build Script"
echo "=========================================="
echo ""

# Verificar si PyInstaller esta instalado
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "Instalando PyInstaller..."
    pip install pyinstaller
fi

echo "Limpiando builds anteriores..."
rm -rf build dist

echo ""
echo "Construyendo ejecutable..."
pyinstaller build.spec --clean

echo ""
if [ -f "dist/FlutterIconGenerator" ]; then
    echo "=========================================="
    echo "¡Build exitoso!"
    echo "Ejecutable: dist/FlutterIconGenerator"
    echo "=========================================="
else
    echo "ERROR: No se pudo crear el ejecutable"
fi
