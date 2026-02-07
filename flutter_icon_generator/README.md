# Flutter Icon Generator v2.0

Generador de iconos multiplataforma para Flutter con interfaz gráfica profesional.

## Características

### Fase 2 (v2.0) - ACTUAL
- ✅ **Preview Visual**: Vista previa en tiempo real de iconos Android, iOS y Adaptive
- ✅ **Configuración Persistente**: Guarda automáticamente preferencias y historial
- ✅ **Templates Predefinidos**: 6 templates optimizados para diferentes casos de uso
- ✅ **Historial de Archivos**: Acceso rápido a archivos recientes
- ✅ **Interfaz Mejorada**: Diseño profesional con panel dividido
- ✅ **Atajos de Teclado**: Ctrl+O para abrir archivos

### Fase 1 (v1.0)
- ✅ Generación completa de iconos para Android (7 archivos)
- ✅ Generación completa de iconos para iOS (16 archivos + Contents.json)
- ✅ Interfaz gráfica con tkinter
- ✅ Selección de archivo de entrada y carpeta de salida
- ✅ Color de fondo personalizable
- ✅ Escalado ajustable por plataforma
- ✅ Log de progreso en tiempo real
- ✅ Ejecutable .exe standalone

## Templates Disponibles

1. **Por defecto**: Configuración estándar recomendada
2. **Material Design**: Optimizado para Material Design (Android)
3. **iOS Rounded**: Optimizado para iconos redondeados de iOS
4. **Android Adaptive**: Foco en iconos adaptativos Android 8+
5. **Tema Oscuro**: Fondo oscuro para logos claros
6. **Marca Corporativa**: Márgenes amplios para logos con texto

## Instalación

### Descargar Ejecutable (Recomendado)
1. Descarga `FlutterIconGenerator.exe` desde la carpeta `dist/`
2. Ejecuta directamente (no requiere instalación)
3. ¡Listo!

### Desarrollo
```bash
# Clonar repositorio
git clone <url>
cd flutter_icon_generator

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python src/main.py
```

## Crear Ejecutable

```bash
# Instalar PyInstaller
pip install pyinstaller

# Construir (Windows)
build.bat

# O manualmente
pyinstaller build.spec --clean
```

El ejecutable se encontrará en `dist/FlutterIconGenerator.exe`

## Uso

### Interfaz Gráfica

1. **Seleccionar Imagen**: Botón "Buscar..." o Ctrl+O
2. **Elegir Template**: Selecciona de la lista desplegable (opcional)
3. **Configurar**: Ajusta color y escalas si es necesario
4. **Vista Previa**: Haz clic en "👁️ VISTA PREVIA" para ver el resultado
5. **Generar**: Haz clic en "🚀 GENERAR"
6. **Abrir Carpeta**: Se abrirá automáticamente la carpeta de salida

### Atajos de Teclado

- **Ctrl+O**: Abrir imagen
- **Menú Archivo → Archivos recientes**: Acceso rápido

## Estructura de Salida

```
output/
├── android/
│   ├── mipmap-mdpi/ic_launcher.png (48x48)
│   ├── mipmap-hdpi/ic_launcher.png (72x72)
│   ├── mipmap-xhdpi/ic_launcher.png (96x96)
│   ├── mipmap-xxhdpi/ic_launcher.png (144x144)
│   ├── mipmap-xxxhdpi/ic_launcher.png (192x192)
│   ├── ic_launcher_foreground.png (432x432)
│   └── ic_launcher_1024x1024.png
└── ios/
    └── AppIcon.appiconset/
        ├── Contents.json
        ├── Icon-App-20x20@1x.png ... @3x.png
        ├── Icon-App-29x29@1x.png ... @3x.png
        ├── Icon-App-40x40@1x.png ... @3x.png
        ├── Icon-App-60x60@2x.png ... @3x.png
        ├── Icon-App-76x76@1x.png ... @2x.png
        ├── Icon-App-83.5x83.5@2x.png
        └── Icon-App-1024x1024@1x.png
```

## Uso en Flutter

### Manual
1. Copia la carpeta `android/` a `android/app/src/main/res/`
2. Copia la carpeta `ios/` a `ios/Runner/Assets.xcassets/`
3. Reemplaza los archivos existentes

### Con flutter_launcher_icons
1. Copia los archivos a tu carpeta `assets/images/`
2. Configura tu `pubspec.yaml`:
```yaml
dev_dependencies:
  flutter_launcher_icons: ^0.13.1

flutter_icons:
  android: true
  ios: true
  image_path: "assets/images/ic_launcher_1024x1024.png"
```
3. Ejecuta:
```bash
flutter pub run flutter_launcher_icons
```

## Estructura del Proyecto

```
flutter_icon_generator/
├── src/
│   ├── __init__.py
│   ├── main.py              # Interfaz gráfica principal
│   ├── icon_generator.py    # Lógica de generación
│   ├── config_manager.py    # Configuración persistente
│   └── preview_manager.py   # Sistema de preview visual
├── dist/
│   ├── FlutterIconGenerator.exe  # Ejecutable
│   └── README.txt
├── build.spec               # Configuración PyInstaller
├── build.bat / build.sh     # Scripts de construcción
├── requirements.txt
└── README.md
```

## Configuración Persistente

La aplicación guarda automáticamente:
- Último archivo de entrada
- Última carpeta de salida
- Color de fondo seleccionado
- Escalas de Android e iOS
- Tamaño y posición de la ventana
- Historial de archivos recientes (últimos 10)

Ubicación:
- Windows: `%APPDATA%\FlutterIconGenerator\config.json`

## Solución de Problemas

### La aplicación no inicia
- Verifica Windows 10/11
- Ejecuta como Administrador

### Error al generar iconos
- Verifica que la imagen no esté corrupta
- Comprueba permisos de escritura
- Usa formato PNG para mejor compatibilidad

### Los iconos se ven mal
- Usa "Vista Previa" antes de generar
- Ajusta las escalas con los sliders
- Prueba diferentes templates
- Usa imagen de alta resolución (512x512 mínimo)

### Configuración no se guarda
- Verifica permisos en `%APPDATA%\FlutterIconGenerator\`

## Roadmap

### Fase 1 ✅ (Completada)
- Core funcional
- Generación completa Android/iOS
- Interfaz básica

### Fase 2 ✅ (Actual)
- Preview visual
- Configuración persistente
- Templates predefinidos
- Historial de archivos

### Fase 3 (Próxima)
- Integración automática con flutter_launcher_icons
- Soporte Web, Windows y macOS
- Generación automática de YAML
- Más templates personalizables
- Importación de configuraciones

## Requisitos

- Windows 10/11
- Python 3.8+ (solo para desarrollo)
- Pillow, PyInstaller (solo para desarrollo)

## Licencia

MIT License - Libre para usar y modificar

## Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

**Hecho con ❤️ para la comunidad Flutter**
