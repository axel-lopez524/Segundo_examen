from flask import Flask


app = Flask(__name__)


@app.get("/")
def inicio():
    return "<h1>Portal de Servicios</h1><p>Aplicación Flask en construcción.</p>"


if __name__ == "__main__":
    app.run(debug=True)
