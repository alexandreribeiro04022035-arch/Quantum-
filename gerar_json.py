import os
import json
import requests

SUPABASE_URL = os.getenv("https://lpkhscatjrllfscqmxka.supabase.co ")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxwa2hzY2F0anJsbGZzY3FteGthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1NzU3MjYsImV4cCI6MjA3OTE1MTcyNn0.HlNIZFU2kq2-pyq0PgBxFX1Kg1iKldF_Y3thWKzYBnM")

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
