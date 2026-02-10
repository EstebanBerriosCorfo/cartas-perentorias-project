"""
scripts/soap_query.py
Script CLI para consultar el servicio SOAP de CORFO por código de proyecto.

Uso:
    python scripts/soap_query.py 24CVIS-255755
    python scripts/soap_query.py 24CVI-264866 --informes
"""

import sys
import json
import os

# Asegurar que se puede importar desde la raíz del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.soap_client import SoapClient
from architecture.data_access.soap_data_manager import SoapDataManager


def consultar_proyecto(project_code: str, incluir_informes: bool = False):
    """Consulta datos del proyecto vía SOAP y los imprime en formato JSON."""
    data_manager = SoapDataManager()

    # ─────────────────────────────────────────────
    # 1️⃣ Datos generales del proyecto
    # ─────────────────────────────────────────────
    print(f"\n🔍 Consultando proyecto: {project_code}\n")
    print("=" * 60)
    print("📋 DATOS GENERALES DEL PROYECTO")
    print("=" * 60)

    data = data_manager.get_project_data(project_code)
    project_info = data.get("projectInfo", {})

    if not project_info:
        print("❌ No se obtuvieron datos del proyecto.")
        return

    # Mostrar datos del proyecto ordenados por clave
    ordered_project = dict(sorted(project_info.items(), key=lambda x: x[0]))
    print(json.dumps(ordered_project, indent=4, ensure_ascii=False, default=str))

    # ─────────────────────────────────────────────
    # 2️⃣ Informes asociados (opcional)
    # ─────────────────────────────────────────────
    if incluir_informes:
        reports = data.get("reports", [])

        if not reports:
            print("\n(no se encontraron informes asociados)")
            return

        # Agrupar por tipo para mostrar ordenado
        grouped = {}
        for item in reports:
            tipo = item.get("tipo", "SIN TIPO")
            grouped.setdefault(tipo, []).append(item)

        for tipo in sorted(grouped.keys()):
            print(f"\n{'=' * 60}")
            print(f"📄 {tipo}")
            print("=" * 60)
            ordered_items = [
                dict(sorted(report.items(), key=lambda x: x[0])) for report in grouped[tipo]
            ]
            print(json.dumps(ordered_items, indent=4, ensure_ascii=False, default=str))


if __name__ == "__main__":
    codigo = None
    if len(sys.argv) >= 2:
        codigo = sys.argv[1]
    else:
        codigo = input("Ingrese el código de proyecto a consultar: ").strip()

    if not codigo:
        print("❌ Debe ingresar un código de proyecto válido.")
        sys.exit(1)

    # Siempre consultar informes asociados
    consultar_proyecto(codigo, True)
