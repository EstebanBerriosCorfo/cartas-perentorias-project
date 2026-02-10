import pandas as pd
from datetime import datetime, date
import getpass
import platform
import unicodedata

"""
architecture/utils/format_utils.py
Funciones de formateo y compatibilidad para estructuras de datos.
Incluye manejo de Timestamps, fechas, normalización de texto y
conversiones seguras a JSON.
"""

class FormatUtils:
    """Funciones estáticas de utilidad para formateo, fechas y compatibilidad de datos."""

    # ─────────────────────────────────────────────
    # 📅 NORMALIZACIÓN DE FECHAS
    # ─────────────────────────────────────────────
    @staticmethod
    def normalize_date(value):
        """
        Convierte una fecha en formato variable (texto, datetime, Timestamp)
        al formato dd/mm/yyyy. Si no se puede parsear, retorna el valor original.
        """
        if not value:
            return None

        # Si viene como Timestamp de pandas
        if isinstance(value, pd.Timestamp):
            return value.strftime("%d/%m/%Y")

        # Si viene como datetime o date
        if isinstance(value, (datetime, date)):
            return value.strftime("%d/%m/%Y")

        # Si viene como string (diversos formatos)
        possible_formats = [
            "%b %d %Y %I:%M%p",  # Aug 29 2024 11:56AM
            "%b %d %Y",          # Aug 29 2024
            "%Y-%m-%d",          # 2024-11-28
            "%d-%m-%Y",          # 28-11-2024
            "%d/%m/%Y",          # 28/11/2024
            "%Y/%m/%d"           # 2024/11/28
        ]

        for fmt in possible_formats:
            try:
                parsed = datetime.strptime(str(value).strip(), fmt)
                return parsed.strftime("%d/%m/%Y")
            except Exception:
                continue

        return str(value)

    # ─────────────────────────────────────────────
    # 🔄 CONVERSIÓN SEGURA A JSON
    # ─────────────────────────────────────────────
    @staticmethod
    def to_json_serializable(value):
        """
        Convierte un valor a un tipo compatible con JSON.
        - Timestamp / datetime / date → str (YYYY-MM-DD)
        - Otros tipos → se devuelven tal cual
        """
        if isinstance(value, pd.Timestamp):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, (datetime, date)):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, (float, int, str, bool)) or value is None:
            return value
        else:
            return str(value)

    @staticmethod
    def sanitize_dict(data):
        """
        Recorre recursivamente un diccionario o lista y convierte
        todos los valores a tipos compatibles con JSON, aplicando
        normalización de fechas cuando corresponde.
        """
        if isinstance(data, dict):
            clean_dict = {}
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    clean_dict[key] = FormatUtils.sanitize_dict(value)
                elif isinstance(value, (pd.Timestamp, datetime, date)):
                    clean_dict[key] = FormatUtils.normalize_date(value)
                elif isinstance(value, str) and "fecha" in key.lower():
                    clean_dict[key] = FormatUtils.normalize_date(value)
                else:
                    clean_dict[key] = FormatUtils.to_json_serializable(value)
            return clean_dict

        if isinstance(data, list):
            return [FormatUtils.sanitize_dict(v) for v in data]

        return data

    # ─────────────────────────────────────────────
    # 🧩 NORMALIZACIÓN DE CLAVES
    # ─────────────────────────────────────────────
    @staticmethod
    def normalize_key(key: str) -> str:
        """
        Normaliza una clave (minúsculas, sin tildes ni espacios extra).
        Ejemplo: 'Nombre Ejecutivo Técnico ' → 'nombre ejecutivo tecnico'
        """
        if not isinstance(key, str):
            return key
        key = key.strip().lower()
        key = "".join(
            c for c in unicodedata.normalize("NFD", key)
            if unicodedata.category(c) != "Mn"
        )  # elimina tildes
        return key

    # ─────────────────────────────────────────────
    # 🧠 FORMATOS PERSONALIZADOS
    # ─────────────────────────────────────────────
    @staticmethod
    def format_title_case(value):
        """Convierte texto a formato título (Mayúscula en cada palabra)."""
        if not isinstance(value, str):
            return value
        return " ".join(word.capitalize() for word in value.lower().split())

    FORMAT_RULES = {
        "representante legal": format_title_case.__func__,
        "beneficiario comuna": format_title_case.__func__,
        "nombre ejecutivo tecnico": format_title_case.__func__,
        "email representante legal": lambda v: v.lower().strip() if isinstance(v, str) else v
    }

    @staticmethod
    def apply_format_rules(data_dict: dict):
        """
        Aplica reglas de formato (title case, lowercase, etc.)
        según coincidencia flexible de claves.
        """
        if not isinstance(data_dict, dict):
            return data_dict

        new_dict = {}
        for key, value in data_dict.items():
            normalized = FormatUtils.normalize_key(key)
            if normalized in FormatUtils.FORMAT_RULES:
                try:
                    new_value = FormatUtils.FORMAT_RULES[normalized](value)
                    new_dict[key] = new_value
                except Exception:
                    new_dict[key] = value
            else:
                new_dict[key] = value
        return new_dict

    # ─────────────────────────────────────────────
    # 🧾 METADATA PARA TRAZABILIDAD
    # ─────────────────────────────────────────────
    @staticmethod
    def get_metadata(project_code: str, sources: list = None):
        """
        Genera metadatos estándar para trazabilidad del JSON integrado.
        """
        if sources is None:
            sources = ["SOAP", "Excel"]

        return {
            "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": getpass.getuser(),
            "projectCode": project_code,
            "sources": sources,
            "environment": platform.node()
        }
    
    # ─────────────────────────────────────────────
    # 🌐 NORMALIZACIÓN DE CLAVES A camelCase (inglés)
    # ─────────────────────────────────────────────
    @staticmethod
    def normalize_keys_to_camel_case(data):
        """
        Traduce las claves del JSON al inglés y las convierte a camelCase.
        Aplica recursivamente sobre dicts y listas.
        """
        if isinstance(data, list):
            return [FormatUtils.normalize_keys_to_camel_case(i) for i in data]

        if not isinstance(data, dict):
            return data

        # Diccionario de mapeo (Español → Inglés)
        translation_map = {
            # Project Info
            "nombre proyecto": "projectName",
            "nombre beneficiario": "beneficiaryName",
            "representante legal": "legalRepresentative",
            "beneficiario comuna": "beneficiaryCity",
            "fecha postulacion oficial": "officialSubmissionDate",
            "codigo": "projectCode",
            "codigo sistema": "systemCode",
            "nombre ejecutivo tecnico": "technicalExecutiveName",
            "email representante legal": "legalRepresentativeEmail",
            "beneficiario correo": "beneficiaryEmail",
            "director correo": "directorEmail",
            "pro_codigo": "systemProjectCode",
            "pro_resolucion": "resolutionNumber",
            "pro_resolucion_fecha": "resolutionDate",

            # Org Structure (from Excel)
            "subdireccion": "subdirection",
            "subdirector": "subdirector",

            # Reports
            "fecha entrega programada": "scheduledDeliveryDate",
            "periodo informe": "reportPeriod",
            "tipo": "reportType",

            # Metadata
            "generatedat": "generatedAt",
            "user": "user",
            "projectcode": "projectCode",
            "sources": "sources",
            "environment": "environment"
        }

        new_dict = {}
        for key, value in data.items():
            normalized_key = FormatUtils.normalize_key(key)
            new_key = translation_map.get(normalized_key, normalized_key)

            # Aplicar recursivamente si hay estructuras anidadas
            if isinstance(value, (dict, list)):
                new_dict[new_key] = FormatUtils.normalize_keys_to_camel_case(value)
            else:
                new_dict[new_key] = value

        return new_dict