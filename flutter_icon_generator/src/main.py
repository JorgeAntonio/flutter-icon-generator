"""
Flutter Icon Generator - Interfaz Gráfica Principal
Fase 3: Multiplataforma completa + Integración flutter_launcher_icons
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.icon_generator import IconGenerator
from src.config_manager import ConfigManager, TemplateManager
from src.preview_manager import PreviewWindow
from src.flutter_integration import FlutterLauncherIconsIntegration

class FlutterIconGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flutter Icon Generator v3.0 - Fase 3 (Multiplataforma)")
        
        # Inicializar gestores
        self.config_manager = ConfigManager()
        self.template_manager = TemplateManager()
        self.flutter_integration = FlutterLauncherIconsIntegration()
        self.config = self.config_manager.config
        
        # Configurar ventana
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.minsize(1000, 800)
        
        # Variables
        self.input_path = tk.StringVar(value=self.config.last_input_path)
        self.output_path = tk.StringVar(value=self.config.last_output_path or os.path.join(os.getcwd(), "output"))
        self.bg_color = tk.StringVar(value=self.config.bg_color if not self.config.use_transparent_bg else "")
        self.android_scale = tk.DoubleVar(value=self.config.android_scale)
        self.ios_scale = tk.DoubleVar(value=self.config.ios_scale)
        self.selected_template = tk.StringVar(value="default")
        self.flutter_project_path = tk.StringVar()
        
        # Variables para plataformas
        self.platform_android = tk.BooleanVar(value=True)
        self.platform_ios = tk.BooleanVar(value=True)
        self.platform_web = tk.BooleanVar(value=True)
        self.platform_windows = tk.BooleanVar(value=True)
        self.platform_macos = tk.BooleanVar(value=True)
        
        self.preview_image = None
        self.preview_tk = None
        self.current_image = None
        
        # Crear menú
        self.create_menu()
        
        # Crear UI
        self.create_ui()
        
        # Cargar archivo reciente si existe
        if self.input_path.get() and os.path.exists(self.input_path.get()):
            self.update_preview(self.input_path.get())
        
        # Centrar ventana
        self.center_window()
        
        # Guardar tamaño de ventana al cerrar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Abrir imagen...", command=self.select_input_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        
        # Submenú de archivos recientes
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Archivos recientes", menu=self.recent_menu)
        self.update_recent_menu()
        
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_closing)
        
        # Menú Templates
        template_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Templates", menu=template_menu)
        
        for template_id, template_data in self.template_manager.get_all_templates().items():
            template_menu.add_command(
                label=f"{template_data['name']}",
                command=lambda tid=template_id: self.apply_template(tid)
            )
        
        # Menú Flutter
        flutter_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Flutter", menu=flutter_menu)
        flutter_menu.add_command(label="Seleccionar proyecto Flutter...", command=self.select_flutter_project)
        flutter_menu.add_command(label="Verificar instalación Flutter", command=self.check_flutter_installation)
        flutter_menu.add_separator()
        flutter_menu.add_command(label="Copiar iconos al proyecto", command=self.copy_icons_to_project)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)
        
        # Atajos de teclado
        self.root.bind('<Control-o>', lambda e: self.select_input_file())
    
    def update_recent_menu(self):
        """Actualiza el menú de archivos recientes"""
        self.recent_menu.delete(0, tk.END)
        recent_files = self.config_manager.get_recent_files()
        
        if not recent_files:
            self.recent_menu.add_command(label="(No hay archivos recientes)", state=tk.DISABLED)
        else:
            for filepath in recent_files:
                filename = os.path.basename(filepath)
                self.recent_menu.add_command(
                    label=filename,
                    command=lambda f=filepath: self.load_recent_file(f)
                )
    
    def load_recent_file(self, filepath):
        """Carga un archivo del historial"""
        if os.path.exists(filepath):
            self.input_path.set(filepath)
            self.update_preview(filepath)
        else:
            messagebox.showerror("Error", "El archivo ya no existe")
            self.config_manager.load()
            self.update_recent_menu()
    
    def apply_template(self, template_id):
        """Aplica un template"""
        template = self.template_manager.get_template(template_id)
        if template:
            self.selected_template.set(template_id)
            self.bg_color.set(template.get("bg_color", "#FFFFFF"))
            self.android_scale.set(template.get("android_scale", 0.8))
            self.ios_scale.set(template.get("ios_scale", 0.85))
            
            if self.bg_color.get():
                self.color_preview.config(bg=self.bg_color.get())
            else:
                self.color_preview.config(bg="gray")
            
            self.update_scale_labels()
            self.log(f"Template aplicado: {template['name']}")
            self.save_config()
    
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
        # Frame principal con padding
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
            font=('Helvetica', 22, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Genera iconos para Android, iOS, Web, Windows y macOS",
            font=('Helvetica', 11)
        )
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # === PANEL IZQUIERDO: CONTROLES ===
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=2, column=0, sticky=(tk.N, tk.W, tk.E), padx=(0, 10))
        left_frame.columnconfigure(1, weight=1)
        
        # --- SECCIÓN 1: IMAGEN DE ENTRADA ---
        input_frame = ttk.LabelFrame(left_frame, text="1. Imagen de Entrada", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Archivo:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.input_path, width=40).grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(input_frame, text="Buscar...", command=self.select_input_file).grid(row=0, column=2)
        
        self.preview_label = ttk.Label(input_frame, text="Sin imagen seleccionada")
        self.preview_label.grid(row=1, column=0, columnspan=3, pady=10)
        
        self.image_info_label = ttk.Label(input_frame, text="", font=('Helvetica', 8))
        self.image_info_label.grid(row=2, column=0, columnspan=3)
        
        # --- SECCIÓN 2: PLATAFORMAS ---
        platforms_frame = ttk.LabelFrame(left_frame, text="2. Plataformas a Generar", padding="10")
        platforms_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(platforms_frame, text="Android", variable=self.platform_android).grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Checkbutton(platforms_frame, text="iOS", variable=self.platform_ios).grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Checkbutton(platforms_frame, text="Web", variable=self.platform_web).grid(row=0, column=2, sticky=tk.W, padx=5)
        ttk.Checkbutton(platforms_frame, text="Windows", variable=self.platform_windows).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(platforms_frame, text="macOS", variable=self.platform_macos).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # --- SECCIÓN 3: TEMPLATES ---
        template_frame = ttk.LabelFrame(left_frame, text="3. Templates Predefinidos", padding="10")
        template_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        template_frame.columnconfigure(0, weight=1)
        
        template_names = [f"{v['name']}" for k, v in self.template_manager.get_all_templates().items()]
        self.template_combo = ttk.Combobox(
            template_frame, 
            values=template_names,
            state="readonly",
            width=35
        )
        self.template_combo.set("Por defecto")
        self.template_combo.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        self.template_combo.bind('<<ComboboxSelected>>', self.on_template_selected)
        
        self.template_desc_label = ttk.Label(
            template_frame, 
            text="Configuración estándar recomendada",
            font=('Helvetica', 8, 'italic'),
            foreground="gray"
        )
        self.template_desc_label.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))
        
        # --- SECCIÓN 4: CONFIGURACIÓN ---
        config_frame = ttk.LabelFrame(left_frame, text="4. Configuración Avanzada", padding="10")
        config_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        ttk.Label(config_frame, text="Color de fondo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        color_frame = ttk.Frame(config_frame)
        color_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        self.color_preview = tk.Label(
            color_frame, 
            text="   ", 
            bg=self.bg_color.get() if self.bg_color.get() else "gray", 
            relief="solid",
            width=5
        )
        self.color_preview.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(color_frame, text="Elegir Color", command=self.pick_color).pack(side=tk.LEFT)
        ttk.Button(color_frame, text="Transparente", command=self.set_transparent).pack(side=tk.LEFT, padx=(5, 0))
        
        scale_frame = ttk.Frame(config_frame)
        scale_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(scale_frame, text="Escala Android:").grid(row=0, column=0, sticky=tk.W)
        self.android_scale_slider = ttk.Scale(
            scale_frame, 
            from_=0.5, 
            to=1.0, 
            orient=tk.HORIZONTAL, 
            variable=self.android_scale,
            length=200,
            command=lambda v: self.update_scale_labels()
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
            length=200,
            command=lambda v: self.update_scale_labels()
        )
        self.ios_scale_slider.grid(row=1, column=1, padx=5)
        self.ios_scale_label = ttk.Label(scale_frame, text=f"{self.ios_scale.get():.0%}")
        self.ios_scale_label.grid(row=1, column=2)
        
        # --- SECCIÓN 5: CARPETA DE SALIDA ---
        output_frame = ttk.LabelFrame(left_frame, text="5. Carpeta de Salida", padding="10")
        output_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Destino:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.output_path, width=40).grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(output_frame, text="Cambiar...", command=self.select_output_folder).grid(row=0, column=2)
        
        # --- SECCIÓN 6: PROYECTO FLUTTER (OPCIONAL) ---
        flutter_frame = ttk.LabelFrame(left_frame, text="6. Proyecto Flutter (Opcional)", padding="10")
        flutter_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        flutter_frame.columnconfigure(1, weight=1)
        
        ttk.Label(flutter_frame, text="Ruta:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(flutter_frame, textvariable=self.flutter_project_path, width=40).grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(flutter_frame, text="Buscar...", command=self.select_flutter_project).grid(row=0, column=2)
        
        self.flutter_status_label = ttk.Label(flutter_frame, text="Sin proyecto seleccionado", font=('Helvetica', 8))
        self.flutter_status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # === PANEL DERECHO: PREVIEW Y ACCIONES ===
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=2, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # --- BOTONES DE ACCIÓN ---
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.preview_btn = tk.Button(
            btn_frame,
            text="👁️ VISTA PREVIA",
            command=self.show_preview_window,
            bg="#2196F3",
            fg="white",
            font=('Helvetica', 10, 'bold'),
            height=2,
            width=18,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.generate_btn = tk.Button(
            btn_frame,
            text="🚀 GENERAR",
            command=self.generate_icons,
            bg="#4CAF50",
            fg="white",
            font=('Helvetica', 10, 'bold'),
            height=2,
            width=18,
            cursor="hand2"
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.copy_btn = tk.Button(
            btn_frame,
            text="📋 COPIAR A FLUTTER",
            command=self.copy_icons_to_project,
            bg="#FF9800",
            fg="white",
            font=('Helvetica', 10, 'bold'),
            height=2,
            width=20,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.copy_btn.pack(side=tk.LEFT)
        
        # --- LOG/PROGRESO ---
        log_frame = ttk.LabelFrame(right_frame, text="Progreso", padding="10")
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=20, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # === FOOTER ===
        footer_label = ttk.Label(
            main_frame,
            text="Fase 3: Multiplataforma + Integración Flutter | v3.0 | 5 plataformas soportadas",
            font=('Helvetica', 8),
            foreground="gray"
        )
        footer_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))
    
    def on_template_selected(self, event):
        """Maneja la selección de un template desde el combobox"""
        selected_name = self.template_combo.get()
        
        for template_id, template_data in self.template_manager.get_all_templates().items():
            if template_data['name'] == selected_name:
                self.apply_template(template_id)
                self.template_desc_label.config(text=template_data['description'])
                break
    
    def update_scale_labels(self):
        """Actualiza los labels de escala"""
        self.android_scale_label.config(text=f"{self.android_scale.get():.0%}")
        self.ios_scale_label.config(text=f"{self.ios_scale.get():.0%}")
        self.save_config()
    
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
            self.config_manager.add_recent_file(filename)
            self.update_recent_menu()
            self.save_config()
    
    def update_preview(self, filepath):
        """Actualiza la vista previa de la imagen"""
        try:
            self.current_image = Image.open(filepath)
            
            max_size = 180
            ratio = min(max_size/self.current_image.width, max_size/self.current_image.height)
            new_size = (int(self.current_image.width * ratio), int(self.current_image.height * ratio))
            
            img = self.current_image.resize(new_size, Image.Resampling.LANCZOS)
            self.preview_tk = ImageTk.PhotoImage(img)
            
            self.preview_label.config(image=self.preview_tk, text="")
            self.image_info_label.config(
                text=f"{self.current_image.width}x{self.current_image.height}px | {os.path.basename(filepath)}"
            )
            
            self.preview_btn.config(state=tk.NORMAL)
            
            self.log(f"Imagen cargada: {os.path.basename(filepath)} ({self.current_image.width}x{self.current_image.height})")
        except Exception as e:
            self.preview_label.config(text=f"Error al cargar imagen")
            self.image_info_label.config(text=str(e))
            self.current_image = None
            self.preview_btn.config(state=tk.DISABLED)
            self.log(f"Error: {str(e)}")
    
    def show_preview_window(self):
        """Muestra la ventana de preview de iconos"""
        if self.current_image:
            bg_color = self.bg_color.get() if self.bg_color.get() else None
            PreviewWindow(
                self.root,
                self.current_image,
                bg_color,
                self.android_scale.get(),
                self.ios_scale.get()
            )
    
    def select_output_folder(self):
        """Abre diálogo para seleccionar carpeta de salida"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if folder:
            self.output_path.set(folder)
            self.save_config()
    
    def select_flutter_project(self):
        """Abre diálogo para seleccionar proyecto Flutter"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta del proyecto Flutter")
        if folder:
            self.flutter_project_path.set(folder)
            self.update_flutter_status()
    
    def update_flutter_status(self):
        """Actualiza el estado del proyecto Flutter"""
        project_path = self.flutter_project_path.get()
        
        if not project_path:
            self.flutter_status_label.config(text="Sin proyecto seleccionado")
            self.copy_btn.config(state=tk.DISABLED)
            return
        
        if not os.path.exists(os.path.join(project_path, 'pubspec.yaml')):
            self.flutter_status_label.config(text="⚠️ No es un proyecto Flutter válido (falta pubspec.yaml)")
            self.copy_btn.config(state=tk.DISABLED)
            return
        
        self.flutter_status_label.config(text="✅ Proyecto Flutter válido")
        self.copy_btn.config(state=tk.NORMAL)
    
    def check_flutter_installation(self):
        """Verifica si Flutter está instalado"""
        if self.flutter_integration.is_flutter_available():
            version = self.flutter_integration.get_flutter_version()
            messagebox.showinfo(
                "Flutter Instalado",
                f"Flutter encontrado:\n{version}\n\n"
                f"flutter_launcher_icons: {'Instalado' if self.flutter_integration.check_flutter_launcher_icons_installed() else 'No instalado'}"
            )
        else:
            messagebox.showwarning(
                "Flutter No Encontrado",
                "Flutter no está instalado o no se encuentra en el PATH del sistema.\n\n"
                "Puedes seguir usando la aplicación para generar iconos, "
                "pero no podrás usar la integración automática."
            )
    
    def copy_icons_to_project(self):
        """Copia los iconos generados al proyecto Flutter"""
        project_path = self.flutter_project_path.get()
        output_path = self.output_path.get()
        
        if not project_path or not os.path.exists(project_path):
            messagebox.showerror("Error", "Selecciona un proyecto Flutter válido primero")
            return
        
        if not os.path.exists(output_path):
            messagebox.showerror("Error", "No se encontraron iconos generados. Genera los iconos primero.")
            return
        
        # Obtener plataformas seleccionadas
        platforms = []
        if self.platform_android.get(): platforms.append('android')
        if self.platform_ios.get(): platforms.append('ios')
        if self.platform_web.get(): platforms.append('web')
        if self.platform_windows.get(): platforms.append('windows')
        if self.platform_macos.get(): platforms.append('macos')
        
        self.log("Copiando iconos al proyecto Flutter...")
        results = self.flutter_integration.copy_icons_to_project(output_path, project_path, platforms)
        
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        
        self.log(f"\nCopia completada: {success_count}/{total_count} plataformas exitosas")
        for platform, success in results.items():
            status = "✅" if success else "❌"
            self.log(f"  {status} {platform.capitalize()}")
        
        messagebox.showinfo(
            "Copia Completada",
            f"Se copiaron los iconos a {success_count}/{total_count} plataformas.\n\n"
            "Revisa el log para más detalles."
        )
    
    def pick_color(self):
        """Abre selector de color"""
        current = self.bg_color.get() if self.bg_color.get() else "#FFFFFF"
        color = colorchooser.askcolor(title="Seleccionar color de fondo", color=current)
        if color[1]:
            self.bg_color.set(color[1])
            self.color_preview.config(bg=color[1])
            self.save_config()
    
    def set_transparent(self):
        """Establece fondo transparente"""
        self.bg_color.set("")
        self.color_preview.config(bg="gray")
        self.save_config()
    
    def save_config(self):
        """Guarda la configuración actual"""
        self.config_manager.update_from_gui(
            last_input_path=self.input_path.get(),
            last_output_path=self.output_path.get(),
            bg_color=self.bg_color.get() if not self.config.use_transparent_bg else self.config.bg_color,
            use_transparent_bg=(self.bg_color.get() == ""),
            android_scale=self.android_scale.get(),
            ios_scale=self.ios_scale.get(),
            window_width=self.root.winfo_width(),
            window_height=self.root.winfo_height()
        )
    
    def log(self, message):
        """Agrega mensaje al log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def show_about(self):
        """Muestra diálogo Acerca de"""
        messagebox.showinfo(
            "Acerca de Flutter Icon Generator",
            "Flutter Icon Generator v3.0\n\n"
            "Fase 3: Multiplataforma + Integración Flutter\n\n"
            "Genera iconos para aplicaciones Flutter de forma automática.\n"
            "Soporta Android, iOS, Web, Windows y macOS.\n\n"
            "Características:\n"
            "• 40+ tamaños de iconos automáticos\n"
            "• 5 plataformas soportadas\n"
            "• Generación de YAML para flutter_launcher_icons\n"
            "• Copia automática al proyecto Flutter\n"
            "• Vista previa visual en tiempo real\n"
            "• Templates predefinidos\n"
            "• Historial de archivos recientes\n"
            "• Configuración persistente\n\n"
            "© 2025 - Libre para usar y modificar"
        )
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        self.save_config()
        self.root.destroy()
    
    def generate_icons(self):
        """Genera todos los iconos"""
        # Validaciones
        if not self.input_path.get():
            messagebox.showerror("Error", "Debes seleccionar una imagen de entrada")
            return
        
        if not os.path.exists(self.input_path.get()):
            messagebox.showerror("Error", "El archivo de entrada no existe")
            return
        
        # Obtener plataformas seleccionadas
        platforms = []
        if self.platform_android.get(): platforms.append('android')
        if self.platform_ios.get(): platforms.append('ios')
        if self.platform_web.get(): platforms.append('web')
        if self.platform_windows.get(): platforms.append('windows')
        if self.platform_macos.get(): platforms.append('macos')
        
        if not platforms:
            messagebox.showerror("Error", "Selecciona al menos una plataforma")
            return
        
        # Deshabilitar botón
        self.generate_btn.config(state=tk.DISABLED, text="Generando...")
        self.log_text.delete(1.0, tk.END)
        self.log("Iniciando generación de iconos...")
        self.log(f"Plataformas seleccionadas: {', '.join(platforms).upper()}")
        
        try:
            # Crear generador
            generator = IconGenerator(self.output_path.get())
            
            # Generar iconos
            bg_color = self.bg_color.get() if self.bg_color.get() else None
            
            self.log(f"\nConfiguración:")
            self.log(f"  Color de fondo: {bg_color if bg_color else 'Transparente'}")
            self.log(f"  Escala Android: {self.android_scale.get():.0%}")
            self.log(f"  Escala iOS: {self.ios_scale.get():.0%}")
            self.log("")
            
            results = generator.generate_all(
                input_path=self.input_path.get(),
                bg_color=bg_color,
                android_scale=self.android_scale.get(),
                ios_scale=self.ios_scale.get(),
                platforms=platforms
            )
            
            # Mostrar resultados
            self.log("\n" + "="*50)
            self.log("GENERACIÓN COMPLETADA!")
            self.log("="*50)
            self.log(f"\nTotal de archivos generados: {results['total']}")
            self.log(f"Archivo YAML: {os.path.basename(results['yaml'])}")
            
            if results['android']:
                self.log(f"\n📱 Android ({len(results['android'])} archivos):")
                for f in results['android'][:5]:
                    self.log(f"  • {os.path.basename(f)}")
                if len(results['android']) > 5:
                    self.log(f"  ... y {len(results['android'])-5} más")
            
            if results['ios']:
                self.log(f"\n🍎 iOS ({len(results['ios'])} archivos):")
                for f in results['ios'][:5]:
                    self.log(f"  • {os.path.basename(f)}")
                if len(results['ios']) > 5:
                    self.log(f"  ... y {len(results['ios'])-5} más")
            
            if results['web']:
                self.log(f"\n🌐 Web ({len(results['web'])} archivos):")
                for f in results['web'][:5]:
                    self.log(f"  • {os.path.basename(f)}")
                if len(results['web']) > 5:
                    self.log(f"  ... y {len(results['web'])-5} más")
            
            if results['windows']:
                self.log(f"\n🪟 Windows ({len(results['windows'])} archivos):")
                for f in results['windows'][:5]:
                    self.log(f"  • {os.path.basename(f)}")
                if len(results['windows']) > 5:
                    self.log(f"  ... y {len(results['windows'])-5} más")
            
            if results['macos']:
                self.log(f"\n🍏 macOS ({len(results['macos'])} archivos):")
                for f in results['macos'][:5]:
                    self.log(f"  • {os.path.basename(f)}")
                if len(results['macos']) > 5:
                    self.log(f"  ... y {len(results['macos'])-5} más")
            
            self.log("\n" + "="*50)
            self.log(f"Archivos guardados en: {self.output_path.get()}")
            self.log("="*50)
            
            # Habilitar botón de copiar si hay proyecto Flutter
            if self.flutter_project_path.get() and os.path.exists(self.flutter_project_path.get()):
                self.copy_btn.config(state=tk.NORMAL)
            
            # Preguntar si abrir carpeta
            if messagebox.askyesno(
                "Éxito", 
                f"Se generaron {results['total']} archivos para {len(platforms)} plataforma(s).\n\n"
                f"¿Deseas abrir la carpeta de salida?"
            ):
                os.startfile(self.output_path.get())
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar iconos:\n{str(e)}")
            self.log(f"\n❌ ERROR: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
        finally:
            # Rehabilitar botón
            self.generate_btn.config(state=tk.NORMAL, text="🚀 GENERAR")

def main():
    """Función principal"""
    root = tk.Tk()
    
    # Estilo moderno
    try:
        style = ttk.Style()
        style.theme_use('clam')
    except:
        pass
    
    app = FlutterIconGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
