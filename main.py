import numpy as np
from PIL import Image, ImageOps

# Cargar la imagen original
input_path = "LOGO ESCUELA POSTGRADO UNAP SIN LETRA 2.png"
original_img = Image.open(input_path)

# --- CONFIGURACIÓN DE COLORES ---
# Detecté el azul del borde para sugerirtelo como background
unap_blue = "#1B2A50"
unap_bg_color = "#FFFFFF"  # El fondo del jpg es grisaceo/blanco

# --- GENERAR ICONO MAESTRO (1024x1024) ---
# Creamos un lienzo cuadrado blanco (para iOS y general)
master_size = (1024, 1024)
master_icon = Image.new("RGB", master_size, unap_bg_color)

# Redimensionar logo manteniendo aspecto para que quepa bien
# Dejamos un margen del 10% para seguridad en iOS
target_height = int(master_size[1] * 0.90)
aspect_ratio = original_img.width / original_img.height
target_width = int(target_height * aspect_ratio)

resized_img = original_img.resize(
    (target_width, target_height), Image.Resampling.LANCZOS
)

# Pegar en el centro
pos_x = (master_size[0] - target_width) // 2
pos_y = (master_size[1] - target_height) // 2
master_icon.paste(resized_img, (pos_x, pos_y))

master_filename = "icon-1024x1024.png"
master_icon.save(master_filename)

# --- GENERAR FOREGROUND ADAPTATIVO (432x432) ---
# Para Android Adaptive, el logo debe ser más pequeño (aprox 50-60% del lienzo)
# para estar en la "zona segura" (safe zone) que es un círculo central de 66px de radio sobre 108px.
adaptive_size = (432, 432)
adaptive_icon = Image.new(
    "RGBA", adaptive_size, (255, 255, 255, 0)
)  # Fondo transparente

# Calculamos un tamaño seguro (55% del total es seguro para iconos redondos)
target_h_adaptive = int(adaptive_size[1] * 0.55)
target_w_adaptive = int(target_h_adaptive * aspect_ratio)

resized_adaptive = original_img.resize(
    (target_w_adaptive, target_h_adaptive), Image.Resampling.LANCZOS
)

pos_x_a = (adaptive_size[0] - target_w_adaptive) // 2
pos_y_a = (adaptive_size[1] - target_h_adaptive) // 2

adaptive_icon.paste(resized_adaptive, (pos_x_a, pos_y_a))

adaptive_filename = "icon-foreground-432x432.png"
adaptive_icon.save(adaptive_filename)

print(f"Archivos generados: {master_filename}, {adaptive_filename}")
