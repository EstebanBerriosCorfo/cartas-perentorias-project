from zeep import Client
from zeep.helpers import serialize_object

"""
services/soap_client.py
Módulo de conexión con los servicios SOAP de CORFO (usando zeep).
Provee funciones genéricas para invocar los métodos del WSDL.
"""



WSDL_URL = "http://osblb2.corfo.cl/OSB/PX000451_ConsultaSnapshotSGP?wsdl"


class SoapClient:
    """Cliente SOAP genérico para consumir los métodos del WSDL de CORFO."""

    def __init__(self, wsdl_url=WSDL_URL):
        self.client = Client(wsdl=wsdl_url)

    def get_snapshot_proyectos(self, project_code: str):
        """Obtiene datos generales del proyecto."""
        params = {"PROYECTO": project_code}
        try:
            response = self.client.service.SEL_SNAPSHOT_PROYECTOS(**params)
            return serialize_object(response)
        except Exception as e:
            print(f"❌ Error en SEL_SNAPSHOT_PROYECTOS: {e}")
            return None

    def get_snapshot_informes(self, project_code: str, report_type: str):
        """Obtiene informes asociados al proyecto según tipo."""
        params = {"GERENCIA": "", "PROYECTO": project_code, "TIPO": report_type}
        try:
            response = self.client.service.SEL_SNAPSHOT_INFORMES(**params)
            return serialize_object(response)
        except Exception as e:
            print(f"⚠️ Error en SEL_SNAPSHOT_INFORMES ({report_type}): {e}")
            return None