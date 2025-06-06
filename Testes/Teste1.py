import random
import time

# Função para criar o tabuleiro como uma matriz
def criar_tabuleiro(tamanho):
    return [["~" for _ in range(tamanho)] for _ in range(tamanho)]

# Função para exibir o tabuleiro
def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" ".join(linha))

# Função para salvar o desempenho no arquivo de ranking
def salvar_ranking(nome, tentativas, tempo):
    with open("ranking.txt", "a") as arquivo:
        arquivo.write(f"{nome};{tentativas};{tempo:.3f}\n")

# Função para ler e exibir o ranking dos jogadores
def exibir_ranking():
    ranking = []
    try:
        with open("ranking.txt", "r") as arquivo:
            for linha in arquivo:
                nome, tentativas, tempo = linha.strip().split(";")
                ranking.append((nome, int(tentativas), float(tempo)))
    except FileNotFoundError:
        print("Nenhum ranking encontrado. Jogue para criar o ranking!")

    # Ordenar o ranking pelo número de tentativas e exibir
    ranking.sort(key=lambda x: x[1])
    print("\nRanking dos Jogadores:")
    for i, (nome, tentativas, tempo) in enumerate(ranking, 1):
        print(f"{i}. {nome} - Tentativas: {tentativas}, Tempo: {tempo:.3f} segundos")

# Função principal do jogo de Batalha Naval
def jogo_batalha_naval():
    tamanho = 5
    tabuleiro = criar_tabuleiro(tamanho)
    linha_navio = random.randint(0, tamanho - 1)
    coluna_navio = random.randint(0, tamanho - 1)
    tentativas = 0
    max_tentativas = 5

    # Solicita o nome do jogador
    nome = input("Digite seu nome para o ranking: ")

    print("Bem-vindo ao Jogo de Batalha Naval!")
    print(f"Você tem {max_tentativas} tentativas para encontrar o navio.")
    print("Escolha uma linha e uma coluna entre 1 e 5.")

    # Início do temporizador
    inicio = time.time()

    # Loop do jogo
    while tentativas < max_tentativas:
        imprimir_tabuleiro(tabuleiro)
        
        try:
            linha_tentativa = int(input("Escolha uma linha (1 a 5): ")) - 1
            coluna_tentativa = int(input("Escolha uma coluna (1 a 5): ")) - 1
        except ValueError:
            print("Por favor, insira números válidos.")
            continue
        
        if linha_tentativa < 0 or linha_tentativa >= tamanho or coluna_tentativa < 0 or coluna_tentativa >= tamanho:
            print("Coordenada fora do tabuleiro! Tente novamente.")
            continue

        tentativas += 1

        if linha_tentativa == linha_navio and coluna_tentativa == coluna_navio:
            print("Parabéns! Você acertou o navio! 💣")
            tabuleiro[linha_tentativa][coluna_tentativa] = "💣"  # Navio acertado com uma bomba
            imprimir_tabuleiro(tabuleiro)
            break
        else:
            print("Você errou! ❌")
            tabuleiro[linha_tentativa][coluna_tentativa] = "❌"  # Tentativa errada
            print(f"Restam {max_tentativas - tentativas} tentativas.")
        
        if tentativas == max_tentativas:
            print("Fim do jogo! Suas tentativas acabaram.")
            print(f"O navio estava na posição ({linha_navio + 1}, {coluna_navio + 1}) 🚢.")
            tabuleiro[linha_navio][coluna_navio] = "🚢"  # Onde o navio estava
            imprimir_tabuleiro(tabuleiro)

    # Fim do temporizador e cálculo do tempo total
    fim = time.time()
    tempo_total = fim - inicio

    # Salva o desempenho do jogador no ranking
    salvar_ranking(nome, tentativas, tempo_total)
    print(f"Seu resultado foi salvo! Você fez {tentativas} tentativas em {tempo_total:.3f} segundos.")

    # Exibe o ranking atualizado
    exibir_ranking()

# Inicia o jogo e exibe o ranking ao final
jogo_batalha_naval()
