from architecture.data_access.soap_data_manager import SoapDataManager
from architecture.data_access.excel_data_manager import ExcelDataManager
from architecture.utils.format_utils import FormatUtils
from architecture.reference.org_structure import OrgStructure
import json

"""
architecture/data_access/integration_data_manager.py
Integra los resultados de los módulos SOAP y Excel en un único JSON consolidado.
Aplica reglas de formato, normalización de fechas (projectInfo + reports)
y genera metadatos técnicos.
"""

class IntegrationDataManager:
    """Fusiona la información de SOAP y Excel para generar un JSON integrado."""

    def __init__(self):
        self.soap_manager = SoapDataManager()
        self.excel_manager = ExcelDataManager()

    # ─────────────────────────────────────────────
    # 🔹 MÉTODO PRINCIPAL
    # ─────────────────────────────────────────────
    def get_integrated_data(self, project_code: str):
        """
        Obtiene datos desde SOAP y Excel, los integra y aplica reglas de formato y limpieza.
        Retorna un diccionario listo para serialización JSON.
        """
        print(f"\n🔍 Obteniendo datos integrados para proyecto {project_code}...")

        # 1️⃣ Obtener datos desde ambas fuentes
        soap_data = self.soap_manager.get_project_data(project_code)
        excel_data = self.excel_manager.get_project_data(project_code)

        # 2️⃣ Fusionar datos base (prioriza Excel si hay claves repetidas)
        project_info = {**soap_data.get("projectInfo", {}), **excel_data}

        # 3️⃣ Aplicar reglas de formato específicas (nombres, correos, etc.)
        project_info = FormatUtils.apply_format_rules(project_info)

        # 4️⃣ Normalizar fechas en projectInfo
        project_info = {
            k: FormatUtils.normalize_date(v) if "fecha" in k.lower() else v
            for k, v in project_info.items()
        }

        # 4️⃣.1️⃣ Enriquecer con datos de Subdirección/Subdirector
        executive_name = project_info.get("Nombre Ejecutivo Técnico")
        org_data = OrgStructure.get_subdirection_for_executive(executive_name)

        if org_data:
            # Fusiona dinámicamente todos los campos definidos en org_structure.json
            project_info.update(org_data)

        # 5️⃣ Normalizar fechas en reports
        reports = soap_data.get("reports", [])
        clean_reports = []
        for report in reports:
            if isinstance(report, dict):
                clean_report = {
                    k: FormatUtils.normalize_date(v) if "fecha" in k.lower() else v
                    for k, v in report.items()
                }
                clean_reports.append(clean_report)
            else:
                clean_reports.append(report)

        # 6️⃣ Construir estructura integrada
        integrated = {
            "projectCode": project_code,
            "projectInfo": project_info,
            "reports": clean_reports,
            "metadata": FormatUtils.get_metadata(project_code, ["SOAP", "Excel"])
        }

        # 7️⃣ Limpieza final y serialización segura
        clean_data = FormatUtils.sanitize_dict(integrated)
        clean_data = FormatUtils.normalize_keys_to_camel_case(clean_data)
        return clean_data

    # ─────────────────────────────────────────────
    # 🔹 MÉTODO PARA EXPORTAR COMO JSON FORMATEADO
    # ─────────────────────────────────────────────
    def get_integrated_data_as_json(self, project_code: str):
        """
        Devuelve los datos integrados en formato JSON legible (UTF-8 y formateado).
        """
        data = self.get_integrated_data(project_code)
        json_output = json.dumps(data, indent=4, ensure_ascii=False)
        return json_output
