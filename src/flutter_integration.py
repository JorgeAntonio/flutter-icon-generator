"""
Integración con flutter_launcher_icons
Permite ejecutar el comando automáticamente y gestionar configuraciones YAML
"""

import os
import subprocess
import shutil
from typing import List, Optional, Dict
from pathlib import Path

class FlutterLauncherIconsIntegration:
    """Integración con el paquete flutter_launcher_icons"""
    
    def __init__(self, working_dir: str = None):
        self.working_dir = working_dir or os.getcwd()
        self.flutter_executable = self._find_flutter_executable()
    
    def _find_flutter_executable(self) -> Optional[str]:
        """Busca el ejecutable de Flutter en el sistema"""
        # Intentar encontrar flutter en PATH
        flutter_cmd = shutil.which('flutter')
        if flutter_cmd:
            return flutter_cmd
        
        # Buscar en ubicaciones comunes de Windows
        common_paths = [
            os.path.expandvars(r'%LOCALAPPDATA%\flutter\bin\flutter.bat'),
            os.path.expandvars(r'%USERPROFILE%\flutter\bin\flutter.bat'),
            r'C:\flutter\bin\flutter.bat',
            r'C:\src\flutter\bin\flutter.bat',
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def is_flutter_available(self) -> bool:
        """Verifica si Flutter está instalado y disponible"""
        return self.flutter_executable is not None
    
    def is_flutter_project(self, path: str = None) -> bool:
        """Verifica si el directorio es un proyecto Flutter"""
        check_dir = path or self.working_dir
        pubspec_path = os.path.join(check_dir, 'pubspec.yaml')
        return os.path.exists(pubspec_path)
    
    def check_flutter_launcher_icons_installed(self, project_dir: str = None) -> bool:
        """Verifica si flutter_launcher_icons está en las dependencias"""
        proj_dir = project_dir or self.working_dir
        pubspec_path = os.path.join(proj_dir, 'pubspec.yaml')
        
        if not os.path.exists(pubspec_path):
            return False
        
        try:
            with open(pubspec_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                return 'flutter_launcher_icons' in content
        except:
            return False
    
    def install_flutter_launcher_icons(self, project_dir: str = None) -> tuple:
        """
        Instala flutter_launcher_icons en el proyecto
        
        Returns:
            Tuple (success: bool, message: str)
        """
        if not self.is_flutter_available():
            return False, "Flutter no está instalado o no se encuentra en PATH"
        
        proj_dir = project_dir or self.working_dir
        
        if not self.is_flutter_project(proj_dir):
            return False, "El directorio no es un proyecto Flutter (no se encontró pubspec.yaml)"
        
        # Añadir dependencia al pubspec.yaml
        result = self._add_dependency_to_pubspec(proj_dir)
        if not result[0]:
            return result
        
        # Ejecutar flutter pub get
        try:
            result = subprocess.run(
                [self.flutter_executable, 'pub', 'get'],
                cwd=proj_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return True, "flutter_launcher_icons instalado correctamente"
            else:
                return False, f"Error al ejecutar flutter pub get: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "Tiempo de espera agotado al instalar dependencias"
        except Exception as e:
            return False, f"Error al instalar: {str(e)}"
    
    def _add_dependency_to_pubspec(self, project_dir: str) -> tuple:
        """Añade flutter_launcher_icons al pubspec.yaml"""
        pubspec_path = os.path.join(project_dir, 'pubspec.yaml')
        
        try:
            with open(pubspec_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Buscar sección dev_dependencies
            dev_deps_idx = None
            for i, line in enumerate(lines):
                if 'dev_dependencies:' in line:
                    dev_deps_idx = i
                    break
            
            if dev_deps_idx is None:
                # Añadir sección dev_dependencies al final
                lines.append('\ndev_dependencies:\n')
                lines.append('  flutter_launcher_icons: ^0.13.1\n')
            else:
                # Verificar si ya está instalado
                content = ''.join(lines).lower()
                if 'flutter_launcher_icons' in content:
                    return True, "Ya está instalado"
                
                # Insertar después de dev_dependencies:
                lines.insert(dev_deps_idx + 1, '  flutter_launcher_icons: ^0.13.1\n')
            
            # Guardar archivo
            with open(pubspec_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            return True, "Dependencia añadida al pubspec.yaml"
            
        except Exception as e:
            return False, f"Error al modificar pubspec.yaml: {str(e)}"
    
    def run_flutter_launcher_icons(
        self,
        project_dir: str = None,
        config_file: str = None
    ) -> tuple:
        """
        Ejecuta flutter_launcher_icons
        
        Args:
            project_dir: Directorio del proyecto Flutter
            config_file: Archivo de configuración YAML (opcional)
            
        Returns:
            Tuple (success: bool, message: str, output: str)
        """
        if not self.is_flutter_available():
            return False, "Flutter no está disponible", ""
        
        proj_dir = project_dir or self.working_dir
        
        if not self.is_flutter_project(proj_dir):
            return False, "No es un proyecto Flutter", ""
        
        # Verificar/instalar flutter_launcher_icons
        if not self.check_flutter_launcher_icons_installed(proj_dir):
            success, msg = self.install_flutter_launcher_icons(proj_dir)
            if not success:
                return False, msg, ""
        
        # Construir comando
        cmd = [
            self.flutter_executable,
            'pub',
            'run',
            'flutter_launcher_icons'
        ]
        
        if config_file:
            cmd.extend(['-f', config_file])
        
        # Ejecutar
        try:
            result = subprocess.run(
                cmd,
                cwd=proj_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            output = result.stdout + "\n" + result.stderr
            
            if result.returncode == 0:
                return True, "Iconos generados exitosamente", output
            else:
                return False, f"Error al generar iconos (código {result.returncode})", output
                
        except subprocess.TimeoutExpired:
            return False, "Tiempo de espera agotado", ""
        except Exception as e:
            return False, f"Error: {str(e)}", ""
    
    def copy_icons_to_project(
        self,
        source_dir: str,
        project_dir: str = None,
        platforms: List[str] = None
    ) -> Dict[str, bool]:
        """
        Copia los iconos generados al proyecto Flutter
        
        Args:
            source_dir: Directorio con los iconos generados
            project_dir: Directorio del proyecto Flutter
            platforms: Lista de plataformas a copiar
            
        Returns:
            Diccionario con el estado de cada copia
        """
        if platforms is None:
            platforms = ['android', 'ios', 'web', 'windows', 'macos']
        
        proj_dir = project_dir or self.working_dir
        results = {}
        
        # Mapeo de directorios
        platform_dirs = {
            'android': ('android', 'android/app/src/main/res'),
            'ios': ('ios', 'ios/Runner/Assets.xcassets/AppIcon.appiconset'),
            'web': ('web', 'web/icons'),
            'windows': ('windows', 'windows/runner/resources'),
            'macos': ('macos', 'macos/Runner/Assets.xcassets/AppIcon.appiconset'),
        }
        
        for platform in platforms:
            if platform not in platform_dirs:
                continue
                
            source_folder = os.path.join(source_dir, platform_dirs[platform][0])
            target_folder = os.path.join(proj_dir, platform_dirs[platform][1])
            
            if not os.path.exists(source_folder):
                results[platform] = False
                continue
            
            try:
                # Crear directorio destino si no existe
                os.makedirs(target_folder, exist_ok=True)
                
                # Copiar archivos
                if platform == 'android':
                    # Copiar estructura de carpetas
                    for item in os.listdir(source_folder):
                        src = os.path.join(source_folder, item)
                        dst = os.path.join(target_folder, item)
                        if os.path.isdir(src):
                            if os.path.exists(dst):
                                shutil.rmtree(dst)
                            shutil.copytree(src, dst)
                        else:
                            shutil.copy2(src, dst)
                else:
                    # Copiar archivos directamente
                    for item in os.listdir(source_folder):
                        src = os.path.join(source_folder, item)
                        if os.path.isfile(src):
                            dst = os.path.join(target_folder, item)
                            shutil.copy2(src, dst)
                
                results[platform] = True
            except Exception as e:
                print(f"Error copiando {platform}: {e}")
                results[platform] = False
        
        return results
    
    def get_flutter_version(self) -> Optional[str]:
        """Obtiene la versión de Flutter instalada"""
        if not self.is_flutter_available():
            return None
        
        try:
            result = subprocess.run(
                [self.flutter_executable, '--version'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Extraer versión de la primera línea
                first_line = result.stdout.strip().split('\n')[0]
                return first_line
            
        except:
            pass
        
        return None
    
    def generate_setup_instructions(self, project_dir: str = None) -> str:
        """Genera instrucciones de configuración"""
        proj_dir = project_dir or self.working_dir
        
        instructions = """
# Configuración de Iconos Flutter

## Opción 1: Uso Manual (Recomendado)

1. Copia las carpetas generadas a tu proyecto:
"""
        
        if os.path.exists(os.path.join(proj_dir, 'pubspec.yaml')):
            instructions += """
   - Copia `android/` → `android/app/src/main/res/`
   - Copia `ios/` → `ios/Runner/Assets.xcassets/`
   - Copia `web/` → `web/icons/`
   - Copia `windows/` → `windows/runner/resources/`
   - Copia `macos/` → `macos/Runner/Assets.xcassets/AppIcon.appiconset/`
"""
        
        instructions += """
## Opción 2: Usando flutter_launcher_icons

1. Asegúrate de tener flutter_launcher_icons instalado:
   ```bash
   flutter pub add --dev flutter_launcher_icons
   ```

2. Usa el archivo `flutter_launcher_icons.yaml` generado en tu proyecto

3. Ejecuta:
   ```bash
   flutter pub run flutter_launcher_icons
   ```

## Archivos Generados
"""
        
        return instructions
