# Flutter Icon Generator v3.0

## 🎉 Fase 3 Completada: Multiplataforma + Integración Flutter

Generador de iconos profesional para Flutter con soporte completo para **5 plataformas**:
- ✅ Android
- ✅ iOS  
- ✅ Web / PWA
- ✅ Windows
- ✅ macOS

---

## ✨ Características Principales

### 🚀 **Novedades Fase 3**
- **Soporte Multiplataforma**: Genera iconos para Android, iOS, Web, Windows y macOS
- **Generación Automática de YAML**: Crea `flutter_launcher_icons.yaml` listo para usar
- **Integración Directa**: Copia automática de iconos a tu proyecto Flutter
- **Verificación de Flutter**: Detecta si Flutter está instalado en tu sistema
- **+40 Archivos Generados**: Incluye todos los tamaños necesarios para cada plataforma
- **Favicons Web**: Incluye favicon.ico multi-resolución y manifest.json para PWA
- **Iconos Windows**: Incluye app_icon.ico para aplicaciones Windows
- **Iconos macOS**: Estructura completa para App Store

### 🎨 **Fase 2**
- Preview visual en tiempo real
- Configuración persistente (guarda preferencias)
- 14 Templates predefinidos (8 nuevos en Fase 3)
- Historial de archivos recientes

### ⚡ **Fase 1**
- Generación completa Android/iOS
- Interfaz gráfica intuitiva
- Escalado ajustable por plataforma
- Sin dependencias externas

---

## 📦 Instalación

### Opción 1: Ejecutable (Recomendado) ⭐
1. Descarga `FlutterIconGenerator.exe` desde Releases
2. Ejecuta directamente (no requiere instalación)
3. ¡Listo!

### Opción 2: Desde Código Fuente
```bash
git clone <url>
cd flutter_icon_generator
pip install -r requirements.txt
python src/main.py
```

---

## 🎯 Cómo Usar

### 1️⃣ Seleccionar Imagen
- Haz clic en "Buscar..." o usa **Ctrl+O**
- Selecciona tu logo (PNG, JPG, JPEG, GIF, BMP)
- Verás la vista previa y dimensiones

### 2️⃣ Seleccionar Plataformas
- Activa/desactiva las plataformas que necesitas:
  - 📱 Android
  - 🍎 iOS
  - 🌐 Web
  - 🪟 Windows
  - 🍏 macOS

### 3️⃣ Elegir Template (Opcional)
- Selecciona de **14 templates** disponibles:
  - Por defecto
  - Material Design
  - iOS Rounded
  - Android Adaptive
  - Tema Oscuro
  - Marca Corporativa
  - **Web/PWA** (nuevo)
  - **Web Transparente** (nuevo)
  - **Windows Metro** (nuevo)
  - **macOS Big Sur** (nuevo)
  - **Gradient Ready** (nuevo)
  - **Minimalista** (nuevo)
  - **Gaming** (nuevo)
  - **Red Social** (nuevo)

### 4️⃣ Configurar Manualmente (Opcional)
- **Color de fondo**: Personaliza o usa transparente
- **Escalas**: Ajusta el tamaño del logo en cada plataforma

### 5️⃣ Vista Previa
- Haz clic en **"👁️ VISTA PREVIA"**
- Revisa cómo quedarán tus iconos
- Ajusta configuración si es necesario

### 6️⃣ Generar
- Haz clic en **"🚀 GENERAR"**
- Se crearán **50+ archivos** automáticamente
- Se incluye `flutter_launcher_icons.yaml`

### 7️⃣ Copiar a Proyecto Flutter (Opcional)
1. Selecciona tu proyecto Flutter en "6. Proyecto Flutter"
2. Haz clic en **"📋 COPIAR A FLUTTER"**
3. Los iconos se copiarán automáticamente a cada carpeta de plataforma

---

## 📁 Estructura de Salida

```
output/
├── flutter_launcher_icons.yaml     # Configuración para flutter_launcher_icons
├── android/
│   ├── mipmap-mdpi/ic_launcher.png (48x48)
│   ├── mipmap-hdpi/ic_launcher.png (72x72)
│   ├── mipmap-xhdpi/ic_launcher.png (96x96)
│   ├── mipmap-xxhdpi/ic_launcher.png (144x144)
│   ├── mipmap-xxxhdpi/ic_launcher.png (192x192)
│   ├── ic_launcher_foreground.png (432x432)
│   └── ic_launcher_1024x1024.png
├── ios/
│   └── AppIcon.appiconset/
│       ├── Contents.json
│       ├── Icon-App-20x20@1x.png ... @3x.png
│       ├── Icon-App-29x29@1x.png ... @3x.png
│       ├── Icon-App-40x40@1x.png ... @3x.png
│       ├── Icon-App-60x60@2x.png ... @3x.png
│       ├── Icon-App-76x76@1x.png ... @2x.png
│       ├── Icon-App-83.5x83.5@2x.png
│       └── Icon-App-1024x1024@1x.png
├── web/
│   ├── favicon.ico                   # Multi-resolución (16,32,48)
│   ├── manifest.json                 # Para PWA
│   └── icon-72x72.png ... 512x512    # 8 tamaños para PWA
├── windows/
│   ├── app_icon.ico                  # Multi-resolución
│   └── app_icon_16.png ... 256.png   # Iconos individuales
└── macos/
    └── Runner/Assets.xcassets/AppIcon.appiconset/
        ├── Contents.json
        └── app_icon_16x16.png ... 512x512@2x.png
```

