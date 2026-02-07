"""
Flutter Icon Generator - Interfaz Gráfica Principal
Fase 1: Core funcional
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.icon_generator import IconGenerator

class FlutterIconGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flutter Icon Generator - Fase 1")
        self.root.geometry("700x650")
        self.root.minsize(700, 650)
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar(value=os.path.join(os.getcwd(), "output"))
        self.bg_color = tk.StringVar(value="#FFFFFF")
        self.android_scale = tk.DoubleVar(value=0.8)
        self.ios_scale = tk.DoubleVar(value=0.85)
        self.preview_image = None
        self.preview_tk = None
        
        # Crear UI
        self.create_ui()
        
        # Centrar ventana
        self.center_window()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_ui(self):
        """Crea la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Flutter Icon Generator", 
            font=('Helvetica', 18, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Genera iconos para Android e iOS automáticamente",
            font=('Helvetica', 10)
        )
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # === SECCIÓN 1: IMAGEN DE ENTRADA ===
        input_frame = ttk.LabelFrame(main_frame, text="1. Imagen de Entrada", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Archivo:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(input_frame, text="Buscar...", command=self.select_input_file).grid(row=0, column=2)
        
        # Preview
        self.preview_label = ttk.Label(input_frame, text="Vista previa no disponible")
        self.preview_label.grid(row=1, column=0, columnspan=3, pady=10)
        
        # === SECCIÓN 2: CONFIGURACIÓN ===
        config_frame = ttk.LabelFrame(main_frame, text="2. Configuración", padding="10")
        config_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Color de fondo
        ttk.Label(config_frame, text="Color de fondo:").grid(row=0, column=0, sticky=tk.W)
        color_frame = ttk.Frame(config_frame)
        color_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        self.color_preview = tk.Label(
            color_frame, 
            text="   ", 
            bg=self.bg_color.get(), 
            relief="solid",
            width=5
        )
        self.color_preview.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(color_frame, text="Elegir Color", command=self.pick_color).pack(side=tk.LEFT)
        ttk.Button(color_frame, text="Transparente", command=self.set_transparent).pack(side=tk.LEFT, padx=(5, 0))
        
        # Escalas
        scale_frame = ttk.Frame(config_frame)
        scale_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(scale_frame, text="Escala Android:").grid(row=0, column=0, sticky=tk.W)
        self.android_scale_slider = ttk.Scale(
            scale_frame, 
            from_=0.5, 
            to=1.0, 
            orient=tk.HORIZONTAL, 
            variable=self.android_scale,
            length=200
        )
        self.android_scale_slider.grid(row=0, column=1, padx=5)
        self.android_scale_label = ttk.Label(scale_frame, text=f"{self.android_scale.get():.0%}")
        self.android_scale_label.grid(row=0, column=2)
        
        ttk.Label(scale_frame, text="Escala iOS:").grid(row=1, column=0, sticky=tk.W)
        self.ios_scale_slider = ttk.Scale(
            scale_frame, 
            from_=0.5, 
            to=1.0, 
            orient=tk.HORIZONTAL, 
            variable=self.ios_scale,
            length=200
        )
        self.ios_scale_slider.grid(row=1, column=1, padx=5)
        self.ios_scale_label = ttk.Label(scale_frame, text=f"{self.ios_scale.get():.0%}")
        self.ios_scale_label.grid(row=1, column=2)
        
        # Actualizar labels cuando cambien los sliders
        self.android_scale.trace_add('write', lambda *args: self.update_scale_labels())
        self.ios_scale.trace_add('write', lambda *args: self.update_scale_labels())
        
        # === SECCIÓN 3: CARPETA DE SALIDA ===
        output_frame = ttk.LabelFrame(main_frame, text="3. Carpeta de Salida", padding="10")
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Destino:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(output_frame, text="Cambiar...", command=self.select_output_folder).grid(row=0, column=2)
        
        # === SECCIÓN 4: BOTÓN DE GENERACIÓN ===
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        self.generate_btn = tk.Button(
            btn_frame,
            text="🚀 GENERAR ICONOS",
            command=self.generate_icons,
            bg="#4CAF50",
            fg="white",
            font=('Helvetica', 12, 'bold'),
            height=2,
            width=25,
            cursor="hand2"
        )
        self.generate_btn.pack()
        
        # === SECCIÓN 5: LOG/PROGRESO ===
        log_frame = ttk.LabelFrame(main_frame, text="Progreso", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # === FOOTER ===
        footer_label = ttk.Label(
            main_frame,
            text="Fase 1: Core funcional | Android + iOS completo",
            font=('Helvetica', 8),
            foreground="gray"
        )
        footer_label.grid(row=7, column=0, columnspan=3, pady=(10, 0))
    
    def update_scale_labels(self):
        """Actualiza los labels de escala"""
        self.android_scale_label.config(text=f"{self.android_scale.get():.0%}")
        self.ios_scale_label.config(text=f"{self.ios_scale.get():.0%}")
    
    def select_input_file(self):
        """Abre diálogo para seleccionar imagen"""
        filename = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )
        if filename:
            self.input_path.set(filename)
            self.update_preview(filename)
    
    def update_preview(self, filepath):
        """Actualiza la vista previa de la imagen"""
        try:
            img = Image.open(filepath)
            
            # Redimensionar para preview (máximo 200x200)
            max_size = 200
            ratio = min(max_size/img.width, max_size/img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            self.preview_tk = ImageTk.PhotoImage(img)
            
            self.preview_label.config(image=self.preview_tk, text="")
            self.log(f"Imagen cargada: {os.path.basename(filepath)} ({img.width}x{img.height})")
        except Exception as e:
            self.preview_label.config(text=f"Error al cargar imagen: {str(e)}")
            self.log(f"Error: {str(e)}")
    
    def select_output_folder(self):
        """Abre diálogo para seleccionar carpeta de salida"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if folder:
            self.output_path.set(folder)
    
    def pick_color(self):
        """Abre selector de color"""
        color = colorchooser.askcolor(title="Seleccionar color de fondo", color=self.bg_color.get())
        if color[1]:
            self.bg_color.set(color[1])
            self.color_preview.config(bg=color[1])
    
    def set_transparent(self):
        """Establece fondo transparente"""
        self.bg_color.set("")
        self.color_preview.config(bg="gray")
    
    def log(self, message):
        """Agrega mensaje al log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def generate_icons(self):
        """Genera todos los iconos"""
        # Validaciones
        if not self.input_path.get():
            messagebox.showerror("Error", "Debes seleccionar una imagen de entrada")
            return
        
        if not os.path.exists(self.input_path.get()):
            messagebox.showerror("Error", "El archivo de entrada no existe")
            return
        
        # Deshabilitar botón
        self.generate_btn.config(state=tk.DISABLED, text="Generando...")
        self.log_text.delete(1.0, tk.END)
        self.log("Iniciando generación de iconos...")
        
        try:
            # Crear generador
            generator = IconGenerator(self.output_path.get())
            
            # Generar iconos
            bg_color = self.bg_color.get() if self.bg_color.get() else None
            
            self.log(f"Color de fondo: {bg_color if bg_color else 'Transparente'}")
            self.log(f"Escala Android: {self.android_scale.get():.0%}")
            self.log(f"Escala iOS: {self.ios_scale.get():.0%}")
            self.log("")
            
            results = generator.generate_all(
                input_path=self.input_path.get(),
                bg_color=bg_color,
                android_scale=self.android_scale.get(),
                ios_scale=self.ios_scale.get()
            )
            
            # Mostrar resultados
            self.log("")
            self.log("✅ ¡Generación completada!")
            self.log(f"Total de archivos generados: {results['total']}")
            self.log("")
            self.log("Archivos Android:")
            for f in results['android']:
                self.log(f"  📱 {os.path.basename(f)}")
            
            self.log("")
            self.log("Archivos iOS:")
            for f in results['ios']:
                self.log(f"  🍎 {os.path.basename(f)}")
            
            # Preguntar si abrir carpeta
            if messagebox.askyesno(
                "Éxito", 
                f"Se generaron {results['total']} archivos.\n\n¿Deseas abrir la carpeta de salida?"
            ):
                os.startfile(self.output_path.get())
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar iconos:\n{str(e)}")
            self.log(f"❌ Error: {str(e)}")
        finally:
            # Rehabilitar botón
            self.generate_btn.config(state=tk.NORMAL, text="🚀 GENERAR ICONOS")

def main():
    """Función principal"""
    root = tk.Tk()
    
    # Estilo moderno (si está disponible)
    try:
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic'
    except:
        pass
    
    app = FlutterIconGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
