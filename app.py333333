from flask import Flask, request, jsonify, render_template, session
import json
import os
import requests
from openai import OpenAI
from gerar_json import gerar_json

app = Flask(__name__)
app.secret_key = "quantum_secret_123"

SUPABASE_URL = "https://lpkhscatjrllfscqmxka.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxwa2hzY2F0anJsbGZzY3FteGthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1NzU3MjYsImV4cCI6MjA3OTE1MTcyNn0.HlNIZFU2kq2-pyq0PgBxFX1Kg1iKldF_Y3thWKzYBnM"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    senha = request.json.get("senha")

    url = f"{SUPABASE_URL}/rest/v1/banco?email=eq.{email}&senha=eq.{senha}"
    r = requests.get(url, headers=headers)

    if not r.json():
        return jsonify({"erro": "Login inválido"}), 401

    session["email"] = email
    gerar_json(email)

    return jsonify({"status": "ok"})

@app.route("/gerar-json", methods=["GET", "POST"])
def rota_gerar_json():
    email = session.get("email")
    if not email:
        return jsonify({"erro": "Não logado"}), 401
    
    gerar_json(email)
    return jsonify({"status": "ok", "msg": "cache atualizado"})

@app.route("/ia", methods=["POST"])
def ia():
    cache_path = "cache/banco.json"

    if not os.path.exists(cache_path):
        return jsonify({"erro": "cache não existe"}), 400

    with open(cache_path, "r", encoding="utf-8") as f:
        banco = json.load(f)

    user_text = request.json.get("texto", "")

    contexto = f"""
Você é a IA do sistema Quantum Invest.
Use APENAS os dados abaixo da tabela banco.
Dados:
{banco}
"""

    resposta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": contexto},
            {"role": "user", "content": user_text}
        ]
    )

    return jsonify({
        "resposta": resposta.choices[0].message.content
    })

if __name__ == "__main__":
    app.run()
