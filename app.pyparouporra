from flask import Flask, request, jsonify, render_template, send_from_directory
import json
import os
from openai import OpenAI
#from qwriter import qwriter

app = Flask(__name__)

# OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =========================
# ROTAS EXISTENTES
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

# =========================
# ÚNICA ROTA DA IA - LÊ TUDO
# =========================
@app.route("/ia", methods=["POST"])
def ia():
    user_text = request.json.get("texto", "")
    
    # 1. Ler banco.json
    banco_content = ""
    banco_path = "cache/banco.json"
    if os.path.exists(banco_path):
        with open(banco_path, "r", encoding="utf-8") as f:
            banco_content = f.read()
    
    # 2. Ler qwriter.html
    qwriter_content = ""
    qwriter_path = "static/qwriter.html"
    if os.path.exists(qwriter_path):
        with open(qwriter_path, "r", encoding="utf-8") as f:
            qwriter_content = f.read()
    
    # 3. Ler login.html
    login_content = ""
    login_path = "templates/login.html"
    if os.path.exists(login_path):
        with open(login_path, "r", encoding="utf-8") as f:
            login_content = f.read()
    
    contexto = f"""
    Banco: {banco_content}
    Qwriter: {qwriter_content}
    Login: {login_content}
    Pergunta: {user_text}
    """
    
    resposta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": contexto},
            {"role": "user", "content": user_text}
        ]
    )
    
    return jsonify({"resposta": resposta.choices[0].message.content})

if __name__ == "__main__":
    app.run()
