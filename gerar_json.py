import os
import json
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

TABLE = "banco"
OUTPUT_FILE = "cache/banco.json"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def gerar_json():
    url = f"{SUPABASE_URL}/rest/v1/{TABLE}?select=*"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise Exception(f"Erro Supabase: {r.text}")

    dados = r.json()

    os.makedirs("cache", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"JSON gerado com sucesso ({len(dados)} registros)")

if __name__ == "__main__":
    gerar_json()
