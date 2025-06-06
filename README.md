# Batalha Naval

Este é um projeto de jogo Batalha Naval desenvolvido em Python, com uma interface web moderna utilizando Flask para o backend e HTML/CSS/JavaScript para o frontend.

## Funcionalidades
- Jogo clássico de Batalha Naval com navios de tamanhos variados.
- Tabuleiro visual com emojis para acertos, erros e navios.
- Ranking de jogadores salvo em arquivo (`ranking.txt`), exibido no frontend.
- Solicitação do nome do jogador a cada nova partida.
- Exibição das posições dos navios restantes ao final do jogo.

## Estrutura do Projeto
```
├── app.py                # Backend Flask (API do jogo e ranking)
├── batalha_naval.py      # Versão CLI do jogo em Python
├── ranking.txt           # Ranking dos jogadores
├── frontend/
│   ├── index.html        # Página principal do jogo
│   └── script.js         # Lógica do frontend
└── Testes/               # Scripts de teste
```

## Como rodar o projeto

### 1. Instale as dependências do backend
Abra o terminal na pasta do projeto e execute:
```bash
pip install flask flask-cors
```

### 2. Inicie o backend
```bash
python app.py
```
O backend Flask estará rodando em `http://localhost:5000`.

### 3. Abra o frontend
Abra o arquivo `frontend/index.html` no seu navegador.

- O jogo solicitará seu nome ao iniciar.
- Jogue clicando nas casas do tabuleiro.
- Veja o ranking atualizado ao final de cada partida.

## Observações
- O ranking é salvo no arquivo `ranking.txt`.
- Para limpar o ranking, basta apagar o conteúdo deste arquivo.
- O projeto também possui uma versão jogável no terminal (`batalha_naval.py`).

---
Desenvolvido por [Seu Nome].
