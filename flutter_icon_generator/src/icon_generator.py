"""
Módulo de generación de iconos para Flutter
Soporta Android e iOS con todos los tamaños necesarios
"""

import os
from PIL import Image
from typing import Tuple, Optional

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
    
    def generate_all(
        self,
        input_path: str,
        bg_color: Optional[str] = None,
        android_scale: float = 0.8,
        ios_scale: float = 0.85
    ) -> dict:
        """
        Genera todos los iconos para Android e iOS
        
        Args:
            input_path: Ruta a la imagen origen
            bg_color: Color de fondo en hex (opcional)
            android_scale: Factor de escala para Android
            ios_scale: Factor de escala para iOS
            
        Returns:
            Diccionario con rutas de archivos generados
        """
        # Cargar imagen
        source_img = Image.open(input_path).convert("RGBA")
        
        # Generar iconos
        android_files = self.generate_android_icons(source_img, bg_color, android_scale)
        ios_files = self.generate_ios_icons(source_img, ios_scale)
        
        return {
            'android': android_files,
            'ios': ios_files,
            'total': len(android_files) + len(ios_files)
        }
