# Flutter Icon Generator v1.0

## Archivos Incluidos
- `FlutterIconGenerator.exe` - Aplicación principal

## Requisitos
- Windows 10/11
- No requiere Python ni otras dependencias

## Cómo Usar

1. **Ejecuta** `FlutterIconGenerator.exe`

2. **Selecciona tu imagen**:
   - Haz clic en "Buscar..." junto a "Imagen de Entrada"
   - Selecciona tu logo (PNG, JPG, JPEG, GIF, BMP)
   - Se mostrará una vista previa

3. **Configura el color de fondo** (opcional):
   - Por defecto: Blanco (#FFFFFF)
   - Usa "Elegir Color" para seleccionar otro color
   - Usa "Transparente" para fondo transparente (solo foreground)

4. **Ajusta las escalas** (opcional):
   - Escala Android: 80% por defecto
   - Escala iOS: 85% por defecto
   - Ajusta según necesites con los sliders

5. **Selecciona carpeta de salida**:
   - Por defecto: `output/` en la misma carpeta
   - Usa "Cambiar..." para seleccionar otra ubicación

6. **Genera los iconos**:
   - Haz clic en "🚀 GENERAR ICONOS"
   - Espera a que termine el proceso
   - Se generarán 23 archivos automáticamente

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

1. Copia la carpeta `android/` a `android/app/src/main/res/`
2. Copia la carpeta `ios/` a `ios/Runner/Assets.xcassets/`
3. Reemplaza los archivos existentes

O usa con `flutter_launcher_icons`:
- Copia los archivos a tu carpeta `assets/images/`
- Configura tu `pubspec.yaml`
- Ejecuta `flutter pub run flutter_launcher_icons`

## Características

✅ Genera todos los tamaños necesarios para Android (5 densidades)
✅ Genera todos los tamaños necesarios para iOS (16 iconos)
✅ Incluye Contents.json para iOS
✅ Preview de imagen antes de generar
✅ Color de fondo personalizable
✅ Escalado ajustable por plataforma
✅ Interfaz gráfica intuitiva
✅ Log de progreso en tiempo real
✅ Sin dependencias externas

## Solución de Problemas

**La aplicación no inicia:**
- Asegúrate de tener Windows 10 o superior
- Ejecuta como Administrador si es necesario

**Error al generar iconos:**
- Verifica que la imagen de entrada no esté corrupta
- Asegúrate de tener permisos de escritura en la carpeta de salida
- Intenta con otra imagen (formato PNG recomendado)

**Los iconos se ven mal:**
- Ajusta las escalas con los sliders
- Usa una imagen de mayor resolución (mínimo 512x512 recomendado)
- Verifica que tu logo tenga buen contraste

## Soporte

Para reportar problemas o sugerencias, contacta al desarrollador.

## Versión

v1.0 - Fase 1: Core funcional

---

**Nota:** Este ejecutable es standalone y no requiere instalación de Python ni ninguna otra dependencia.
