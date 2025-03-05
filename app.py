from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "1a34a19cf008b742705ba2a0bc2a2901"
URL_BASE = "http://api.openweathermap.org/data/2.5/weather"

def obter_temperatura(cidade):
    """ Obtém a temperatura de uma cidade no Brasil. """
    parametros = {
        "q": f"{cidade},BR",
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt"
    }
    resposta = requests.get(URL_BASE, params=parametros)
    dados = resposta.json()

    if resposta.status_code == 200:
        return dados["main"]["temp"]
    return None

def dar_dica(temperatura):
    """ Retorna uma dica com base na temperatura. """
    if temperatura < 15:
        return "Está frio! Use um casaco e tome um café quente. ☕❄️"
    elif 15 <= temperatura <= 25:
        return "Clima agradável! Um passeio ao ar livre seria ótimo. 🌤️🚶‍♂️"
    else:
        return "Está quente! Hidrate-se e use protetor solar. ☀️💧"

@app.route("/", methods=["GET", "POST"])
def index():
    temperatura = None
    dica = None
    cidade = ""

    if request.method == "POST":
        cidade = request.form.get("cidade")
        temperatura = obter_temperatura(cidade)

        if temperatura is not None:
            dica = dar_dica(temperatura)
        else:
            dica = "Cidade não encontrada. Tente novamente."

    return render_template("index.html", temperatura=temperatura, dica=dica, cidade=cidade)

if __name__ == "__main__":
    app.run(debug=True)
