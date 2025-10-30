from architecture.data_access.data_manager import DataManager
import json

manager = DataManager()

codigo = "24CYE-256395"
print(f"🔎 Buscando proyecto: {codigo}\n")

data = manager.fetchProjectData(codigo)

if not data:
    print("❌ Proyecto no encontrado.")
else:
    print("✅ Datos del proyecto e informes asociados:\n")
    print(json.dumps(data, indent=2, ensure_ascii=False))