**Total: 50+ archivos generados automáticamente!**

---

## 🔧 Uso con flutter_launcher_icons

### Opción 1: Automático (Recomendado)
1. Selecciona tu proyecto Flutter en la aplicación
2. Genera los iconos
3. Haz clic en "📋 COPIAR A FLUTTER"
4. ¡Listo! Los iconos están en tu proyecto

### Opción 2: Manual
1. Copia la carpeta `output/` a tu proyecto
2. Copia `flutter_launcher_icons.yaml` a la raíz de tu proyecto
3. Asegúrate de tener `flutter_launcher_icons` en tu `pubspec.yaml`:
   ```yaml
   dev_dependencies:
     flutter_launcher_icons: ^0.13.1
   ```
4. Ejecuta:
   ```bash
   flutter pub run flutter_launcher_icons
   ```

---

## 🎨 Templates Disponibles

| Template | Descripción | Uso Ideal |
|----------|-------------|-----------|
| **Por defecto** | Configuración estándar | Proyectos generales |
| **Material Design** | Optimizado Android | Apps Android nativas |
| **iOS Rounded** | Iconos redondeados | Apps iOS exclusivas |
| **Android Adaptive** | Fondo transparente | Android 8+ adaptive icons |
| **Tema Oscuro** | Fondo oscuro | Logos claros |
| **Marca Corporativa** | Márgenes amplios | Logos con texto |
| **Web/PWA** | Optimizado web | Aplicaciones web/PWA |
| **Web Transparente** | Sin fondo | Favicons y PWA |
| **Windows Metro** | Estilo Windows 10/11 | Apps Windows Modern UI |
| **macOS Big Sur** | Esquinas redondeadas | Apps macOS App Store |
| **Gradient Ready** | Logo grande | Aplicar gradientes después |
| **Minimalista** | Márgenes extra | Diseño minimalista |
| **Gaming** | Estilo gaming | Apps/juegos |
| **Red Social** | Estilo Instagram/TikTok | Apps sociales |

---

## ⌨️ Atajos de Teclado

- **Ctrl+O**: Abrir imagen
- **Menú Archivo**: Acceso a archivos recientes
- **Menú Flutter**: Integración con proyecto Flutter

---

## 📊 Resumen por Fase

### Fase 3 ✅ (Actual)
- **5 Plataformas**: Android, iOS, Web, Windows, macOS
- **50+ Archivos** generados automáticamente
- **YAML automático** para flutter_launcher_icons
- **Copia automática** al proyecto Flutter
- **14 Templates** predefinidos
- Detección de Flutter instalado

### Fase 2 ✅ 
- Preview visual en tiempo real
- Configuración persistente (JSON)
- 6 Templates básicos
- Historial de archivos recientes
- Interfaz mejorada

### Fase 1 ✅
- Android + iOS completos
- 23 archivos automáticos
- Interfaz gráfica base
- Escalado ajustable

---

## 🔧 Requisitos

### Para Usar el Ejecutable
- Windows 10/11
- No requiere Python ni dependencias

### Para Desarrollo
- Python 3.8+
- Pillow
- PyYAML
- PyInstaller

---

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verifica Windows 10/11
- Ejecuta como Administrador si es necesario

### Error al generar iconos
- Verifica que la imagen no esté corrupta
- Asegúrate de tener permisos de escritura
- Usa formato PNG para mejor compatibilidad

### Flutter no detectado
- Asegúrate de que Flutter esté en el PATH
- Menú "Flutter" → "Verificar instalación Flutter"

### Copia a proyecto falla
- Verifica que sea un proyecto Flutter válido (debe tener pubspec.yaml)
- Asegúrate de tener permisos de escritura en el proyecto

---

## 📝 Configuración Persistente

La aplicación guarda automáticamente en:
- Windows: `%APPDATA%\FlutterIconGenerator\config.json`

Incluye:
- Últimas rutas utilizadas
- Configuración de plataformas
- Escalas y colores
- Historial de archivos

---

## 📈 Roadmap Futuro

- [ ] Soporte para Linux
- [ ] Editor visual de iconos integrado
- [ ] Más formatos de salida (SVG, WebP)
- [ ] Compresión automática de imágenes
- [ ] Batch processing (múltiples iconos)
- [ ] Integración CI/CD

---

## 🤝 Contribuir

Las contribuciones son bienvenidas:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - Libre para usar y modificar

---

**Hecho con ❤️ para la comunidad Flutter**

**Versión Actual**: v3.0 - Fase 3 Multiplataforma

---

## 📞 Soporte

¿Tienes problemas o sugerencias?
- Revisa el log de progreso en la aplicación
- Verifica que cumples con los requisitos mínimos
- Consulta la sección de Solución de Problemas

¡Gracias por usar Flutter Icon Generator! 🚀
