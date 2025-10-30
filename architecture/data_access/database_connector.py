import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

"""
DatabaseConnector: Gestiona la conexión a SQL Server (Mirror_PowerB)
usando SQLAlchemy + pyodbc, con configuración específica para entorno CORFO.
"""

class DatabaseConnector:
    """
    Conector hacia SQL Server (Mirror_PowerB).
    """

    server: str = r"ddssql2k6-avs\PROD7"
    database: str = "Mirror_PowerB"
    driver: str = "ODBC Driver 18 for SQL Server"
    _engine: Engine | None = None

    @classmethod
    def getEngine(cls) -> Engine:
        """
        Crea (si no existe) y retorna un Engine de SQLAlchemy
        configurado para Mirror_PowerB con Trusted Connection.
        """
        if cls._engine is not None:
            return cls._engine

        # Armamos la cadena de conexión compatible con SQLAlchemy
        driver_enc = cls.driver.replace(" ", "+")
        connection_string = (
            f"mssql+pyodbc://@{cls.server}/{cls.database}"
            f"?driver={driver_enc}"
            "&Encrypt=no"
            "&TrustServerCertificate=yes"
            "&Trusted_Connection=yes"
            "&charset=utf8"
        )

        cls._engine = create_engine(connection_string, fast_executemany=True, future=True)
        return cls._engine

    @classmethod
    def executeQuery(cls, query: str) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL y retorna un DataFrame de pandas.
        """
        engine = cls.getEngine()
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
        return df