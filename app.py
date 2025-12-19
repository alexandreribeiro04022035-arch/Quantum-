from flask import Flask, request, jsonify, render_template, send_from_directory
import json
import os

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

client = OpenAI(api_key=OPENAI_KEY)

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

@app.route("/miniwriter")
def miniwriter():
    return send_from_directory("static", "miniwriter.html")

@app.route("/writer-owner")
def writer-owner():
    return send_from_directory("static", "writer-owner.html")


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
# IA (CORRIGIDA DE VERDADE)
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

    # 🔥 CORREÇÃO AQUI
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
{contexto}

Usuário:
{user_text}
"""
    )

    return jsonify({
        "resposta": response.output_text
    })

# =========================
# START
# =========================
if __name__ == "__main__":
    app.run()
