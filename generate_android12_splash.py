from PIL import Image

# --- CONFIGURACION ---
input_path = "trivia_1024x1024.png"  # Asegúrate de que esta imagen exista
output_prefix = "android12_splash_"

# Cargar imagen original
try:
    original_img = Image.open(input_path)
    print(f"Imagen cargada: {input_path} ({original_img.width}x{original_img.height})")
except FileNotFoundError:
    print(f"ERROR: No se encontró el archivo '{input_path}'.")
    exit()

def create_centered_image(canvas_size, content_max_size, output_filename):
    """
    Crea una imagen con fondo transparente del tamaño `canvas_size`,
    redimensionando la imagen original para que quepa dentro de `content_max_size` (círculo seguro),
    manteniendo el aspecto y centrándola.
    """
    # Crear lienzo transparente
    canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))
    
    # Calcular nueva escala manteniendo aspect ratio
    # Queremos que la dimensión más grande de la imagen sea igual al tamaño seguro (o un poco menos si prefieres margen)
    # El prompt dice "fit within a circle <diameter>", así que usaremos el diámetro como límite máximo.
    
    width_ratio = content_max_size[0] / original_img.width
    height_ratio = content_max_size[1] / original_img.height
    scale_factor = min(width_ratio, height_ratio, 1.0)
    
    new_width = int(original_img.width * scale_factor)
    new_height = int(original_img.height * scale_factor)
    
    # Redimensionar con alta calidad
    resized_img = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Calcular posición para centrar
    pos_x = (canvas_size[0] - new_width) // 2
    pos_y = (canvas_size[1] - new_height) // 2
    
    # Pegar
    canvas.paste(resized_img, (pos_x, pos_y))
    
    # Guardar
    canvas.save(output_filename)
    print(f"Generado: {output_filename} (Canvas: {canvas_size}, Contenido ajustado a: {new_width}x{new_height})")

# 1. App icon without an icon background
# Canvas: 1152x1152, Safe Zone (Circle Diameter): 768
print("--- Generando Icono (Sin Fondo) ---")
create_centered_image(
    canvas_size=(1152, 1152),
    content_max_size=(768, 768),
    output_filename=f"{output_prefix}icon_no_bg_1152.png"
)

# 2. App icon with an icon background
# Canvas: 960x960, Safe Zone (Circle Diameter): 640
print("--- Generando Icono (Con Fondo) ---")
create_centered_image(
    canvas_size=(960, 960),
    content_max_size=(640, 640), 
    output_filename=f"{output_prefix}icon_with_bg_960.png"
)

# 3. Branding parameter
# The branding image dimensions must be 800x320 px.
print("--- Generando Branding Image ---")
# Para branding, el canvas es 800x320. Ajustamos la imagen para que quepa completa dentro de ese rectángulo.
create_centered_image(
    canvas_size=(800, 320),
    content_max_size=(800, 320),
    output_filename=f"{output_prefix}branding_800x320.png"
)

print("--- Proceso Finalizado ---")
