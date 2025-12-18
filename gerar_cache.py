import os, json, requests

SUPABASE_URL = os.getenv("https://lpkhscatjrllfscqmxka.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

URL = f"{SUPABASE_URL}/rest/v1/banco?select=id,nome,email,saldo,credito,debito"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def gerar_cache():
    r = requests.get(URL, headers=headers)

    if r.status_code != 200:
        raise Exception(r.text)

    dados = r.json()

    os.makedirs("cache", exist_ok=True)
    with open("cache/banco.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return len(dados)
