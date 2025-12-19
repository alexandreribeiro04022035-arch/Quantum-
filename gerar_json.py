import os
import json
import requests
# =========================
# CONFIGURAÇÃO SUPABASE
# =========================

SUPABASE_URL = os.getenv("https://lpkhscatjrllfscqmxka.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxwa2hzY2F0anJsbGZzY3FteGthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1NzU3MjYsImV4cCI6MjA3OTE1MTcyNn0.HlNIZFU2kq2-pyq0PgBxFX1Kg1iKldF_Y3thWKzYBnM")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("SUPABASE_URL ou SUPABASE_KEY não definidos")

# 🔽 ESCOLHA EXATAMENTE OS CAMPOS QUE A IA PODE VER
TABLE_URL = (
    f"{SUPABASE_URL}/rest/v1/banco"
    "?select=id,nome,email,saldo,credito,debito,limite,fatura"
)

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
r = requests.get(GITHUB_URL, headers=headers)
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# =========================
# FUNÇÃO PRINCIPAL
# =========================

def gerar_json():
    print("🔑 Conectando ao Supabase...")

    response = requests.get(TABLE_URL, headers=HEADERS)

    if response.status_code != 200:
        print("❌ Erro ao acessar Supabase")
        print(response.text)
        return False

    dados = response.json()

    # garante pasta cache
    os.makedirs("cache", exist_ok=True)

    caminho = "cache/banco.json"

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"✅ Cache gerado com sucesso ({len(dados)} registros)")
    return True


# =========================
# EXECUÇÃO DIRETA
# =========================

if __name__ == "__main__":
    gerar_json()
