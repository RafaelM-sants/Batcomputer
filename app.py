from flask import Flask, render_template, jsonify
import requests
import psutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

@app.route("/") 
def home():
    try: 
        dolar = requests.get(url="https://economia.awesomeapi.com.br/json/last/USD-BRL")
        dolar_js = dolar.json()
        cotacao_dolar = dolar_js['USDBRL']['bid']
    except requests.exceptions.RequestException:
        cotacao_dolar = "Indisponivel"

    try:
        clima = requests.get(url="https://api.open-meteo.com/v1/forecast?latitude=-23.55&longitude=-46.63&current_weather=true")
        clima_js = clima.json()
        temperatura = clima_js['current_weather']['temperature']
    except requests.exceptions.RequestException:
        temperatura = 'Indisponivel'
  
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disc = psutil.disk_usage('/').percent

    return render_template("index.html", cotacao_dolar=cotacao_dolar, temperatura=temperatura, cpu=cpu, ram=ram, disc=disc)


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


def testar_ip(ip_teste):
    resultado = subprocess.run(["ping", "-c", "1", "-W", "1", ip_teste], stdout=subprocess.DEVNULL)
    if resultado.returncode == 0:
        return ip_teste
    return None

@app.route("/scan-rede")
def scan_rede():
    ip_fix = "192.168.1."
    ips = [ip_fix + str(i) for i in range(1, 255)]

    with ThreadPoolExecutor(max_workers=50) as executor:
        resultados = list(executor.map(testar_ip, ips))

    dispositivos = [ip for ip in resultados if ip is not None]

    return jsonify(dispositivos)

if __name__ == "__main__":
    app.run(debug=True)


