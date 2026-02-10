import os
import pandas as pd
from tkinter import messagebox, filedialog
from architecture.utils.path_utils import PathUtils
"""
architecture/data_access/excel_data_manager.py
Lee el archivo Excel institucional 'datos_finales_cartasp.xlsx'
y devuelve la información del proyecto filtrada por el código.
"""




class ExcelDataManager:
    """Maneja la lectura y filtrado del archivo Excel institucional."""

    def __init__(self):
        # Obtiene ruta usando PathUtils
        self.excel_path = PathUtils.get_cartasperentorias_excel_path()

    def get_project_data(self, project_code: str):
        """
        Lee el Excel y filtra por código de proyecto.
        Retorna un diccionario con los campos relevantes.
        """
        if not os.path.exists(self.excel_path):
            raise FileNotFoundError(f"No se encontró el archivo: {self.excel_path}")

        df = pd.read_excel(self.excel_path)

        if "Código" not in df.columns:
            raise ValueError("El archivo Excel no contiene la columna 'Código'.")

        filtered = df[df["Código"].astype(str).str.strip() == project_code.strip()]
        if filtered.empty:
            messagebox.showinfo("Proyecto no encontrado", f"No se encontró el código: {project_code}")
            return {}

        # No eliminamos los NaN para mantener todas las columnas relevantes
        data_dict = filtered.iloc[0].to_dict()

        # Campos que queremos incluir siempre
        selected_fields = [
            "Código",
            "Código Sistema",
            "Nombre Ejecutivo Técnico",
            "Subdirección",
            "Subdirector",
            "Email representante legal",
            "Beneficiario correo",
            "Director correo",
            "pro_codigo",
            "pro_resolucion",
            "pro_resolucion_fecha"
        ]

        filtered_dict = {k: (None if pd.isna(v) else v) for k, v in data_dict.items() if k in selected_fields}
        return filtered_dict