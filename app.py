from flask import Flask, request, jsonify, render_template
import json
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# rota principal
@app.route("/")
def index():
    return render_template("index.html")

# rota da IA
@app.route("/ia", methods=["POST"])
def ia():
    user_text = request.json.get("texto", "")

    # lê o JSON cache
    with open("cache/banco.json", "r", encoding="utf-8") as f:
        banco = json.load(f)

    contexto = f"""
    Você é a IA do sistema Quantum Invest.
    Estes são os dados disponíveis da tabela banco:
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

from gerar_json import gerar_json

@app.route("/gerar-json", methods=["GET"])
def rota_gerar_json():
    gerar_json()
    return {"status": "ok"}



if __name__ == "__main__":
    app.run()
