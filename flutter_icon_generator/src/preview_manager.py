"""
Sistema de preview visual para Flutter Icon Generator
Genera vistas previas de cómo quedarán los iconos
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk, ImageFont
import io
import base64

class IconPreviewGenerator:
    """Generador de vistas previas de iconos"""
    
    def __init__(self):
        self.preview_cache = {}
    
    def generate_android_preview(self, source_img: Image.Image, bg_color: str = "#FFFFFF", 
                                scale: float = 0.8, size: int = 192) -> Image.Image:
        """Genera preview de icono Android"""
        # Crear canvas cuadrado
        canvas = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        
        # Calcular tamaño del contenido
        content_size = int(size * scale)
        
        # Redimensionar imagen manteniendo aspect ratio
        aspect = source_img.width / source_img.height
        if aspect >= 1:
            new_width = content_size
            new_height = int(content_size / aspect)
        else:
            new_height = content_size
            new_width = int(content_size * aspect)
        
        resized = source_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calcular posición centrada
        x = (size - new_width) // 2
        y = (size - new_height) // 2
        
        # Si hay color de fondo, dibujar fondo
        if bg_color and bg_color != "":
            rgb = self.hex_to_rgb(bg_color)
            # Fondo cuadrado con esquinas redondeadas (simula icono Android)
            mask = Image.new("L", (size, size), 0)
            draw = ImageDraw.Draw(mask)
            radius = size // 5  # Esquinas redondeadas
            draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
            
            bg = Image.new("RGBA", (size, size), rgb + (255,))
            canvas.paste(bg, (0, 0), mask)
        
        # Pegar imagen
        if resized.mode == 'RGBA':
            canvas.paste(resized, (x, y), resized)
        else:
            canvas.paste(resized, (x, y))
        
        return canvas
    
    def generate_ios_preview(self, source_img: Image.Image, bg_color: str = "#FFFFFF",
                            scale: float = 0.85, size: int = 180) -> Image.Image:
        """Genera preview de icono iOS"""
        # Crear canvas cuadrado
        canvas = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        
        # Calcular tamaño del contenido
        content_size = int(size * scale)
        
        # Redimensionar imagen manteniendo aspect ratio
        aspect = source_img.width / source_img.height
        if aspect >= 1:
            new_width = content_size
            new_height = int(content_size / aspect)
        else:
            new_height = content_size
            new_width = int(content_size * aspect)
        
        resized = source_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calcular posición centrada
        x = (size - new_width) // 2
        y = (size - new_height) // 2
        
        # Fondo con esquinas redondeadas (iOS superellipse)
        if bg_color and bg_color != "":
            rgb = self.hex_to_rgb(bg_color)
            mask = self.create_ios_mask(size)
            bg = Image.new("RGBA", (size, size), rgb + (255,))
            canvas.paste(bg, (0, 0), mask)
        
        # Pegar imagen
        if resized.mode == 'RGBA':
            canvas.paste(resized, (x, y), resized)
        else:
            canvas.paste(resized, (x, y))
        
        return canvas
    
    def create_ios_mask(self, size: int) -> Image.Image:
        """Crea una máscara de superellipse para iOS"""
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        
        # Radio de esquina para iOS (aproximadamente 22% del tamaño)
        radius = int(size * 0.223)
        
        # Dibujar rectángulo redondeado (aproximación del superellipse)
        draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=255)
        
        return mask
    
    def generate_adaptive_preview(self, source_img: Image.Image, scale: float = 0.75, 
                                  size: int = 192) -> Image.Image:
        """Genera preview de icono adaptativo (foreground)"""
        canvas = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        
        # Calcular tamaño del contenido
        content_size = int(size * scale)
        
        # Redimensionar
        aspect = source_img.width / source_img.height
        if aspect >= 1:
            new_width = content_size
            new_height = int(content_size / aspect)
        else:
            new_height = content_size
            new_width = int(content_size * aspect)
        
        resized = source_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Centrar
        x = (size - new_width) // 2
        y = (size - new_height) // 2
        
        # Pegar con transparencia
        if resized.mode == 'RGBA':
            canvas.paste(resized, (x, y), resized)
        else:
            canvas.paste(resized, (x, y))
        
        return canvas
    
    def generate_comparison_preview(self, source_img: Image.Image, bg_color: str = "#FFFFFF",
                                   android_scale: float = 0.8, ios_scale: float = 0.85,
                                   width: int = 600) -> Image.Image:
        """Genera una imagen comparativa de Android vs iOS"""
        # Tamaño de cada preview
        preview_size = 180
        padding = 40
        
        # Crear canvas
        canvas_width = width
        canvas_height = preview_size + padding * 3 + 60  # Espacio para labels
        canvas = Image.new("RGBA", (canvas_width, canvas_height), (245, 245, 245, 255))
        
        # Generar previews
        android_icon = self.generate_android_preview(source_img, bg_color, android_scale, preview_size)
        ios_icon = self.generate_ios_preview(source_img, bg_color, ios_scale, preview_size)
        adaptive_icon = self.generate_adaptive_preview(source_img, android_scale, preview_size)
        
        # Calcular posiciones
        total_width = preview_size * 3 + padding * 2
        start_x = (canvas_width - total_width) // 2
        
        # Pegar previews
        canvas.paste(android_icon, (start_x, padding), android_icon)
        canvas.paste(ios_icon, (start_x + preview_size + padding, padding), ios_icon)
        canvas.paste(adaptive_icon, (start_x + (preview_size + padding) * 2, padding), adaptive_icon)
        
        # Agregar texto (si es posible)
        try:
            draw = ImageDraw.Draw(canvas)
            # Intentar usar fuente por defecto
            try:
                font = ImageFont.truetype("arial.ttf", 14)
            except:
                font = ImageFont.load_default()
            
            # Labels
            labels = ["Android", "iOS", "Adaptive"]
            for i, label in enumerate(labels):
                x = start_x + i * (preview_size + padding) + preview_size // 2
                y = padding + preview_size + 10
                bbox = draw.textbbox((0, 0), label, font=font)
                text_width = bbox[2] - bbox[0]
                draw.text((x - text_width // 2, y), label, fill=(100, 100, 100, 255), font=font)
        except:
            pass
        
        return canvas
    
    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Convierte hex a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


class PreviewWindow:
    """Ventana de preview flotante"""
    
    def __init__(self, parent, source_img: Image.Image, bg_color: str = "#FFFFFF",
                 android_scale: float = 0.8, ios_scale: float = 0.85):
        self.window = tk.Toplevel(parent)
        self.window.title("Vista Previa de Iconos")
        self.window.geometry("650x500")
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame, 
            text="Así se verán tus iconos",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=(0, 20))
        
        # Generar preview
        generator = IconPreviewGenerator()
        preview_img = generator.generate_comparison_preview(
            source_img, bg_color, android_scale, ios_scale
        )
        
        # Redimensionar para mostrar
        max_width = 550
        ratio = max_width / preview_img.width
        new_size = (max_width, int(preview_img.height * ratio))
        preview_img = preview_img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convertir a PhotoImage
        self.preview_tk = ImageTk.PhotoImage(preview_img)
        
        # Mostrar
        preview_label = ttk.Label(main_frame, image=self.preview_tk)
        preview_label.pack(pady=10)
        
        # Información
        info_frame = ttk.LabelFrame(main_frame, text="Detalles", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text=f"Color de fondo: {bg_color if bg_color else 'Transparente'}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Escala Android: {android_scale:.0%}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Escala iOS: {ios_scale:.0%}").pack(anchor=tk.W)
        
        # Botón cerrar
        ttk.Button(
            main_frame, 
            text="Cerrar", 
            command=self.window.destroy
        ).pack(pady=10)
        
        # Centrar ventana
        self.window.transient(parent)
        self.window.grab_set()
        self.window.update_idletasks()
        
        x = parent.winfo_x() + (parent.winfo_width() - self.window.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.window.winfo_height()) // 2
        self.window.geometry(f"+{x}+{y}")
