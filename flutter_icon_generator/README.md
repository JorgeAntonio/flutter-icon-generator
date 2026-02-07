# Flutter Icon Generator

Generador de iconos multiplataforma para Flutter con interfaz gráfica.

## Características (Fase 1)

- ✅ Generación completa de iconos para Android (todos los tamaños mipmap)
- ✅ Generación completa de iconos para iOS (AppIcon.appiconset)
- ✅ Interfaz gráfica con tkinter
- ✅ Selección de archivo de entrada
- ✅ Selección de carpeta de salida
- ✅ Color de fondo personalizable
- ✅ Preview de imagen
- ✅ Ejecutable .exe standalone

## Instalación

### Para desarrollo:
```bash
pip install -r requirements.txt
python src/main.py
```

### Para crear el ejecutable:
```bash
pip install pyinstaller
pyinstaller build.spec
```

El ejecutable se encontrará en `dist/FlutterIconGenerator.exe`

## Uso

1. Ejecuta `FlutterIconGenerator.exe`
2. Selecciona tu imagen de logo
3. Configura el color de fondo (opcional)
4. Selecciona la carpeta de salida
5. Haz clic en "Generar Iconos"

## Estructura de Salida

```
output/
├── android/
│   ├── mipmap-hdpi/
│   ├── mipmap-mdpi/
│   ├── mipmap-xhdpi/
│   ├── mipmap-xxhdpi/
│   ├── mipmap-xxxhdpi/
│   └── ic_launcher-web.png
└── ios/
    └── AppIcon.appiconset/
        ├── Contents.json
        ├── Icon-App-20x20@1x.png
        ├── Icon-App-20x20@2x.png
        ├── Icon-App-20x20@3x.png
        ├── Icon-App-29x29@1x.png
        ├── Icon-App-29x29@2x.png
        ├── Icon-App-29x29@3x.png
        ├── Icon-App-40x40@1x.png
        ├── Icon-App-40x40@2x.png
        ├── Icon-App-40x40@3x.png
        ├── Icon-App-60x60@2x.png
        ├── Icon-App-60x60@3x.png
        ├── Icon-App-76x76@1x.png
        ├── Icon-App-76x76@2x.png
        └── Icon-App-83.5x83.5@2x.png
```

## Fases del Proyecto

- **Fase 1:** Core funcional (Android/iOS completo) - ✅ Actual
- **Fase 2:** Preview visual + configuración persistente
- **Fase 3:** Integración Flutter automática + Web + Windows + macOS

## Licencia

MIT License - Libre para usar y modificar
