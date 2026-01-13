from PIL import Image
import os

# --- CONFIGURACION DE ARCHIVOS ---
robot_path = "trivia_1024x1024.png"  # El Robot
text_path = "trivia_text.png"        # El Texto (Branding)
output_prefix = "android12_splash_"

def create_centered_image(source_img, canvas_size, content_max_size, output_filename):
    """
    Crea una imagen con fondo transparente del tamaño `canvas_size`.
    Centra la `source_img` dentro, asegurando que no exceda `content_max_size`.
    NO estira la imagen si es más pequeña que el hueco (scale_factor min 1.0).
    """
    # 1. Crear lienzo transparente
    canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))
    
    # 2. Calcular escala
    # Usamos min(..., 1.0) para evitar que imágenes pequeñas se pixelen al estirarse
    width_ratio = content_max_size[0] / source_img.width
    height_ratio = content_max_size[1] / source_img.height
    scale_factor = min(width_ratio, height_ratio, 1.0)
    
    new_width = int(source_img.width * scale_factor)
    new_height = int(source_img.height * scale_factor)
    
    # 3. Redimensionar (Downscaling de alta calidad)
    if scale_factor < 1.0:
        resized_img = source_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    else:
        resized_img = source_img # Se mantiene igual si ya era pequeña
    
    # 4. Calcular posición para centrar
    pos_x = (canvas_size[0] - new_width) // 2
    pos_y = (canvas_size[1] - new_height) // 2
    
    # 5. Pegar y Guardar
    canvas.paste(resized_img, (pos_x, pos_y))
    canvas.save(output_filename)
    print(f"✅ Generado: {output_filename}")
    print(f"   Canvas: {canvas_size} | Contenido real: {new_width}x{new_height}")

# --- EJECUCION ---

# 1. PROCESAR EL ROBOT (Icono Central)
if os.path.exists(robot_path):
    print(f"\n--- Procesando Robot: {robot_path} ---")
    robot_img = Image.open(robot_path).convert("RGBA")

    # A. Icono sin fondo (El estándar)
    # Canvas 1152, Zona visible 768
    create_centered_image(
        source_img=robot_img,
        canvas_size=(1152, 1152),
        content_max_size=(768, 768),
        output_filename=f"{output_prefix}icon_no_bg_1152.png"
    )

    # B. Icono con fondo (Opcional)
    # Canvas 960, Zona visible 640
    create_centered_image(
        source_img=robot_img,
        canvas_size=(960, 960),
        content_max_size=(640, 640),
        output_filename=f"{output_prefix}icon_with_bg_960.png"
    )
else:
    print(f"❌ ERROR: No encontré la imagen del robot: {robot_path}")

# 2. PROCESAR EL TEXTO (Branding Inferior)
if os.path.exists(text_path):
    print(f"\n--- Procesando Branding: {text_path} ---")
    text_img = Image.open(text_path).convert("RGBA")

    # C. Branding Image
    # Canvas obligatorio: 800x320.
    # Área segura interna: Usamos 600x200 para dejar aire y que no toque los bordes.
    create_centered_image(
        source_img=text_img,
        canvas_size=(800, 320),
        content_max_size=(600, 200), 
        output_filename=f"{output_prefix}branding_800x320.png"
    )
else:
    print(f"\n⚠️ ALERTA: No encontré '{text_path}'.")
    print("   No se generó la imagen de branding. (Si no la usas, ignora esto).")

print("\n--- Proceso Finalizado ---")