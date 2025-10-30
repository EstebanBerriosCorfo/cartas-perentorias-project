from architecture.data_access.database_connector import DatabaseConnector

try:
    print("🔄 Conectando a la base de datos Mirror_PowerB ...")
    query = "SELECT TOP 5 * FROM dbo.GER_INN_SNAPSHOT_PROYECTOS;"
    df = DatabaseConnector.executeQuery(query)
    print("✅ Conexión exitosa.")
    print(df.head())
except Exception as e:
    print("❌ Error en la conexión:", e)