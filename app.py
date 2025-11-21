from flask import Flask, render_template

app = Flask(__name__, 
    template_folder="templates",
    static_folder="static"
)

@app.route("/")
def index():
    return render_template("index.html")

# Rota para servir arquivos estáticos (CSS, JS, imagens)
@app.route("/static/<path:filename>")
def serve_static(filename):
    return app.send_static_file(filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
