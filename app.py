from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests
import psutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
import mysql.connector
from config import bd_config, ip_fix

app = Flask(__name__)

#Cria a rota para pagina "/"
@app.route("/") 
def home():

    # 1º PUXAR APIs EXTERNAS

    #API para puxar o valor do dolar (dentro do try except para caso a api externa cair, nao quebrar o site)
    try: 
        #puxa a api externa
        dolar = requests.get(url="https://economia.awesomeapi.com.br/json/last/USD-BRL")
        #converte a resposta da API em um dicionário Python
        dolar_js = dolar.json()
        #seleciona apenas as informações que queros dentro da variavel
        cotacao_dolar = dolar_js['USDBRL']['bid']
    except requests.exceptions.RequestException:
        cotacao_dolar = "Indisponivel"

    #API para puxar o valor do dolar (dentro do try except para caso a api externa cair, nao quebrar o site)
    try:
        #puxa a api externa
        clima = requests.get(url="https://api.open-meteo.com/v1/forecast?latitude=-23.55&longitude=-46.63&current_weather=true")
        #converte a resposta da API em um dicionário Python
        clima_js = clima.json()
        #seleciona apenas as informações que queros dentro da variavel
        temperatura = clima_js['current_weather']['temperature']
    except requests.exceptions.RequestException:
        temperatura = 'Indisponivel'


    #2º PUXA DADOS CPU RAM E DISCO
    cpu = psutil.cpu_percent(interval=1) #interval=1 pede para esperar 1seg para retornar o valor
    ram = psutil.virtual_memory().percent
    disc = psutil.disk_usage('/').percent

    #3 CONEXÃO COM O BANCO DE DADOS (LISTA DE TAREFAS)

    #faz a conexão com meu BD, o "**bd_config" puxa um arquivo confi.py onde tem minhas credenciais de acesso
    conexao = mysql.connector.connect(**bd_config )

    #cria a variavel cursor, é aque realmente execulta os comandos SQL
    cursor = conexao.cursor()
    #define qual comando SQL o cursor vai execultar
    cursor.execute("SELECT * FROM tarefas")
    #cria a variavel que vai exibir o resultado dessa execução 
    tarefas = cursor.fetchall()

    #render template retornar para o html todos esses trablhos que fizemos
    return render_template("index.html", cotacao_dolar=cotacao_dolar, temperatura=temperatura, cpu=cpu, ram=ram, disc=disc, tarefas=tarefas)


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

#Cria a função que testas os ip, se retorna 0 ok se retornar qualquer valor diferente disso none
def testar_ip(ip_teste):
    resultado = subprocess.run(["ping", "-c", "1", "-W", "1", ip_teste], stdout=subprocess.DEVNULL)
    if resultado.returncode == 0:
        return ip_teste
    return None


# cria a rota para o escaner de rede
@app.route("/scan-rede")
def scan_rede():

    #define um ip fixo
    ip_fix
    #pega o ip fixo e adiciona no final numero do 1 ao 254 (todos ips q vamos testar)
    ips = [ip_fix + str(i) for i in range(1, 255)]

    #cria uma thread para ao inves de testar apenas um ip por vez testar varios
    with ThreadPoolExecutor(max_workers=50) as executor:

        #roda a função testar_ip, verifica todos ip de 1 a 254 para ver quais estao conectados
        resultados = list(executor.map(testar_ip, ips))

    #remove da lista os IPs que não responderam (valor None)
    dispositivos = [ip for ip in resultados if ip is not None]

    return jsonify(dispositivos)


@app.route("/formulario", methods=['POST'])
def formulario():
    
    nome = request.form['nome']
    materia = request.form['materia']
    prazo = request.form['prazo']
    tipo = request.form['tipo']
    status = request.form['status']

    conexao = mysql.connector.connect(**bd_config )
    cursor = conexao.cursor()

    cursor.execute('INSERT INTO tarefas (tar_nome, tar_materia, tar_data_conclu, tar_tipo, tar_status) VALUES (%s, %s, %s, %s, %s)',
                   (nome, materia, prazo, tipo, status))

    conexao.commit()

    return redirect(url_for("home"))

@app.route("/alterar_formulario", methods=['POST'])
def atualiza_status():
    tar_id = request.form.get('tar_id', type=int)
    novo_status = request.form.get("status")

    status_permitido = ['Pendente', 'Em andamento', 'Concluido']

    if tar_id is None:
        return 'ID da tarefa invalida', 400 

    if novo_status not in status_permitido:
        return 'Status invalido', 400

    conexao = mysql.connector.connect(**bd_config)
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "" \
            "UPDATE tarefas " \
            "SET tar_status = %s WHERE tar_id = %s",
            (novo_status, tar_id)
        )
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for("home"))


@app.route('/deletar-tarefa', methods=['POST'])
def deleta_tarefa():
    tar_id = request.form.get('tar_id', type=int)
    conexao = mysql.connector.connect(**bd_config )

    cursor = conexao.cursor()

    try:
        cursor.execute (
            'DELETE FROM tarefas WHERE tar_id = %s', (tar_id,)
        )
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)
