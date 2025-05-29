import pygame
import threading
import time
import requests

# Dimensões
LARGURA_CELULA = 40
ALTURA_CELULA = 40
COLUNAS = 16
LINHAS = 12

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (150, 150, 150)
VERDE = (0, 255, 0)

# Inicialização
pygame.init()
tela = pygame.display.set_mode((COLUNAS * LARGURA_CELULA, LINHAS * ALTURA_CELULA))
pygame.display.set_caption("Robô Controlado pelo Node-RED")

# Labirinto 0=caminho, 1=parede
labirinto = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1],
    [1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1],
    [1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1],
]

# Posição do robô
pos_x, pos_y = 1, 1
comando_atual = ""

# Função de movimento
def mover_para(x, y):
    global pos_x, pos_y
    if 0 <= x < COLUNAS and 0 <= y < LINHAS:
        if labirinto[y][x] == 0:
            pos_x, pos_y = x, y
            return "aceito"
    return "rejeitado"

# Thread: escuta comandos do Node-RED
def escutar_comandos():
    global comando_atual
    while True:
        try:
            r = requests.get("http://localhost:1880/controle_robo", timeout=1)
            comando = r.text.strip()
            if comando in ["cima", "baixo", "esquerda", "direita"]:
                comando_atual = comando
        except:
            pass
        time.sleep(0.1)

# Inicia a thread
thread = threading.Thread(target=escutar_comandos, daemon=True)
thread.start()

# Loop principal
relogio = pygame.time.Clock()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    novo_x, novo_y = pos_x, pos_y

    if comando_atual == "cima":
        novo_y -= 1
    elif comando_atual == "baixo":
        novo_y += 1
    elif comando_atual == "esquerda":
        novo_x -= 1
    elif comando_atual == "direita":
        novo_x += 1

    if comando_atual:
        status = mover_para(novo_x, novo_y)
        try:
            requests.post("http://localhost:1880/retorno_robo", json={
                "x": pos_x,
                "y": pos_y,
                "status": status
            }, timeout=1)
        except:
            pass
        comando_atual = ""  # limpa comando após usar

    # Desenha o mapa
    tela.fill(BRANCO)
    for y in range(LINHAS):
        for x in range(COLUNAS):
            cor = CINZA if labirinto[y][x] == 1 else BRANCO
            pygame.draw.rect(tela, cor, (x * LARGURA_CELULA, y * ALTURA_CELULA, LARGURA_CELULA, ALTURA_CELULA))
            pygame.draw.rect(tela, PRETO, (x * LARGURA_CELULA, y * ALTURA_CELULA, LARGURA_CELULA, ALTURA_CELULA), 1)

    centro_x = pos_x * LARGURA_CELULA + LARGURA_CELULA // 2
    centro_y = pos_y * ALTURA_CELULA + ALTURA_CELULA // 2
    pygame.draw.circle(tela, VERDE, (centro_x, centro_y), 15)

    pygame.display.flip()
    relogio.tick(30)

pygame.quit()
