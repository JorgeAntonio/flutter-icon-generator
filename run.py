#!/usr/bin/env python3
"""
Entry point para desarrollo
Activa el entorno virtual automaticamente si existe
"""

import sys
import os

# Activar entorno virtual si existe
venv_path = os.path.join(os.path.dirname(__file__), 'venv')
if os.path.exists(venv_path):
    if sys.platform == 'win32':
        site_packages = os.path.join(venv_path, 'Lib', 'site-packages')
    else:
        site_packages = os.path.join(venv_path, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages')
    
    if site_packages not in sys.path:
        sys.path.insert(0, site_packages)

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    main()
