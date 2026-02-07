# Flutter Icon Generator v2.0

## Archivos Incluidos
- `FlutterIconGenerator.exe` - Aplicación principal

## Requisitos
- Windows 10/11
- No requiere Python ni otras dependencias

## Novedades en v2.0 (Fase 2)

### Preview Visual 👁️
- Vista previa en tiempo real de cómo quedarán tus iconos
- Compara Android, iOS y Adaptive side-by-side
- Botón "Vista Previa" antes de generar

### Configuración Persistente 💾
- Guarda automáticamente tus preferencias
- Historial de archivos recientes (menú Archivo)
- Recuerda última carpeta de salida
- Conserva escalas y colores entre sesiones

### Templates Predefinidos 🎨
- **Por defecto**: Configuración estándar recomendada
- **Material Design**: Optimizado para Android Material
- **iOS Rounded**: Optimizado para iconos redondeados de iOS
- **Android Adaptive**: Foco en iconos adaptativos Android 8+
- **Tema Oscuro**: Fondo oscuro para logos claros
- **Marca Corporativa**: Márgenes amplios para logos con texto

## Cómo Usar

### 1. Selecciona tu imagen
- Haz clic en "Buscar..." o usa Ctrl+O
- Selecciona tu logo (PNG, JPG, JPEG, GIF, BMP)
- Se mostrará información de la imagen (dimensiones)

### 2. Elige un Template (opcional)
- Selecciona de la lista desplegable
- Los templates ajustan automáticamente escalas y colores
- Lee la descripción debajo del selector

### 3. Configura manualmente (opcional)
- **Color de fondo**: Usa "Elegir Color" o "Transparente"
- **Escalas**: Ajusta con los sliders (Android: 80%, iOS: 85% por defecto)

### 4. Vista Previa (recomendado)
- Haz clic en "👁️ VISTA PREVIA"
- Revisa cómo quedarán los iconos antes de generar
- Ajusta configuración si es necesario

### 5. Genera los iconos
- Selecciona carpeta de salida (o usa la por defecto)
- Haz clic en "🚀 GENERAR"
- Se crearán 23 archivos automáticamente

### 6. Accede a archivos recientes
- Menú "Archivo" → "Archivos recientes"
- Acceso rápido a imágenes usadas anteriormente

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

### Manual:
1. Copia la carpeta `android/` a `android/app/src/main/res/`
2. Copia la carpeta `ios/` a `ios/Runner/Assets.xcassets/`
3. Reemplaza los archivos existentes

### Con flutter_launcher_icons:
1. Copia los archivos a tu carpeta `assets/images/`
2. Configura tu `pubspec.yaml`
3. Ejecuta `flutter pub run flutter_launcher_icons`

## Características

✅ **Generación Completa**: 23 archivos (7 Android + 16 iOS)
✅ **Preview Visual**: Vista previa en tiempo real
✅ **Templates**: 6 configuraciones predefinidas
✅ **Configuración Persistente**: Guarda preferencias automáticamente
✅ **Historial**: Archivos recientes accesibles
✅ **Interfaz Mejorada**: Diseño limpio y profesional
✅ **Atajos de Teclado**: Ctrl+O para abrir archivo
✅ **Sin Dependencias**: Ejecutable standalone

## Atajos de Teclado

- **Ctrl+O**: Abrir imagen
- **Menú Archivo**: Acceso a archivos recientes

## Solución de Problemas

**La aplicación no inicia:**
- Asegúrate de tener Windows 10 o superior
- Ejecuta como Administrador si es necesario

**Error al generar iconos:**
- Verifica que la imagen de entrada no esté corrupta
- Asegúrate de tener permisos de escritura en la carpeta de salida
- Intenta con otra imagen (formato PNG recomendado)

**Los iconos se ven mal:**
- Usa la "Vista Previa" antes de generar
- Ajusta las escalas con los sliders
- Prueba diferentes templates
- Usa una imagen de mayor resolución (mínimo 512x512 recomendado)
- Verifica que tu logo tenga buen contraste

**Vista previa no funciona:**
- Asegúrate de haber seleccionado una imagen primero
- Verifica que la imagen no esté corrupta

**Configuración no se guarda:**
- La configuración se guarda en %APPDATA%\FlutterIconGenerator\
- Asegúrate de tener permisos de escritura en esa carpeta

## Ubicación de Configuración

La configuración se guarda en:
- Windows: `%APPDATA%\FlutterIconGenerator\config.json`

## Soporte

Para reportar problemas o sugerencias:
- Revisa el log de progreso en la aplicación
- Verifica que cumples con los requisitos mínimos

## Versiones

- **v2.0** (Actual): Fase 2 - Preview visual + Configuración persistente + Templates
- **v1.0**: Fase 1 - Core funcional (Android + iOS completo)

## Próximas Funciones (Fase 3)

- Integración automática con flutter_launcher_icons
- Soporte Web, Windows y macOS
- Generación automática de YAML
- Más templates personalizables

---

**Nota:** Este ejecutable es standalone y no requiere instalación de Python ni ninguna otra dependencia.

**Licencia:** Libre para usar y modificar (MIT License)
