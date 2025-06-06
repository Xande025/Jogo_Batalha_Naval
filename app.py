from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

# Funções do jogo (adaptadas do seu código)
def criar_tabuleiro(linhas, colunas):
    return [["~" for _ in range(colunas)] for _ in range(linhas)]

def posicionar_navios(tabuleiro, navios):
    linhas, colunas = len(tabuleiro), len(tabuleiro[0])
    posicoes_navios = set()
    for tamanho in navios:
        colocado = False
        while not colocado:
            orientacao = random.choice(["H", "V"])
            if orientacao == "H":
                linha = random.randint(0, linhas - 1)
                coluna = random.randint(0, colunas - tamanho)
                pos = [(linha, coluna + i) for i in range(tamanho)]
            else:
                linha = random.randint(0, linhas - tamanho)
                coluna = random.randint(0, colunas - 1)
                pos = [(linha + i, coluna) for i in range(tamanho)]
            if all(p not in posicoes_navios for p in pos):
                posicoes_navios.update(pos)
                colocado = True
    return posicoes_navios

# Estado do jogo (simples, para 1 jogador por vez)
jogo = {
    'tabuleiro': [],
    'navios': [5, 4, 3, 3, 2, 1, 1],
    'posicoes_navios': set(),
    'tentativas': 0,
    'max_tentativas': 20,
    'acertos': 0,
    'total_partes_navios': 0,
    'inicio': 0
}

@app.route('/iniciar', methods=['POST'])
def iniciar():
    data = request.get_json()
    nome = data.get('nome', '').strip() if data else ''
    if not nome:
        return jsonify({'erro': 'Nome do jogador é obrigatório!'}), 400
    linhas, colunas = 10, 10
    jogo['tabuleiro'] = criar_tabuleiro(linhas, colunas)
    jogo['posicoes_navios'] = posicionar_navios(jogo['tabuleiro'], jogo['navios'])
    jogo['tentativas'] = 0
    jogo['acertos'] = 0
    jogo['total_partes_navios'] = len(jogo['posicoes_navios'])
    jogo['inicio'] = time.time()
    jogo['nome'] = nome
    return jsonify({'tabuleiro': jogo['tabuleiro'], 'tentativas': jogo['tentativas'], 'max_tentativas': jogo['max_tentativas']})

@app.route('/jogar', methods=['POST'])
def jogar():
    data = request.json
    linha = data.get('linha')
    coluna = data.get('coluna')
    if not (0 <= linha < 10 and 0 <= coluna < 10):
        return jsonify({'erro': 'Coordenada inválida!'}), 400
    if jogo['tabuleiro'][linha][coluna] != "~":
        return jsonify({'erro': 'Posição já tentada!'}), 400
    jogo['tentativas'] += 1
    if (linha, coluna) in jogo['posicoes_navios']:
        jogo['tabuleiro'][linha][coluna] = "💣"
        jogo['acertos'] += 1
        jogo['posicoes_navios'].remove((linha, coluna))
        acertou = True
    else:
        jogo['tabuleiro'][linha][coluna] = "❌"
        acertou = False
    fim = False
    restantes = []
    if jogo['acertos'] == jogo['total_partes_navios'] or jogo['tentativas'] == jogo['max_tentativas']:
        fim = True
        restantes = list(jogo['posicoes_navios'])
        # Salva no ranking
        tempo_total = time.time() - jogo['inicio']
        pontuacao = jogo['acertos'] * 20
        with open('ranking.txt', 'a') as arquivo:
            arquivo.write(f"{jogo.get('nome','')};{jogo['tentativas']};{tempo_total:.3f};{pontuacao}\n")
    return jsonify({'tabuleiro': jogo['tabuleiro'], 'acertou': acertou, 'tentativas': jogo['tentativas'], 'fim': fim, 'acertos': jogo['acertos'], 'total': jogo['total_partes_navios'], 'restantes': restantes})

@app.route('/pontuacao', methods=['GET'])
def pontuacao():
    ranking = []
    try:
        with open('ranking.txt', 'r') as arquivo:
            for linha in arquivo:
                nome, tentativas, tempo, pontuacao = linha.strip().split(';')
                ranking.append({
                    'nome': nome,
                    'tentativas': int(tentativas),
                    'tempo': float(tempo),
                    'pontuacao': int(pontuacao)
                })
    except FileNotFoundError:
        return {'ranking': []}
    ranking.sort(key=lambda x: x['pontuacao'], reverse=True)
    return {'ranking': ranking}

if __name__ == '__main__':
    app.run(debug=True)
