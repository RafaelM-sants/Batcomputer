# Batcomputer

Painel pessoal (dashboard) hospedado no meu servidor doméstico, com o back end em Flask e visual inspirado no Batcomputador do Batman — telas escuras, painéis em HUD, tipografia futurista e detalhes com brilho neon.

O projeto roda na rede local (sem exposição externa) e reúne informações úteis do dia a dia, dados do próprio servidor e módulos pessoais, tudo numa única interface.

> Projeto em desenvolvimento ativo — este README é atualizado conforme o site evolui.

## Status atual

- [x] Estrutura base do Flask (rotas, templates com herança via Jinja2)
- [x] Layout HUD inicial (`base.html` + `style.css`, fontes Orbitron/Share Tech Mono)
- [x] Relógio em tempo real (JavaScript)
- [x] Cotação do dólar (API AwesomeAPI)
- [x] Clima atual (API Open-Meteo)
- [x] Painel de saúde do servidor: uso de CPU, RAM e disco (`psutil`)
- [x] Scanner de dispositivos na rede local, com paralelização via `ThreadPoolExecutor` e exibição assíncrona (`fetch`)
- [ ] Estilização final do card de dispositivos (lista lateral)
- [ ] Lista de tarefas da faculdade e projetos com status (vai exigir banco de dados)
- [ ] Central de botões (executar scripts pré-definidos no servidor)
- [ ] Lista de filmes e séries com notas
- [ ] Página "Sobre mim" com links (Spotify, LinkedIn, GitHub, Instagram etc.)
- [ ] Deploy no servidor doméstico com nginx + WSGI de produção (gunicorn)
- [ ] Cache para dados externos (dólar/clima), evitando requisições repetidas

## Tecnologias

**Back end**
- Python 3
- Flask
- `requests` — consumo de APIs externas
- `psutil` — métricas do sistema (CPU, RAM, disco)
- `concurrent.futures.ThreadPoolExecutor` — paralelização do scan de rede
- `subprocess` — execução de comandos do sistema (ping)

**Front end**
- HTML + Jinja2 (herança de templates)
- CSS puro (variáveis CSS, Flexbox, Grid)
- JavaScript puro (DOM, `fetch`, `setInterval`)
- Google Fonts (Orbitron, Share Tech Mono)

**Infraestrutura (planejado)**
- nginx — servidor web / proxy reverso
- gunicorn — servidor WSGI de produção
- SQLite — persistência da lista de tarefas/projetos e filmes/séries
- Acesso restrito à rede local (sem exposição para a internet)

## APIs utilizadas

- [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas) — cotação do dólar (USD-BRL)
- [Open-Meteo](https://open-meteo.com/) — previsão do tempo

## Estrutura do projeto

```
projeto/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── sobre.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```


## Sobre o projeto

Feito como projeto pessoal de estudo, unindo Flask, front end e conceitos de infraestrutura (servidor doméstico, rede local, nginx). Serve tanto como painel funcional do dia a dia quanto como prática de desenvolvimento web e Python.
