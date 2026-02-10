from architecture.data_access.integration_data_manager import IntegrationDataManager
"""
core/logic.py
Integra la lógica de obtención de datos de proyectos e informes asociados
utilizando IntegrationDataManager sin generar archivos JSON intermedios.
"""
# ─────────────────────────────────────────────
# FUNCIÓN PRINCIPAL: obtener_datos_proyecto
# ─────────────────────────────────────────────
def obtener_datos_proyecto(codigo_proyecto: str) -> dict:
    """
    Obtiene la información consolidada de un proyecto (SOAP + Excel)
    y devuelve los datos esenciales para la interfaz de usuario.
    """
    try:
        integration = IntegrationDataManager()
        data = integration.get_integrated_data(codigo_proyecto)

        # ✅ Ahora usamos la clave correcta (minúscula)
        project_info = data.get("projectinfo", {}) or data.get("projectInfo", {})
        reports = data.get("reports", [])

        # Extraer datos base con las claves reales del JSON
        nombre = project_info.get("projectName", "Sin nombre")
        beneficiario = project_info.get("beneficiaryName", "Sin información")
        representante = project_info.get("legalRepresentative", "No disponible")

        # Obtener informes disponibles
        informes_disponibles = _obtener_informes_disponibles(reports)

        # Log para depuración
        print(f"✅ Proyecto encontrado: {nombre}")
        print(f"👤 Beneficiario: {beneficiario}")
        print(f"📨 Responsable: {representante}")
        print(f"🧾 Informes disponibles: {informes_disponibles}")

        return {
            "nombreProyecto": nombre,
            "beneficiario": beneficiario,
            "representanteLegal": representante,
            "informesDisponibles": informes_disponibles,
        }

    except Exception as e:
        print(f"[ERROR] obtener_datos_proyecto -> {e}")
        raise


# ─────────────────────────────────────────────
# FUNCIÓN AUXILIAR: _obtener_informes_disponibles
# ─────────────────────────────────────────────
def _obtener_informes_disponibles(reports: list) -> list:
    """
    Revisa los informes asociados al proyecto y devuelve solo los que
    tengan un tipo de informe (reportType) válido.
    Si hay fecha de entrega, se considera como informe pendiente.
    """
    informes_disponibles = []

    for report in reports:
        if not isinstance(report, dict):
            continue

        tipo = report.get("reportType", "").strip()
        fecha = report.get("scheduledDeliveryDate", "")
        if isinstance(fecha, str):
            fecha = fecha.strip()
        else:
            fecha = ""

        # Si existe un tipo de informe, se muestra; podrías filtrar más adelante por estado
        if tipo:
            if fecha:
                informes_disponibles.append(f"{tipo} - {fecha}")
            else:
                informes_disponibles.append(f"{tipo} - SIN FECHA")

    if not informes_disponibles:
        informes_disponibles = ["No hay informes disponibles"]

    return informes_disponibles


# ─────────────────────────────────────────────
# TEST LOCAL
# ─────────────────────────────────────────────
if __name__ == "__main__":
    codigo = "24PATI-272023"
    info = obtener_datos_proyecto(codigo)
    import json
    print(json.dumps(info, indent=4, ensure_ascii=False))
