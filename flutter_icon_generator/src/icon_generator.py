"""
Módulo de generación de iconos para Flutter
Soporta Android, iOS, Web, Windows y macOS con todos los tamaños necesarios
Fase 3: Multiplataforma completa + Integración flutter_launcher_icons
"""

import os
import json
import yaml
from PIL import Image
from typing import Tuple, Optional, List, Dict

class IconGenerator:
    """Generador de iconos multiplataforma para Flutter"""
    
    # Configuración de tamaños para Android
    ANDROID_SIZES = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192,
    }
    
    # Configuración de tamaños para iOS
    IOS_SIZES = [
        (20, 1), (20, 2), (20, 3),
        (29, 1), (29, 2), (29, 3),
        (40, 1), (40, 2), (40, 3),
        (60, 2), (60, 3),
        (76, 1), (76, 2),
        (83.5, 2),
        (1024, 1),  # App Store
    ]
    
    # Configuración de tamaños para Web (PWA)
    WEB_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]
    
    # Configuración de tamaños para Windows
    WINDOWS_SIZES = [16, 32, 48, 256]
    
    # Configuración de tamaños para macOS
    MACOS_SIZES = [
        (16, 1), (16, 2),
        (32, 1), (32, 2),
        (128, 1), (128, 2),
        (256, 1), (256, 2),
        (512, 1), (512, 2),
    ]
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convierte color hex a RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_centered_image(
        self,
        source_img: Image.Image,
        canvas_size: Tuple[int, int],
        content_max_size: Tuple[int, int],
        bg_color: Tuple[int, int, int, int] = (255, 255, 255, 0)
    ) -> Image.Image:
        """
        Crea una imagen centrada en un canvas del tamaño especificado
        
        Args:
            source_img: Imagen origen
            canvas_size: Tamaño del canvas (ancho, alto)
            content_max_size: Tamaño máximo del contenido
            bg_color: Color de fondo (RGBA)
        """
        # Crear canvas transparente
        canvas = Image.new("RGBA", canvas_size, bg_color)
        
        # Calcular escala manteniendo aspect ratio
        width_ratio = content_max_size[0] / source_img.width
        height_ratio = content_max_size[1] / source_img.height
        scale_factor = min(width_ratio, height_ratio, 1.0)
        
        new_width = int(source_img.width * scale_factor)
        new_height = int(source_img.height * scale_factor)
        
        # Redimensionar con alta calidad
        resized_img = source_img.resize(
            (new_width, new_height), 
            Image.Resampling.LANCZOS
        )
        
        # Calcular posición centrada
        pos_x = (canvas_size[0] - new_width) // 2
        pos_y = (canvas_size[1] - new_height) // 2
        
        # Pegar la imagen
        if resized_img.mode == 'RGBA':
            canvas.paste(resized_img, (pos_x, pos_y), mask=resized_img)
        else:
            canvas.paste(resized_img, (pos_x, pos_y))
            
        return canvas
    
    def generate_android_icons(
        self,
        source_img: Image.Image,
        bg_color: Optional[str] = None,
        scale_factor: float = 0.8
    ) -> list:
        """
        Genera todos los iconos para Android
        
        Args:
            source_img: Imagen origen (debe ser RGBA)
            bg_color: Color de fondo en hex (opcional)
            scale_factor: Factor de escala del contenido (0.0 - 1.0)
            
        Returns:
            Lista de rutas de archivos generados
        """
        generated_files = []
        android_dir = os.path.join(self.output_dir, 'android')
        
        # Crear directorios
        for folder in self.ANDROID_SIZES.keys():
            os.makedirs(os.path.join(android_dir, folder), exist_ok=True)
        
        # Generar iconos launcher
        for folder, size in self.ANDROID_SIZES.items():
            # Icono con fondo
            if bg_color:
                rgb = self.hex_to_rgb(bg_color)
                bg = rgb + (255,)
                icon = self.create_centered_image(
                    source_img,
                    (size, size),
                    (int(size * scale_factor), int(size * scale_factor)),
                    bg
                )
                # Convertir a RGB si no tiene transparencia
                if icon.mode == 'RGBA':
                    background = Image.new('RGB', icon.size, rgb)
                    background.paste(icon, mask=icon.split()[-1])
                    icon = background
            else:
                icon = self.create_centered_image(
                    source_img,
                    (size, size),
                    (int(size * scale_factor), int(size * scale_factor))
                )
            
            output_path = os.path.join(android_dir, folder, 'ic_launcher.png')
            icon.save(output_path, 'PNG')
            generated_files.append(output_path)
        
        # Generar foreground adaptativo (432x432)
        adaptive_size = 432
        adaptive_icon = self.create_centered_image(
            source_img,
            (adaptive_size, adaptive_size),
            (int(adaptive_size * 0.75), int(adaptive_size * 0.75))
        )
        adaptive_path = os.path.join(android_dir, 'ic_launcher_foreground.png')
        adaptive_icon.save(adaptive_path, 'PNG')
        generated_files.append(adaptive_path)
        
        # Generar icono maestro 1024x1024
        master_size = 1024
        if bg_color:
            rgb = self.hex_to_rgb(bg_color)
            bg = rgb + (255,)
            master_icon = self.create_centered_image(
                source_img,
                (master_size, master_size),
                (int(master_size * 0.9), int(master_size * 0.9)),
                bg
            )
            # Convertir a RGB
            if master_icon.mode == 'RGBA':
                background = Image.new('RGB', master_icon.size, rgb)
                background.paste(master_icon, mask=master_icon.split()[-1])
                master_icon = background
        else:
            master_icon = self.create_centered_image(
                source_img,
                (master_size, master_size),
                (int(master_size * 0.9), int(master_size * 0.9))
            )
        
        master_path = os.path.join(android_dir, 'ic_launcher_1024x1024.png')
        master_icon.save(master_path, 'PNG')
        generated_files.append(master_path)
        
        return generated_files
    
    def generate_ios_icons(
        self,
        source_img: Image.Image,
        scale_factor: float = 0.85
    ) -> list:
        """
        Genera todos los iconos para iOS
        
        Args:
            source_img: Imagen origen (debe ser RGBA)
            scale_factor: Factor de escala del contenido
            
        Returns:
            Lista de rutas de archivos generados
        """
        generated_files = []
        ios_dir = os.path.join(self.output_dir, 'ios', 'AppIcon.appiconset')
        os.makedirs(ios_dir, exist_ok=True)
        
        # Generar Contents.json
        contents = self._generate_ios_contents_json()
        contents_path = os.path.join(ios_dir, 'Contents.json')
        with open(contents_path, 'w') as f:
            import json
            json.dump(contents, f, indent=2)
        generated_files.append(contents_path)
        
        # Generar iconos
        for size, scale in self.IOS_SIZES:
            actual_size = int(size * scale)
            filename = f"Icon-App-{size}x{size}@{scale}x.png"
            
            icon = self.create_centered_image(
                source_img,
                (actual_size, actual_size),
                (int(actual_size * scale_factor), int(actual_size * scale_factor))
            )
            
            output_path = os.path.join(ios_dir, filename)
            
            # Convertir a RGB para iOS (sin transparencia)
            if icon.mode == 'RGBA':
                background = Image.new('RGB', icon.size, (255, 255, 255))
                background.paste(icon, mask=icon.split()[-1])
                icon = background
            
            icon.save(output_path, 'PNG')
            generated_files.append(output_path)
        
        return generated_files
    
    def _generate_ios_contents_json(self) -> dict:
        """Genera el archivo Contents.json para iOS"""
        images = []
        
        # iPhone
        images.extend([
            {"size": "20x20", "idiom": "iphone", "filename": "Icon-App-20x20@2x.png", "scale": "2x"},
            {"size": "20x20", "idiom": "iphone", "filename": "Icon-App-20x20@3x.png", "scale": "3x"},
            {"size": "29x29", "idiom": "iphone", "filename": "Icon-App-29x29@2x.png", "scale": "2x"},
            {"size": "29x29", "idiom": "iphone", "filename": "Icon-App-29x29@3x.png", "scale": "3x"},
            {"size": "40x40", "idiom": "iphone", "filename": "Icon-App-40x40@2x.png", "scale": "2x"},
            {"size": "40x40", "idiom": "iphone", "filename": "Icon-App-40x40@3x.png", "scale": "3x"},
            {"size": "60x60", "idiom": "iphone", "filename": "Icon-App-60x60@2x.png", "scale": "2x"},
            {"size": "60x60", "idiom": "iphone", "filename": "Icon-App-60x60@3x.png", "scale": "3x"},
        ])
        
        # iPad
        images.extend([
            {"size": "20x20", "idiom": "ipad", "filename": "Icon-App-20x20@1x.png", "scale": "1x"},
            {"size": "20x20", "idiom": "ipad", "filename": "Icon-App-20x20@2x.png", "scale": "2x"},
            {"size": "29x29", "idiom": "ipad", "filename": "Icon-App-29x29@1x.png", "scale": "1x"},
            {"size": "29x29", "idiom": "ipad", "filename": "Icon-App-29x29@2x.png", "scale": "2x"},
            {"size": "40x40", "idiom": "ipad", "filename": "Icon-App-40x40@1x.png", "scale": "1x"},
            {"size": "40x40", "idiom": "ipad", "filename": "Icon-App-40x40@2x.png", "scale": "2x"},
            {"size": "76x76", "idiom": "ipad", "filename": "Icon-App-76x76@1x.png", "scale": "1x"},
            {"size": "76x76", "idiom": "ipad", "filename": "Icon-App-76x76@2x.png", "scale": "2x"},
            {"size": "83.5x83.5", "idiom": "ipad", "filename": "Icon-App-83.5x83.5@2x.png", "scale": "2x"},
        ])
        
        # App Store
        images.append({
            "size": "1024x1024",
            "idiom": "ios-marketing",
            "filename": "Icon-App-1024x1024@1x.png",
            "scale": "1x"
        })
        
        return {
            "images": images,
            "info": {
                "author": "xcode",
                "version": 1
            }
        }
    
    def generate_web_icons(
        self,
        source_img: Image.Image,
        bg_color: Optional[str] = None,
        scale_factor: float = 0.85
    ) -> list:
        """
        Genera todos los iconos para Web/PWA
        
        Args:
            source_img: Imagen origen (debe ser RGBA)
            bg_color: Color de fondo en hex (opcional)
            scale_factor: Factor de escala del contenido
            
        Returns:
            Lista de rutas de archivos generados
        """
        generated_files = []
        web_dir = os.path.join(self.output_dir, 'web')
        os.makedirs(web_dir, exist_ok=True)
        
        # Generar favicon.ico (multi-resolución)
        favicon_images = []
        for size in [16, 32, 48]:
            icon = self.create_centered_image(
                source_img,
                (size, size),
                (int(size * scale_factor), int(size * scale_factor)),
                self._get_bg_color_rgba(bg_color)
            )
            if icon.mode == 'RGBA':
                icon = icon.convert('RGB')
            favicon_images.append(icon)
        
        # Guardar favicon.ico
        favicon_path = os.path.join(web_dir, 'favicon.ico')
        favicon_images[0].save(
            favicon_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in favicon_images]
        )
        generated_files.append(favicon_path)
        
        # Generar iconos PWA
        for size in self.WEB_SIZES:
            icon = self.create_centered_image(
                source_img,
                (size, size),
                (int(size * scale_factor), int(size * scale_factor)),
                self._get_bg_color_rgba(bg_color)
            )
            
            output_path = os.path.join(web_dir, f'icon-{size}x{size}.png')
            icon.save(output_path, 'PNG')
            generated_files.append(output_path)
        
        # Generar manifest.json para PWA
        manifest = self._generate_web_manifest(bg_color)
        manifest_path = os.path.join(web_dir, 'manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        generated_files.append(manifest_path)
        
        return generated_files
    
    def _generate_web_manifest(self, theme_color: Optional[str] = None) -> dict:
        """Genera el manifest.json para PWA"""
        theme = theme_color if theme_color else "#FFFFFF"
        return {
            "name": "Flutter App",
            "short_name": "Flutter App",
            "start_url": ".",
            "display": "standalone",
            "background_color": theme,
            "theme_color": theme,
            "icons": [
                {
                    "src": f"icon-{size}x{size}.png",
                    "sizes": f"{size}x{size}",
                    "type": "image/png"
                }
                for size in self.WEB_SIZES
            ]
        }
    
    def generate_windows_icons(
        self,
        source_img: Image.Image,
        bg_color: Optional[str] = None,
        scale_factor: float = 0.85
    ) -> list:
        """
        Genera todos los iconos para Windows
        
        Args:
            source_img: Imagen origen (debe ser RGBA)
            bg_color: Color de fondo en hex (opcional)
            scale_factor: Factor de escala del contenido
            
        Returns:
            Lista de rutas de archivos generados
        """
        generated_files = []
        windows_dir = os.path.join(self.output_dir, 'windows')
        os.makedirs(windows_dir, exist_ok=True)
        
        # Generar iconos individuales
        icons_for_ico = []
        for size in self.WINDOWS_SIZES:
            icon = self.create_centered_image(
                source_img,
                (size, size),
                (int(size * scale_factor), int(size * scale_factor)),
                self._get_bg_color_rgba(bg_color)
            )
            
            # Guardar PNG individual
            png_path = os.path.join(windows_dir, f'app_icon_{size}.png')
            if icon.mode == 'RGBA':
                icon_rgb = Image.new('RGB', icon.size, self._get_bg_color_rgb(bg_color) or (255, 255, 255))
                icon_rgb.paste(icon, mask=icon.split()[-1])
                icon_rgb.save(png_path, 'PNG')
            else:
                icon.save(png_path, 'PNG')
            generated_files.append(png_path)
            
            icons_for_ico.append(icon.convert('RGB') if icon.mode == 'RGBA' else icon)
        
        # Generar app_icon.ico (multi-resolución)
        ico_path = os.path.join(windows_dir, 'app_icon.ico')
        icons_for_ico[0].save(
            ico_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in icons_for_ico]
        )
        generated_files.append(ico_path)
        
        return generated_files
    
    def generate_macos_icons(
        self,
        source_img: Image.Image,
        bg_color: Optional[str] = None,
        scale_factor: float = 0.85
    ) -> list:
        """
        Genera todos los iconos para macOS
        
        Args:
            source_img: Imagen origen (debe ser RGBA)
            bg_color: Color de fondo en hex (opcional)
            scale_factor: Factor de escala del contenido
            
        Returns:
            Lista de rutas de archivos generados
        """
        generated_files = []
        macos_dir = os.path.join(self.output_dir, 'macos', 'Runner', 'Assets.xcassets', 'AppIcon.appiconset')
        os.makedirs(macos_dir, exist_ok=True)
        
        # Generar Contents.json
        contents = self._generate_macos_contents_json()
        contents_path = os.path.join(macos_dir, 'Contents.json')
        with open(contents_path, 'w') as f:
            json.dump(contents, f, indent=2)
        generated_files.append(contents_path)
        
        # Generar iconos
        for size, scale in self.MACOS_SIZES:
            actual_size = int(size * scale)
            filename = f'app_icon_{size}x{size}{"@2x" if scale == 2 else ""}.png'
            
            icon = self.create_centered_image(
                source_img,
                (actual_size, actual_size),
                (int(actual_size * scale_factor), int(actual_size * scale_factor)),
                self._get_bg_color_rgba(bg_color)
            )
            
            output_path = os.path.join(macos_dir, filename)
            
            # Convertir a RGB para macOS
            if icon.mode == 'RGBA':
                bg_rgb = self._get_bg_color_rgb(bg_color) or (255, 255, 255)
                background = Image.new('RGB', icon.size, bg_rgb)
                background.paste(icon, mask=icon.split()[-1])
                icon = background
            
            icon.save(output_path, 'PNG')
            generated_files.append(output_path)
        
        return generated_files
    
    def _generate_macos_contents_json(self) -> dict:
        """Genera el archivo Contents.json para macOS"""
        images = []
        
        for size, scale in self.MACOS_SIZES:
            filename = f'app_icon_{size}x{size}{"@2x" if scale == 2 else ""}.png'
            images.append({
                "size": f"{size}x{size}",
                "idiom": "mac",
                "filename": filename,
                "scale": f"{scale}x"
            })
        
        return {
            "images": images,
            "info": {
                "author": "xcode",
                "version": 1
            }
        }
    
    def _get_bg_color_rgba(self, bg_color: Optional[str]) -> Tuple[int, int, int, int]:
        """Convierte color hex a RGBA tuple para fondo"""
        if bg_color:
            rgb = self.hex_to_rgb(bg_color)
            return rgb + (255,)
        return (255, 255, 255, 0)
    
    def _get_bg_color_rgb(self, bg_color: Optional[str]) -> Optional[Tuple[int, int, int]]:
        """Convierte color hex a RGB tuple"""
        if bg_color:
            return self.hex_to_rgb(bg_color)
        return None
    
    def generate_flutter_launcher_icons_yaml(
        self,
        image_path: str,
        platforms: List[str] = None,
        bg_color: Optional[str] = None
    ) -> str:
        """
        Genera el archivo de configuración flutter_launcher_icons.yaml
        
        Args:
            image_path: Ruta a la imagen maestra (relativa al proyecto Flutter)
            platforms: Lista de plataformas a habilitar
            bg_color: Color de fondo para Android
            
        Returns:
            Contenido del archivo YAML como string
        """
        if platforms is None:
            platforms = ['android', 'ios', 'web', 'windows', 'macos']
        
        config = {
            'flutter_launcher_icons': {
                'android': 'android' in platforms,
                'ios': 'ios' in platforms,
                'web': 'web' in platforms,
                'windows': 'windows' in platforms,
                'macos': 'macos' in platforms,
                'image_path': image_path,
                'adaptive_icon_background': bg_color if bg_color else '#FFFFFF',
                'adaptive_icon_foreground': image_path,
                'min_sdk_android': 21,
                'remove_alpha_ios': True,
            }
        }
        
        return yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    def save_flutter_launcher_icons_yaml(
        self,
        image_path: str,
        platforms: List[str] = None,
        bg_color: Optional[str] = None
    ) -> str:
        """
        Guarda el archivo flutter_launcher_icons.yaml en el directorio de salida
        
        Returns:
            Ruta al archivo generado
        """
        yaml_content = self.generate_flutter_launcher_icons_yaml(image_path, platforms, bg_color)
        yaml_path = os.path.join(self.output_dir, 'flutter_launcher_icons.yaml')
        
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        return yaml_path
    
    def generate_all(
        self,
        input_path: str,
        bg_color: Optional[str] = None,
        android_scale: float = 0.8,
        ios_scale: float = 0.85,
        platforms: List[str] = None
    ) -> dict:
        """
        Genera todos los iconos para las plataformas especificadas
        
        Args:
            input_path: Ruta a la imagen origen
            bg_color: Color de fondo en hex (opcional)
            android_scale: Factor de escala para Android
            ios_scale: Factor de escala para iOS
            platforms: Lista de plataformas ('android', 'ios', 'web', 'windows', 'macos')
                      Si es None, genera para todas
            
        Returns:
            Diccionario con rutas de archivos generados
        """
        if platforms is None:
            platforms = ['android', 'ios', 'web', 'windows', 'macos']
        
        # Cargar imagen
        source_img = Image.open(input_path).convert("RGBA")
        
        results = {
            'android': [],
            'ios': [],
            'web': [],
            'windows': [],
            'macos': [],
            'yaml': None,
            'total': 0
        }
        
        # Generar iconos para cada plataforma
        if 'android' in platforms:
            results['android'] = self.generate_android_icons(source_img, bg_color, android_scale)
            results['total'] += len(results['android'])
        
        if 'ios' in platforms:
            results['ios'] = self.generate_ios_icons(source_img, ios_scale)
            results['total'] += len(results['ios'])
        
        if 'web' in platforms:
            results['web'] = self.generate_web_icons(source_img, bg_color)
            results['total'] += len(results['web'])
        
        if 'windows' in platforms:
            results['windows'] = self.generate_windows_icons(source_img, bg_color)
            results['total'] += len(results['windows'])
        
        if 'macos' in platforms:
            results['macos'] = self.generate_macos_icons(source_img, bg_color)
            results['total'] += len(results['macos'])
        
        # Generar archivo YAML para flutter_launcher_icons
        yaml_path = self.save_flutter_launcher_icons_yaml(
            'assets/icon/icon.png',  # Ruta sugerida en proyecto Flutter
            platforms,
            bg_color
        )
        results['yaml'] = yaml_path
        results['total'] += 1
        
        return results
