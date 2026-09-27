function atualizarRelogio() {
    const relogio = document.getElementById('clock');
    const agora = new Date();
    const horas = String(agora.getHours()).padStart(2, '0');
    const minutos = String(agora.getMinutes()).padStart(2, '0');
    const segundos = String(agora.getSeconds()).padStart(2, '0');

    relogio.textContent = `${horas}:${minutos}:${segundos}`;
}

setInterval(atualizarRelogio, 1000);
atualizarRelogio();

fetch("/scan-rede")
    .then(resposta => resposta.json())
    .then(dados => {
        const lista = document.getElementById("lista-dispositivos");
        lista.innerHTML = "";

        dados.forEach(ip => {
            const item = document.createElement("li");
            item.textContent = ip;
            lista.appendChild(item);
        });
    });


function montarCalendario() {
    const hoje = new Date();
    const ano = hoje.getFullYear();
    const mes = hoje.getMonth();

    const nomesMeses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];

    document.getElementById("calendar-month-year").textContent = `${nomesMeses[mes]} ${ano}`;

    const primeiroDiaSemana = new Date(ano, mes, 1).getDay();
    const totalDiasNoMes = new Date(ano, mes + 1, 0).getDate();

    const container = document.getElementById("calendar-days");
    container.innerHTML = "";

    for (let i = 0; i < primeiroDiaSemana; i++) {
        const vazio = document.createElement("span");
        container.appendChild(vazio);
    }

    for (let dia = 1; dia <= totalDiasNoMes; dia++) {
        const celula = document.createElement("span");
        celula.textContent = dia;

        if (dia === hoje.getDate()) {
            celula.classList.add("calendar-today");
        }

        container.appendChild(celula);
    }
}

montarCalendario();


function filtraTarefas(status) {
    document.querySelectorAll('#tarefas li').forEach(tarefa => {
        if (status === 'todas') {
            tarefa.style.display = 'list-item';
        } else if (status === 'pendentes' && (tarefa.classList.contains('tarefa-pendente') || tarefa.classList.contains('tarefa-andamento'))) {
    tarefa.style.display = 'list-item';
        } else if (status === 'concluidas' && tarefa.classList.contains('tarefa-concluida')) {
        tarefa.style.display = 'list-item';
        } else {
            tarefa.style.display = 'none';
        }
    });
}