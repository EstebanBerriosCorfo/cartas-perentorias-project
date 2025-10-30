import pandas as pd
from typing import Dict, Any, List
from .database_connector import DatabaseConnector

"""
DataManager: Une información de las vistas de Mirror_PowerB
(GER_INN_SNAPSHOT_PROYECTOS, GER_INN_SNAPSHOT_INFORMES, GER_INN_SNAPSHOT_PROYECTOS_COMITE)
y entrega los datos de un proyecto consolidado.
"""

class DataManager:
    """
    Gestiona la obtención y consolidación de datos de proyectos desde Mirror_PowerB.
    Retorna un objeto JSON con estructura jerárquica: projectInfo + reports.
    """

    def fetchProjectData(self, projectCode: str) -> Dict[str, Any]:
        """
        Retorna un diccionario estructurado con:
        - projectInfo: datos generales del proyecto (de PROYECTOS y COMITE)
        - reports: lista de informes asociados (de INFORMES)
        """

        projectCode = projectCode.strip()
        engine = DatabaseConnector.getEngine()

        # ─────────────────────────────────────────────
        # 1️⃣ Datos generales del proyecto (PROYECTOS + COMITE)
        # ─────────────────────────────────────────────
        query_project = """
            SELECT
                p.[Código] AS codigoProyecto,
                p.[Código Sistema] AS codigoSistema,
                p.[Nombre Ejecutivo Técnico] AS nombreEjecutivoTecnico,
                p.[Gerencia] AS nombreGerencia,
                p.[Fecha Resolucion] AS fechaResolucion,
                p.[Nombre Proyecto] AS nombreProyecto,
                p.[Nombre Beneficiario] AS nombreBeneficiario,
                p.[Estado Proyecto] AS estadoProyecto,
                p.[Representante Legal] AS nombreRepresentante,
                p.[Email representante legal] AS representativeEmail,
                p.[Fecha Inicio Versión Vigente] AS fechaInicio,
                p.[Fecha Termino Versión Vigente] AS fechaTermino,
                p.[Estado de informe final] AS estadoInformeFinal,
                c.[pro_resolucion] AS resolucionNumero,
                c.[pro_resolucion_fecha] AS resolucionFecha
            FROM dbo.GER_INN_SNAPSHOT_PROYECTOS p
            LEFT JOIN dbo.GER_INN_SNAPSHOT_PROYECTOS_COMITE c
                ON p.[Código Sistema] = c.[pro_codigo]
            WHERE p.[Código] = ?
        """

        df_project = pd.read_sql(query_project, engine, params=(projectCode,))

        if df_project.empty:
            return {}

        proj = df_project.iloc[0].fillna("")

        projectInfo = {
            "projectCode": proj.get("codigoProyecto", ""),
            "systemCode": proj.get("codigoSistema", ""),
            "projectName": proj.get("nombreProyecto", ""),
            "beneficiaryName": proj.get("nombreBeneficiario", ""),
            "representativeName": proj.get("nombreRepresentante", ""),
            "representativeEmail": proj.get("representativeEmail", ""),
            "executiveName": proj.get("nombreEjecutivoTecnico", ""),
            "management": proj.get("nombreGerencia", ""),
            "projectStatus": proj.get("estadoProyecto", ""),
            "resolutionNumber": str(proj.get("resolucionNumero", "")),
            "resolutionDate": str(proj.get("resolucionFecha", "")),
            "resolutionDateOriginal": str(proj.get("fechaResolucion", "")),
            "startDate": str(proj.get("fechaInicio", "")),
            "endDate": str(proj.get("fechaTermino", "")),
            "reportFinalStatus": str(proj.get("estadoInformeFinal", ""))
        }

        # ─────────────────────────────────────────────
        # 2️⃣ Lista de informes asociados
        # ─────────────────────────────────────────────
        query_reports = """
            SELECT
                i.[Nombre de Informe] AS nombreInforme,
                i.[Tipo de Informe] AS tipoInforme,
                i.[Estado de informe] AS estadoInforme,
                i.[Fecha Entrega Programada] AS fechaEntregaProgramada
            FROM dbo.GER_INN_SNAPSHOT_INFORMES i
            WHERE i.[Código de Proyecto] = ?
            ORDER BY i.[Fecha Entrega Programada]
        """

        df_reports = pd.read_sql(query_reports, engine, params=(projectCode,))

        reports = []
        if not df_reports.empty:
            df_reports = df_reports.fillna("")
            for _, row in df_reports.iterrows():
                reports.append({
                    "reportName": row["nombreInforme"],
                    "reportType": row["tipoInforme"],
                    "reportStatus": row["estadoInforme"],
                    "reportDueDate": str(row["fechaEntregaProgramada"])
                })

        # ─────────────────────────────────────────────
        # 3️⃣ Retornar estructura final
        # ─────────────────────────────────────────────
        return {
            "projectInfo": projectInfo,
            "reports": reports
        }