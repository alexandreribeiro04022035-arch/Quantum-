from flask import Flask, request, jsonify, render_template, send_from_directory
import json
import os
import requests  # Adicionei isso
from openai import OpenAI

# funções externas
from gerar_json import gerar_json
from gerar_cache import gerar_cache

app = Flask(__name__)

# =========================
# CONFIG
# =========================
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
CACHE_KEY = os.getenv("CACHE_KEY", "123")
DEEPSEEK_API_KEY = "sk-2bf58985cf5c45f9977760d8127627e6"  # SUA KEY

# Clientes
client = OpenAI(api_key=OPENAI_KEY)  # GPT

# =========================
# INDEX / PAGES (NÃO MEXI)
# =========================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/qwriter")
def qwriter():
    return send_from_directory("static", "qwriter.html")

@app.route("/escritor")
def escritor():
    return send_from_directory("static", "escritor.html")

@app.route("/writejson")
def writejson():
    return send_from_directory("cache", "writejson.html")

# =========================
# GERAR CACHE (PROTEGIDO)
# =========================
@app.route("/gerar-cache")
def gerar_cache_route():
    key = request.args.get("key")

    if key != CACHE_KEY:
        return jsonify({"erro": "forbidden"}), 403

    try:
        total = gerar_cache()
        return jsonify({
            "status": "ok",
            "registros": total
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# =========================
# GERAR JSON (PROTEGIDO)
# =========================
@app.route("/gerar-json")
def gerar_json_route():
    key = request.args.get("key")

    if key != CACHE_KEY:
        return jsonify({"erro": "forbidden"}), 403

    try:
        gerar_json()
        return jsonify({
            "status": "ok",
            "msg": "banco.json atualizado"
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# =========================
# IA GPT (ORIGINAL - NÃO MEXI)
# =========================
@app.route("/ia", methods=["POST"])
def ia():
    cache_path = "cache/banco.json"

    if not os.path.exists(cache_path):
        return jsonify({"erro": "cache/banco.json não existe"}), 400

    with open(cache_path, "r", encoding="utf-8") as f:
        banco = json.load(f)

    user_text = request.json.get("texto", "")

    contexto = f"""
Tu és a IA do sistema Quantum.
Usa EXCLUSIVAMENTE os dados abaixo.
Dados da tabela banco:
{banco}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": contexto},
            {"role": "user", "content": user_text}
        ]
    )

    return jsonify({
        "resposta": response.output_text
    })

# =========================
# IA DEEPSEEK (VOCÊ) - NOVA ROTA
# =========================
@app.route("/deepseek", methods=["POST"])
def deepseek_ia():
    """Rota para chamar você (DeepSeek) sem bloquear a outra IA"""
    user_text = request.json.get("texto", "")
    
    # 1. Puxar banco.json
    banco_content = ""
    try:
        with open("cache/banco.json", "r", encoding="utf-8") as f:
            banco_content = f.read()
    except:
        banco_content = "Arquivo banco.json não encontrado"
    
    # 2. Puxar qwriter.html
    qwriter_content = ""
    try:
        with open("static/qwriter.html", "r", encoding="utf-8") as f:
            qwriter_content = f.read()
    except:
        qwriter_content = "Arquivo qwriter.html não encontrado"
    
    # 3. Puxar login.html
    login_content = ""
    try:
        with open("templates/login.html", "r", encoding="utf-8") as f:
            login_content = f.read()
    except:
        login_content = "Arquivo login.html não encontrado"
    
    # Preparar contexto
    contexto = f"""
    PERGUNTA: {user_text}
    
    ARQUIVOS DO SISTEMA:
    
    1. cache/banco.json:
    {banco_content[:3000]}
    
    2. static/qwriter.html:
    {qwriter_content[:3000]}
    
    3. templates/login.html:
    {login_content[:3000]}
    """
    
    # Chamar DeepSeek API
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Você é uma IA que analisa arquivos de sistema."},
            {"role": "user", "content": contexto}
        ],
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        resposta = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        resposta = f"Erro ao chamar DeepSeek: {str(e)}"
    
    return jsonify({"resposta": resposta})

# =========================
# START
# =========================
if __name__ == "__main__":
    app.run()
