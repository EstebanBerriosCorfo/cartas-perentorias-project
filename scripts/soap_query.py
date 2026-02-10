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


def consultar_proyecto(project_code: str, incluir_informes: bool = False):
    """Consulta datos del proyecto vía SOAP y los imprime en formato JSON."""
    client = SoapClient()

    # ─────────────────────────────────────────────
    # 1️⃣ Datos generales del proyecto
    # ─────────────────────────────────────────────
    print(f"\n🔍 Consultando proyecto: {project_code}\n")
    print("=" * 60)
    print("📋 DATOS GENERALES DEL PROYECTO")
    print("=" * 60)

    response = client.get_snapshot_proyectos(project_code)

    if not response:
        print("❌ No se obtuvieron datos del proyecto.")
        return

    print(json.dumps(response, indent=4, ensure_ascii=False, default=str))

    # ─────────────────────────────────────────────
    # 2️⃣ Informes asociados (opcional)
    # ─────────────────────────────────────────────
    if incluir_informes:
        report_types = [
            "INFORME DE AVANCE",
            "INFORME DE GESTIÓN TÉCNICA",
            "INFORME FINAL"
        ]

        for tipo in report_types:
            print(f"\n{'=' * 60}")
            print(f"📄 {tipo}")
            print("=" * 60)

            response = client.get_snapshot_informes(project_code, tipo)
            if response:
                print(json.dumps(response, indent=4, ensure_ascii=False, default=str))
            else:
                print("  (sin datos)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/soap_query.py <CÓDIGO_PROYECTO> [--informes]")
        print("Ejemplo: python scripts/soap_query.py 24CVIS-255755 --informes")
        sys.exit(1)

    codigo = sys.argv[1]
    con_informes = "--informes" in sys.argv

    consultar_proyecto(codigo, con_informes)
