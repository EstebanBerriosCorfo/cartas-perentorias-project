from services.soap_client import SoapClient
import json

"""
architecture/data_access/soap_data_manager.py
Gestiona el consumo de los servicios SOAP y construye un JSON estructurado
con información de proyectos e informes.
"""


class SoapDataManager:
    """Controlador de alto nivel para obtener datos del proyecto desde SOAP."""

    def __init__(self):
        self.client = SoapClient()

    # ─────────────────────────────────────────────
    # PARSEOS DE RESPUESTA SOAP
    # ─────────────────────────────────────────────
    def _parse_rows_to_dict(self, serialized):
        """Convierte la respuesta SOAP (Row/Column) en un diccionario seguro."""
        if not serialized or not isinstance(serialized, list):
            return {}

        first = serialized[0]
        if not isinstance(first, dict) or "Row" not in first:
            return {}

        rows = first.get("Row")
        if not rows:
            return {}

        if isinstance(rows, dict):
            rows = [rows]

        result = {}
        for col in rows[0].get("Column", []):  # solo la primera fila
            name = col.get("name")
            value = col.get("_value_1")
            result[name] = value

        return result

    def _parse_rows_to_list(self, serialized):
        """Convierte la respuesta SOAP (Row/Column) en una lista de dicts segura."""
        if not serialized or not isinstance(serialized, list):
            return []

        first = serialized[0]
        if not isinstance(first, dict) or "Row" not in first:
            return []

        rows = first.get("Row")
        if not rows:
            return []

        if isinstance(rows, dict):
            rows = [rows]

        result = []
        for row in rows:
            item = {}
            for col in row.get("Column", []):
                name = col.get("name")
                value = col.get("_value_1")
                item[name] = value
            result.append(item)

        return result

    # ─────────────────────────────────────────────
    # MÉTODOS PRINCIPALES
    # ─────────────────────────────────────────────
    def get_project_data(self, project_code: str):
        """Obtiene datos generales del proyecto + informes asociados."""
        print(f"\n🔍 Consultando datos del proyecto {project_code}...")

        project_info = self._parse_rows_to_dict(
            self.client.get_snapshot_proyectos(project_code)
        )

        report_types = [
            "INFORME DE AVANCE",
            "INFORME DE GESTIÓN TÉCNICA",
            "INFORME FINAL"
        ]

        reports = []
        for tipo in report_types:
            serialized = self.client.get_snapshot_informes(project_code, tipo)
            items = self._parse_rows_to_list(serialized)

            if items:
                for item in items:
                    item["tipo"] = tipo  # etiqueta de tipo de informe
                    reports.append(item)

        # Devuelve objetos Python puros (no strings)
        return {
            "projectInfo": project_info,
            "reports": reports
        }

    def get_project_data_as_json(self, project_code: str):
        """Devuelve los datos del proyecto en formato JSON formateado."""
        data = self.get_project_data(project_code)
        return json.dumps(data, indent=4, ensure_ascii=False)