import random
import time


def criar_tabuleiro(linhas, colunas):
    return [["~" for _ in range(colunas)] for _ in range(linhas)]

def imprimir_tabuleiro(tabuleiro):
    print("  ", " ".join(str(i) for i in range(1, len(tabuleiro[0]) + 1)))

    for idx, linha in enumerate(tabuleiro, start=1):
        print(f"{idx} " + " ".join(linha))

def salvar_ranking(nome, tentativas, tempo, pontuacao):
    with open("ranking.txt", "a") as arquivo:
        arquivo.write(f"{nome};{tentativas};{tempo:.3f};{pontuacao}\n")

def exibir_ranking():
    ranking = []
    try:
        with open("ranking.txt", "r") as arquivo:
            for linha in arquivo:
                nome, tentativas, tempo, pontuacao = linha.strip().split(";")
                ranking.append((nome, int(tentativas), float(tempo), int(pontuacao)))
    except FileNotFoundError:
        print("Nenhum ranking encontrado. Jogue para criar o ranking!")

    ranking.sort(key=lambda x: x[3], reverse=True)
    print("\nRanking dos Jogadores:")
    for i, (nome, tentativas, tempo, pontuacao) in enumerate(ranking, 1):
        print(f"{i}. {nome} - Pontuação: {pontuacao}, Tentativas: {tentativas}, Tempo: {tempo:.3f} segundos")

def jogo_batalha_naval():
    linhas, colunas = 10, 10
    tabuleiro = criar_tabuleiro(linhas, colunas)
    max_navios = 5
    max_tentativas = 10
    tentativas = 0
    navios_encontrados = 0
    pontuacao = 0

    nome = input("Digite seu nome para o ranking: ")

    print("Bem-vindo ao Jogo de Batalha Naval!")
    print(f"Você tem {max_tentativas} tentativas para encontrar {max_navios} navios.")
    print("Escolha uma linha e uma coluna entre 1 e 10.")

    posicoes_navios = set()
    while len(posicoes_navios) < max_navios:
        linha_navio = random.randint(0, linhas - 1)
        coluna_navio = random.randint(0, colunas - 1)
        posicoes_navios.add((linha_navio, coluna_navio))

    inicio = time.time()


    while tentativas < max_tentativas and navios_encontrados < max_navios:
        imprimir_tabuleiro(tabuleiro)
        
        try:
            linha_tentativa = int(input("Escolha uma linha (1 a 10): ")) - 1
            coluna_tentativa = int(input("Escolha uma coluna (1 a 10): ")) - 1
        except ValueError:
            print("Por favor, insira números válidos.")
            continue
        
        if linha_tentativa < 0 or linha_tentativa >= linhas or coluna_tentativa < 0 or coluna_tentativa >= colunas:
            print("Coordenada fora do tabuleiro! Tente novamente.")
            continue

        tentativas += 1

        if (linha_tentativa, coluna_tentativa) in posicoes_navios:
            print("Parabéns! Você acertou um navio! 💣")
            tabuleiro[linha_tentativa][coluna_tentativa] = "💣"  
            navios_encontrados += 1
            pontuacao += 20  
            posicoes_navios.remove((linha_tentativa, coluna_tentativa))
        else:
            print("Você errou! ❌")
            tabuleiro[linha_tentativa][coluna_tentativa] = "❌"  
            print(f"Restam {max_tentativas - tentativas} tentativas.")

        if navios_encontrados == max_navios:
            print("Parabéns! Você encontrou todos os navios!")
            break
        
        if tentativas == max_tentativas:
            print("Fim do jogo! Suas tentativas acabaram.")
            print("Os navios estavam nas seguintes posições:")
            for linha, coluna in posicoes_navios:
                tabuleiro[linha][coluna] = "🚢"  
            imprimir_tabuleiro(tabuleiro)

    
    fim = time.time()
    tempo_total = fim - inicio

    salvar_ranking(nome, tentativas, tempo_total, pontuacao)
    print(f"Seu resultado foi salvo! Você fez {tentativas} tentativas em {tempo_total:.3f} segundos e sua pontuação foi {pontuacao} pontos.")


    exibir_ranking()

jogo_batalha_naval()
