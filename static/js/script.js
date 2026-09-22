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