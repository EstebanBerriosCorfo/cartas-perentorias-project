import json
from architecture.utils.path_utils import PathUtils

"""
architecture/reference/org_structure.py
Módulo de referencia institucional dinámico.
Lee la estructura organizacional desde el mismo directorio donde está el Excel institucional.
"""

class OrgStructure:
    """Gestiona la estructura jerárquica (subdirección / subdirector / ejecutivos)."""

    @classmethod
    def load_structure(cls):
        """Carga la estructura organizacional desde el archivo JSON externo."""
        json_path = PathUtils.get_org_structure_json_path()
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def get_subdirection_for_executive(cls, executive_name: str):
        """Retorna subdirección y subdirector asociados a un ejecutivo."""
        if not executive_name:
            return None

        structure = cls.load_structure()
        exec_name = executive_name.strip().lower()

        for entry in structure:
            for name in entry.get("executives", []):
                if exec_name == name.strip().lower():
                    # Devuelve todos los campos del bloque, menos la lista de ejecutivos
                    return {
                        k: v for k, v in entry.items() if k != "executives"
                    }
        return None