from flask import Flask, request, jsonify, render_template
import json
import os
from openai import OpenAI
#chama o gerar py
from gerar_json import gerar_json
from gerar_cache import gerar_cache

app = Flask(__name__)

# OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =========================
# INDEX
# =========================
@app.route("/")
def index():
    return render_template("index.html")

# =========================
# LOGIN PAGE
# =========================
@app.route("/login")
def login():
    return render_template("login.html")

# =========================
# qwriter 
# =========================
@app.route("/qwriter")
def qwriter():
    return send_from_directory("static","qwriter.html")



@app.route("/escritor")
def  escritor():
    return  send_from_directory("static", "escritor.html")


# =========================
# IA
# =========================
@app.route("/ia", methods=["POST"])
def ia():
    user_text = request.json.get("texto", "")

    cache_path = "static/banco.json"

    if not os.path.exists(cache_path):
        return jsonify({"erro": "static não existe"}), 400

    with open(cache_path, "r", encoding="utf-8") as f:
        banco = json.load(f)

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
