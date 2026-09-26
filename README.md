# 🦇 Batcomputer

Painel pessoal (dashboard) hospedado no meu servidor doméstico, com o back end em Flask e visual inspirado no Batcomputador do Batman — telas escuras, painéis em HUD, medidores circulares e detalhes com brilho neon.

O projeto roda na rede local (sem exposição externa) e reúne informações úteis do dia a dia, dados do próprio servidor e módulos pessoais, tudo numa única interface.

> Projeto em desenvolvimento ativo — este README é atualizado conforme o site evolui.

## Status atual

- [x] Estrutura base do Flask (rotas, templates com herança via Jinja2)
- [x] Layout HUD (nav lateral, cabeçalho com leituras em tempo real, símbolo decorativo, rodapé esquemático)
- [x] Relógio em tempo real (JavaScript)
- [x] Cotação do dólar (API AwesomeAPI)
- [x] Clima atual (API Open-Meteo)
- [x] Painel de saúde do servidor: uso de CPU, RAM e disco, exibidos como medidores circulares (SVG)
- [x] Scanner de dispositivos na rede local, com paralelização via `ThreadPoolExecutor` e exibição assíncrona (`fetch`)
- [x] Lista de tarefas da faculdade e projetos pessoais, com banco de dados MySQL
  - [x] Adicionar tarefa (formulário recolhível na própria página)
  - [x] Alterar status de uma tarefa existente
  - [x] Excluir tarefa
  - [x] Cor por status (verde/amarelo/vermelho)
- [ ] Central de botões (executar scripts pré-definidos no servidor)
- [ ] Lista de filmes e séries com notas
- [ ] Página "Sobre mim" com links (Spotify, LinkedIn, GitHub, Instagram etc.)
- [ ] Deploy no servidor doméstico com nginx + gunicorn + systemd
- [ ] Cache para dados externos (dólar/clima), evitando requisições repetidas

## Tecnologias

**Back end**
- Python 3
- Flask
- `requests` — consumo de APIs externas
- `psutil` — métricas do sistema (CPU, RAM, disco)
- `concurrent.futures.ThreadPoolExecutor` — paralelização do scan de rede
- `subprocess` — execução de comandos do sistema (ping)
- `mysql-connector-python` — conexão com o banco MySQL

**Front end**
- HTML + Jinja2 (herança de templates, `{% for %}`, `{% if %}`)
- CSS puro (variáveis CSS, Flexbox, medidores circulares em SVG)
- JavaScript puro (DOM, `fetch`, `setInterval`)
- Google Fonts (Orbitron, Share Tech Mono)

**Banco de dados**
- MySQL — tabela `tarefas` (nome, matéria/projeto, status, prazo, tipo)

**Infraestrutura (planejado)**
- nginx — servidor web / proxy reverso
- gunicorn — servidor WSGI de produção
- systemd — manter a aplicação rodando como serviço, mesmo após reiniciar o servidor
- Acesso restrito à rede local (sem exposição para a internet)

## APIs utilizadas

- [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas) — cotação do dólar (USD-BRL)
- [Open-Meteo](https://open-meteo.com/) — previsão do tempo

## Estrutura do projeto

```
projeto/
├── app.py
├── config_exemplo.py
├── config.py            # não versionado (.gitignore) — suas credenciais reais
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   └── sobre.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── img/
        └── bat-symbol.png
```

## Configuração

1. Crie um ambiente virtual e ative-o:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Copie o arquivo de exemplo de configuração e preencha com suas credenciais reais:
   ```bash
   cp config_exemplo.py config.py
   ```
   Edite `config.py` com o usuário/senha do seu MySQL e a faixa de IP da sua rede local (`ip_fix`).

4. Crie o banco de dados e a tabela `tarefas` no MySQL (ver seção "Banco de dados" abaixo).

## Banco de dados

```sql
CREATE DATABASE batcomputer;
USE batcomputer;

CREATE TABLE tarefas (
    tar_id INT PRIMARY KEY AUTO_INCREMENT,
    tar_nome VARCHAR(30) NOT NULL,
    tar_materia VARCHAR(30),
    tar_status VARCHAR(30) NOT NULL DEFAULT 'Pendente',
    tar_data_conclu DATE,
    tar_tipo VARCHAR(20) NOT NULL,
    CONSTRAINT ck_tarefa_status CHECK (tar_status IN ('Pendente', 'Em andamento', 'Concluido')),
    CONSTRAINT ck_tarefa_tipo CHECK (tar_tipo IN ('Faculdade', 'Projeto'))
);
```

## Rodando localmente

```bash
python3 app.py
```

Acesse `http://127.0.0.1:5000`.

> Observação: o scanner de rede (`/scan-rede`) usa a faixa de IP definida em `config.py` (`ip_fix`). Ajuste conforme a faixa de IP da sua própria rede.

## Sobre o projeto

Feito como projeto pessoal de estudo, unindo Flask, front end, banco de dados e conceitos de infraestrutura (servidor doméstico, rede local, nginx). Serve tanto como painel funcional do dia a dia quanto como prática de desenvolvimento web e Python.