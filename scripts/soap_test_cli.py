import json
import sys

from architecture.data_access.soap_data_manager import SoapDataManager


def _prompt_project_code() -> str:
    try:
        return input("Codigo de proyecto: ").strip()
    except EOFError:
        return ""


def main() -> int:
    project_code = None

    if len(sys.argv) > 1:
        project_code = sys.argv[1].strip()
    else:
        project_code = _prompt_project_code()

    if not project_code:
        print("ERROR: Debes ingresar un codigo de proyecto.")
        return 1

    manager = SoapDataManager()
    data = manager.get_project_data(project_code)

    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
