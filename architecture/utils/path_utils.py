from datetime import datetime
import os
import sys
from tkinter import filedialog, messagebox
"""
architecture/utils/path_utils.py
Utilidades para la gestión de rutas institucionales y locales.
Compatible con OneDrive CORFO, modo desarrollo y ejecutable PyInstaller.
"""


class PathUtils:
    """Clase de utilidades para obtener rutas institucionales y de sistema."""

    # ─────────────────────────────────────────────
    # 🔧 RUTAS BASE
    # ─────────────────────────────────────────────
    @staticmethod
    def get_base_dir():
        """
        Devuelve la ruta base correcta tanto en entorno de desarrollo como en ejecutable (PyInstaller).
        """
        if hasattr(sys, "_MEIPASS"):  # Cuando está empaquetado como .exe
            return sys._MEIPASS
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # /architecture/utils → /architecture

    @staticmethod
    def get_user_folder():
        return os.path.expanduser("~")

    # ─────────────────────────────────────────────
    # 📂 RUTAS ESPECÍFICAS DE ONEDRIVE CORFO
    # ─────────────────────────────────────────────
    @staticmethod
    def get_onedrive_root():
        """
        Devuelve la ruta base del OneDrive institucional (si existe).
        """
        user_folder = PathUtils.get_user_folder()
        onedrive_path = os.path.join(user_folder, "OneDrive - corfo.cl")
        if os.path.exists(onedrive_path):
            return onedrive_path
        return None

    @staticmethod
    def get_innovachile_folder():
        """Devuelve la ruta a la carpeta principal de InnovaChile en OneDrive."""
        root = PathUtils.get_onedrive_root()
        if root:
            folder = os.path.join(root, "InnovaChile - General")
            if os.path.exists(folder):
                return folder
        return None

    # ─────────────────────────────────────────────
    # 📊 ARCHIVOS INSTITUCIONALES
    # ─────────────────────────────────────────────
    @staticmethod
    def get_cartasperentorias_excel_path():
        """
        Devuelve la ruta al archivo institucional 'datos_finales_cartasp.xlsx'.
        Si no se encuentra, permite al usuario seleccionarlo manualmente.
        """
        base_folder = PathUtils.get_innovachile_folder()
        if not base_folder:
            messagebox.showwarning("Ruta OneDrive no encontrada", "No se encontró la carpeta 'InnovaChile - General'.")
            return filedialog.askopenfilename(
                title="Seleccionar archivo datos_finales_cartasp.xlsx",
                filetypes=[("Excel Files", "*.xlsx *.xls")]
            )

        ruta_excel = os.path.join(base_folder, "Base Cartas Perentorias", "datos_finales_cartasp.xlsx")
        if os.path.exists(ruta_excel):
            return ruta_excel

        # Si no existe, permitir selección manual
        respuesta = messagebox.askyesno(
            "Archivo no encontrado",
            f"No se encontró el archivo datos_finales_cartasp.xlsx en:\n\n{ruta_excel}\n\n¿Deseas buscarlo manualmente?"
        )
        if respuesta:
            ruta = filedialog.askopenfilename(
                title="Seleccionar archivo datos_finales_cartasp.xlsx",
                filetypes=[("Excel Files", "*.xlsx *.xls")]
            )
            if ruta:
                return ruta

        raise FileNotFoundError("No se pudo localizar el archivo datos_finales_cartasp.xlsx.")

    # ─────────────────────────────────────────────
    # 📥 CARPETA DESCARGAS Y ASSETS
    # ─────────────────────────────────────────────
    @staticmethod
    def get_downloads_folder():
        """Devuelve la ruta de Descargas del usuario."""
        return os.path.join(PathUtils.get_user_folder(), "Downloads")

    @staticmethod
    def get_assets_folder():
        """Devuelve la ruta de la carpeta de recursos (assets) del proyecto."""
        return os.path.join(PathUtils.get_base_dir(), "assets")


# ─────────────────────────────────────────────
# 📝 RUTAS DE DESCARGA DE CARTAS GENERADAS
# ─────────────────────────────────────────────

def generate_download_path(project_code: str, letter_type: str) -> str:
    """
    Genera una ruta de salida en la carpeta 'Descargas' con nombre estructurado:
    <project_code>_Carta_<letter_type>_<fecha>.docx

    Args:
        project_code (str): Código del proyecto (ej. "24CVI-264677")
        letter_type (str): Tipo de carta (ej. "perentoria" o "incumplimiento")

    Returns:
        str: Ruta completa donde se guardará el documento generado.
    """
    # Fecha y hora exacta para evitar sobrescribir
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Nombre del archivo
    file_name = f"{project_code}_Carta_{letter_type.capitalize()}_{date_str}.docx"
    # Carpeta Descargas del usuario
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    # Ruta completa del archivo
    return os.path.join(downloads_dir, file_name)