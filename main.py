import numpy as np
from PIL import Image, ImageOps

# Cargar la imagen original
# ASEGURATE QUE ESTA RUTA SEA CORRECTA A TU ARCHIVO LOCAL
input_path = "LOGO ESCUELA POSTGRADO UNAP SIN LETRA 2.png"
original_img = Image.open(input_path)

# --- CONFIGURACIÓN DE COLORES ---
unap_bg_color = "#FFFFFF"  # Fondo blanco para rellenar el cuadrado

# --- GENERAR ICONO MAESTRO GRANDE (1024x1024) ---
master_size = (1024, 1024)
master_icon = Image.new("RGB", master_size, unap_bg_color)

# CAMBIO AQUÍ: Aumentamos la escala al 95% del alto total.
# Esto deja un margen mínimo para que no se corte el texto en las esquinas.
target_height = int(master_size[1] * 0.95)
aspect_ratio = original_img.width / original_img.height
target_width = int(target_height * aspect_ratio)

# Redimensionar con alta calidad
resized_img = original_img.resize(
    (target_width, target_height), Image.Resampling.LANCZOS
)

# Pegar en el centro
pos_x = (master_size[0] - target_width) // 2
pos_y = (master_size[1] - target_height) // 2
master_icon.paste(resized_img, (pos_x, pos_y))

master_filename = "icon-1024x1024.png"
master_icon.save(master_filename)

# --- GENERAR FOREGROUND ADAPTATIVO GRANDE (432x432) ---
adaptive_size = (432, 432)
adaptive_icon = Image.new(
    "RGBA", adaptive_size, (255, 255, 255, 0)
)  # Fondo transparente

# CAMBIO AQUÍ: Aumentamos la escala al 75% para Android.
# En Android el recorte es circular, así que podemos arriesgar más.
target_h_adaptive = int(adaptive_size[1] * 0.75)
target_w_adaptive = int(target_h_adaptive * aspect_ratio)

resized_adaptive = original_img.resize(
    (target_w_adaptive, target_h_adaptive), Image.Resampling.LANCZOS
)

pos_x_a = (adaptive_size[0] - target_w_adaptive) // 2
pos_y_a = (adaptive_size[1] - target_h_adaptive) // 2

adaptive_icon.paste(resized_adaptive, (pos_x_a, pos_y_a))

adaptive_filename = "icon-foreground-432x432.png"
adaptive_icon.save(adaptive_filename)

print(
    f"Nuevos archivos generados (más grandes): {master_filename}, {adaptive_filename}"
)
print(
    "Reemplaza los archivos en assets/images/ y vuelve a ejecutar el comando de flutter."
)
