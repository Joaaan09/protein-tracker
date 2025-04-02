import subprocess
import json
import sys
import os

def run_scrapper(script_name):
    try:
        # Ruta absoluta al script
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        print(f"Executant {script_path}...", file=sys.stderr)  # Depuració
        
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True
        )
        print(f"Sortida de {script_name}:", file=sys.stderr)  # Depuració
        print(result.stdout, file=sys.stderr)  # Depuració
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error executant {script_name}: {e}", file=sys.stderr)  # Depuració
        return {"error": str(e)}

if __name__ == "__main__":
    scrapers = ["myprotein.py", "prozis.py"]
    data = {}

    for scrapper in scrapers:
        try:
            print(f"Processant {scrapper}...", file=sys.stderr)  # Depuració
            data[scrapper.replace(".py", "")] = run_scrapper(scrapper)
        except Exception as e:
            print(f"Error processant {scrapper}: {e}", file=sys.stderr)  # Depuració
            data[scrapper.replace(".py", "")] = {"error": str(e)}
    result = data;
    print(json.dumps(data, ensure_ascii=False))  # Evita problemes d'encoding

