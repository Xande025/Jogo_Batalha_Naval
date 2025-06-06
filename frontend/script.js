let tabuleiro = [];
let fim = false;
let nomeJogador = '';

function solicitarNomeJogador() {
    nomeJogador = prompt('Digite seu nome para o ranking:');
    if (!nomeJogador || nomeJogador.trim() === '') {
        alert('Nome obrigatório!');
        return solicitarNomeJogador();
    }
}

function desenharTabuleiro() {
    const tab = document.getElementById('tabuleiro');
    tab.innerHTML = '';
    // Adiciona cabeçalho de colunas
    const headerRow = document.createElement('div');
    headerRow.style.display = 'grid';
    headerRow.style.gridTemplateColumns = 'repeat(11, 44px)';
    headerRow.style.marginBottom = '2px';
    // Célula vazia canto superior esquerdo
    const emptyCell = document.createElement('div');
    emptyCell.style.background = 'transparent';
    headerRow.appendChild(emptyCell);
    for (let j = 0; j < 10; j++) {
        const colHeader = document.createElement('div');
        colHeader.textContent = j + 1;
        colHeader.style.textAlign = 'center';
        colHeader.style.fontWeight = 'bold';
        colHeader.style.background = '#1976d2';
        colHeader.style.color = 'white';
        colHeader.style.borderRadius = '6px 6px 0 0';
        colHeader.style.boxShadow = '0 2px 4px #0002';
        headerRow.appendChild(colHeader);
    }
    tab.appendChild(headerRow);
    // Adiciona linhas do tabuleiro
    for (let i = 0; i < 10; i++) {
        const row = document.createElement('div');
        row.style.display = 'grid';
        row.style.gridTemplateColumns = 'repeat(11, 44px)';
        row.style.marginBottom = '2px';
        // Número da linha
        const rowHeader = document.createElement('div');
        rowHeader.textContent = i + 1;
        rowHeader.style.textAlign = 'center';
        rowHeader.style.fontWeight = 'bold';
        rowHeader.style.background = '#1976d2';
        rowHeader.style.color = 'white';
        rowHeader.style.borderRadius = '6px 0 0 6px';
        rowHeader.style.boxShadow = '2px 0 4px #0002';
        row.appendChild(rowHeader);
        for (let j = 0; j < 10; j++) {
            const casa = document.createElement('div');
            casa.className = 'casa';
            casa.textContent = tabuleiro[i][j];
            casa.style.transition = 'background 0.2s, box-shadow 0.2s';
            casa.style.background = '#b3e5fc';
            casa.style.border = '1px solid #90caf9';
            casa.style.borderRadius = '6px';
            casa.style.boxShadow = '0 1px 2px #0001';
            casa.style.display = 'flex';
            casa.style.alignItems = 'center';
            casa.style.justifyContent = 'center';
            casa.style.fontSize = '1.6em';
            casa.style.cursor = fim ? 'not-allowed' : 'pointer';
            casa.onmouseover = () => { if (!fim && casa.textContent === '~') casa.style.background = '#81d4fa'; };
            casa.onmouseout = () => { if (!fim && casa.textContent === '~') casa.style.background = '#b3e5fc'; };
            if (tabuleiro[i][j] === '💣') {
                casa.classList.add('acertou');
                casa.style.background = '#388e3c';
                casa.style.color = 'white';
                casa.style.boxShadow = '0 0 8px #388e3c88';
            }
            if (tabuleiro[i][j] === '❌') {
                casa.classList.add('errou');
                casa.style.background = '#e57373';
                casa.style.color = 'white';
                casa.style.boxShadow = '0 0 8px #e5737388';
            }
            casa.onclick = () => jogar(i, j);
            row.appendChild(casa);
        }
        tab.appendChild(row);
    }
}

function iniciarJogo() {
    solicitarNomeJogador();
    fetch('http://localhost:5000/iniciar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome: nomeJogador })
    })
    .then(res => res.json())
    .then(data => {
        tabuleiro = data.tabuleiro;
        fim = false;
        document.getElementById('info').textContent = `Tentativas: 0 / ${data.max_tentativas}`;
        desenharTabuleiro();
    });
}

function jogar(i, j) {
    if (fim) return;
    fetch('http://localhost:5000/jogar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ linha: i, coluna: j })
    })
    .then(res => res.json())
    .then(data => {
        if (data.erro) {
            alert(data.erro);
            return;
        }
        tabuleiro = data.tabuleiro;
        document.getElementById('info').textContent = `Tentativas: ${data.tentativas} / ${data.total} acertos: ${data.acertos}`;
        desenharTabuleiro();
        if (data.fim) {
            fim = true;
            if (data.acertos === data.total) {
                alert('Parabéns! Você encontrou todos os navios!');
            } else {
                // Mostra as posições dos navios restantes
                if (data.restantes) {
                    for (const [linha, coluna] of data.restantes) {
                        // Mostra navio não encontrado
                        const tabDivs = document.querySelectorAll('#tabuleiro > div');
                        if (tabDivs[linha + 1]) { // +1 por causa do header
                            const casa = tabDivs[linha + 1].children[coluna + 1]; // +1 por causa do header
                            if (casa && casa.textContent === '~') {
                                casa.textContent = '🚢';
                                casa.style.background = '#ffd600';
                                casa.style.color = '#333';
                            }
                        }
                    }
                }
                alert('Fim do jogo! Suas tentativas acabaram. Os navios restantes foram revelados.');
            }
        }
    });
}

function exibirRanking() {
    fetch('http://localhost:5000/pontuacao')
        .then(res => res.json())
        .then(data => {
            const rankingDiv = document.getElementById('ranking');
            if (!data.ranking || data.ranking.length === 0) {
                rankingDiv.innerHTML = '<p style="text-align:center;">Nenhum ranking encontrado.</p>';
                return;
            }
            let html = '<table style="width:100%;border-collapse:collapse;text-align:center;">';
            html += '<tr style="background:#1976d2;color:white;"><th>Posição</th><th>Nome</th><th>Pontuação</th><th>Tentativas</th><th>Tempo (s)</th></tr>';
            data.ranking.forEach((jogador, idx) => {
                html += `<tr style="background:${idx%2?'#e3f2fd':'#bbdefb'};">
                    <td>${idx+1}</td>
                    <td>${jogador.nome}</td>
                    <td>${jogador.pontuacao}</td>
                    <td>${jogador.tentativas}</td>
                    <td>${jogador.tempo.toFixed(2)}</td>
                </tr>`;
            });
            html += '</table>';
            rankingDiv.innerHTML = html;
        })
        .catch(() => {
            document.getElementById('ranking').innerHTML = '<p style="text-align:center;">Nenhum ranking encontrado.</p>';
        });
}

// Inicia automaticamente ao abrir
window.onload = function() {
    iniciarJogo();
    exibirRanking();
};
