"""
Sistema de configuración persistente para Flutter Icon Generator
Guarda y carga configuraciones en formato JSON
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class AppConfig:
    """Configuración de la aplicación"""
    # Rutas
    last_input_path: str = ""
    last_output_path: str = ""
    
    # Configuración de iconos
    bg_color: str = "#FFFFFF"
    use_transparent_bg: bool = False
    android_scale: float = 0.8
    ios_scale: float = 0.85
    
    # UI
    window_width: int = 900
    window_height: int = 750
    
    # Historial
    recent_files: list = None
    max_recent_files: int = 10
    
    def __post_init__(self):
        if self.recent_files is None:
            self.recent_files = []


class ConfigManager:
    """Gestor de configuración de la aplicación"""
    
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.config = AppConfig()
        self.load()
    
    def _get_config_dir(self) -> str:
        """Obtiene el directorio de configuración según el sistema operativo"""
        # En Windows: %APPDATA%/FlutterIconGenerator
        # En macOS/Linux: ~/.config/flutter_icon_generator
        
        if os.name == 'nt':  # Windows
            app_data = os.environ.get('APPDATA', os.path.expanduser('~'))
            config_dir = os.path.join(app_data, 'FlutterIconGenerator')
        else:  # macOS/Linux
            config_dir = os.path.expanduser('~/.config/flutter_icon_generator')
        
        # Crear directorio si no existe
        os.makedirs(config_dir, exist_ok=True)
        return config_dir
    
    def load(self) -> AppConfig:
        """Carga la configuración desde el archivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.config = AppConfig(**data)
            except Exception as e:
                print(f"Error al cargar configuración: {e}")
                self.config = AppConfig()
        return self.config
    
    def save(self) -> bool:
        """Guarda la configuración en el archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.config), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            return False
    
    def add_recent_file(self, filepath: str):
        """Agrega un archivo al historial reciente"""
        if filepath in self.config.recent_files:
            self.config.recent_files.remove(filepath)
        
        self.config.recent_files.insert(0, filepath)
        
        # Mantener solo los últimos N archivos
        self.config.recent_files = self.config.recent_files[:self.config.max_recent_files]
        self.save()
    
    def get_recent_files(self) -> list:
        """Obtiene la lista de archivos recientes que aún existen"""
        valid_files = []
        for filepath in self.config.recent_files:
            if os.path.exists(filepath):
                valid_files.append(filepath)
        return valid_files
    
    def update_from_gui(self, **kwargs):
        """Actualiza la configuración desde valores de la GUI"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        self.save()


# Templates predefinidos
TEMPLATES = {
    "default": {
        "name": "Por defecto",
        "description": "Configuración estándar recomendada",
        "bg_color": "#FFFFFF",
        "use_transparent_bg": False,
        "android_scale": 0.8,
        "ios_scale": 0.85
    },
    "material": {
        "name": "Material Design",
        "description": "Optimizado para Material Design (Android)",
        "bg_color": "#FFFFFF",
        "use_transparent_bg": False,
        "android_scale": 0.72,
        "ios_scale": 0.85
    },
    "ios_rounded": {
        "name": "iOS Rounded",
        "description": "Optimizado para iconos redondeados de iOS",
        "bg_color": "#FFFFFF",
        "use_transparent_bg": False,
        "android_scale": 0.8,
        "ios_scale": 0.78
    },
    "adaptive": {
        "name": "Android Adaptive",
        "description": "Foco en iconos adaptativos de Android 8+",
        "bg_color": "#FFFFFF",
        "use_transparent_bg": True,
        "android_scale": 0.75,
        "ios_scale": 0.85
    },
    "dark": {
        "name": "Tema Oscuro",
        "description": "Fondo oscuro para logos claros",
        "bg_color": "#1A1A1A",
        "use_transparent_bg": False,
        "android_scale": 0.8,
        "ios_scale": 0.85
    },
    "brand": {
        "name": "Marca Corporativa",
        "description": "Márgenes amplios para logos con texto",
        "bg_color": "#FFFFFF",
        "use_transparent_bg": False,
        "android_scale": 0.65,
        "ios_scale": 0.70
    },
    # Fase 3: Nuevos templates
    "web_pwa": {
        "name": "Web / PWA",
        "description": "Optimizado para aplicaciones web y PWA",
        "bg_color": "#FFFFFF",
        "use_transparent_bg": False,
        "android_scale": 0.85,
        "ios_scale": 0.88
    },
    "web_transparent": {
        "name": "Web Transparente",
        "description": "Fondo transparente para favicon y PWA",
        "bg_color": "#FFFFFF",
        "use_transparent_bg": True,
        "android_scale": 0.9,
        "ios_scale": 0.9
    },
    "windows_metro": {
        "name": "Windows Metro",
        "description": "Estilo Windows 10/11 Modern UI",
        "bg_color": "#0078D4",
        "use_transparent_bg": False,
        "android_scale": 0.82,
        "ios_scale": 0.85
    },
    "macos_big_sur": {
        "name": "macOS Big Sur",
        "description": "Estilo macOS Big Sur con esquinas redondeadas",
        "bg_color": "#F5F5F7",
        "use_transparent_bg": False,
        "android_scale": 0.8,
        "ios_scale": 0.75
    },
    "gradient_ready": {
        "name": "Listo para Gradiente",
        "description": "Logo grande sin fondo para aplicar gradientes",
        "bg_color": "#FFFFFF",
        "use_transparent_bg": True,
        "android_scale": 0.6,
        "ios_scale": 0.65
    },
    "minimal": {
        "name": "Minimalista",
        "description": "Márgenes extra grandes para diseño minimalista",
        "bg_color": "#FFFFFF",
        "use_transparent_bg": False,
        "android_scale": 0.55,
        "ios_scale": 0.60
    },
    "gaming": {
        "name": "Gaming",
        "description": "Estilo gaming con fondo oscuro y logo grande",
        "bg_color": "#0D0D0D",
        "use_transparent_bg": False,
        "android_scale": 0.88,
        "ios_scale": 0.88
    },
    "social": {
        "name": "Red Social",
        "description": "Optimizado para apps sociales (estilo Instagram/TikTok)",
        "bg_color": "#000000",
        "use_transparent_bg": False,
        "android_scale": 0.82,
        "ios_scale": 0.82
    }
}


class TemplateManager:
    """Gestor de templates"""
    
    def __init__(self):
        self.templates = TEMPLATES.copy()
        self.user_templates_file = os.path.join(
            ConfigManager().config_dir, "user_templates.json"
        )
        self.load_user_templates()
    
    def load_user_templates(self):
        """Carga templates personalizados del usuario"""
        if os.path.exists(self.user_templates_file):
            try:
                with open(self.user_templates_file, 'r', encoding='utf-8') as f:
                    user_templates = json.load(f)
                    self.templates.update(user_templates)
            except Exception as e:
                print(f"Error al cargar templates de usuario: {e}")
    
    def save_user_template(self, template_id: str, template_data: dict):
        """Guarda un template personalizado"""
        self.templates[template_id] = template_data
        
        # Filtrar solo templates de usuario
        user_templates = {
            k: v for k, v in self.templates.items() 
            if k not in TEMPLATES
        }
        
        try:
            with open(self.user_templates_file, 'w', encoding='utf-8') as f:
                json.dump(user_templates, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar template: {e}")
            return False
    
    def get_template(self, template_id: str) -> Optional[dict]:
        """Obtiene un template por ID"""
        return self.templates.get(template_id)
    
    def get_all_templates(self) -> Dict[str, dict]:
        """Obtiene todos los templates disponibles"""
        return self.templates
    
    def apply_template(self, template_id: str, config_manager: ConfigManager):
        """Aplica un template a la configuración actual"""
        template = self.get_template(template_id)
        if template:
            config_manager.config.bg_color = template.get("bg_color", "#FFFFFF")
            config_manager.config.use_transparent_bg = template.get("use_transparent_bg", False)
            config_manager.config.android_scale = template.get("android_scale", 0.8)
            config_manager.config.ios_scale = template.get("ios_scale", 0.85)
            config_manager.save()
            return True
        return False
