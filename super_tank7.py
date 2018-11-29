# Super Tank - utilizando as imagens de resolução baixa (e arrumando o CROP já que a resolução é outra)

from mame_lib import *
import time
import keyboard
import random
import cv2
import numpy as np

# retorna False caso não ache o "meu tanque"
def localizaMeuTanque():
    # mandar uma imagem por vez como parametro, quando encontrar retorna
    pt = localizaTanqueAmarelo(img_amarelo_up)

    if(pt == False):
        pt = localizaTanqueAmarelo(img_amarelo_left)

    if (pt == False):
        pt = localizaTanqueAmarelo(img_amarelo_down)

    if (pt == False):
        pt = localizaTanqueAmarelo(img_amarelo_right)

    return pt

def localizaTanqueAmarelo(imagem):
    coordenadas = imgMatchComCor(img_tela, imagem)
    for pt in coordenadas:
        return pt

    return False

def objetivoMaisProximo(coordenadaMeuTanque, coordenadaObjetivos):
    return nearestPoint(coordenadaMeuTanque, coordenadaObjetivos)

def objetivoMaisDistante(coordenadaMeuTanque, coordenadaObjetivos):
    return farthestPoint(coordenadaMeuTanque, coordenadaObjetivos)

def direcaoObjetivo(coordenadaMeuTanque, coordenadaObjetivo):
    if(coordenadaMeuTanque == False or coordenadaObjetivo == False):
        return False

    x1, y1 = coordenadaMeuTanque
    x2, y2 = coordenadaObjetivo

    # escolhe se vai mover na horizontal ou na vertical, indo para a direção que está mais longe
    distX = abs(x1-x2)
    distY = abs(y1-y2)

    if(distX > distY):
        #move na horizontal
        if(x1 > x2):
            #print('objetivo na esquerda')
            return left
        else:
            #print('objetivo na direita')
            return right
    else:
        #move na vertical
        if(y1 > y2):
            #print('objetivo acima')
            return up
        else:
            #print('objetivo embaixo')
            return down

    return False

#comandos
up    = MAME_UP
right = MAME_RIGHT
down  = MAME_DOWN
left  = MAME_LEFT
shoot = MAME_LCONTROL

start = MAME_1
coin  = MAME_5

#testa se a direcao atual é exatamente o inverso da direcao anterior
def dilema(direcao, direcaoAnterior):
    if ((direcao == up and direcaoAnterior == down) or
        (direcao == down and direcaoAnterior == up) or
        (direcao == left and direcaoAnterior == right) or
        (direcao == right and direcaoAnterior == left)):
        return True
    else:
        return False

print ("PRESSIONE 'i' PARA INICIAR O ALGORITMO!")
keyboard.wait('i')

# imagens
img_verde = cv2.imread('imgs2/stank_verde.jpg', 0)
img_vermelho = cv2.imread('imgs2/stank_vermelho.jpg', 0)

#imagens dependentes de cor
img_amarelo_up = cv2.imread('imgs2/stank_amarelo_up.jpg', 1)
img_amarelo_left = cv2.imread('imgs2/stank_amarelo_left.jpg', 1)
img_amarelo_down = cv2.imread('imgs2/stank_amarelo_down.jpg', 1)
img_amarelo_right = cv2.imread('imgs2/stank_amarelo_right.jpg', 1)

cont = 0
direcaoAnterior = 0
posicaoAnteriorTanque = 0
alvoAtual = 0
while(True):
    # imagem da tela
    img_tela = getImg()
    #img_tela = img_tela[148:908, 30:730]    #crop apenas na parte que interessa
    img_gray = cv2.cvtColor(img_tela, cv2.COLOR_BGR2GRAY)

    # localiza todos pontos vermelhos
    coordenadasVermelhas = imgMatch(img_gray, img_vermelho)

    # só procura os verdes se não tiver nenhum vermelho (estrategia e economia de recursos)
    coordenadasVerdes = []
    if(coordenadasVermelhas == []):
        # localiza todos pontos verdes
        coordenadasVerdes = imgMatch(img_gray, img_verde)

    # localiza o tanque amarelo
    coordenadaMeuTanque = localizaMeuTanque()

    # se nao encontrou o meu tanque, usa a coordenada anterior
    if(coordenadaMeuTanque == False):
        coordenadaMeuTanque = posicaoAnteriorTanque
    else:
        posicaoAnteriorTanque = coordenadaMeuTanque

    # se o alvo atual ainda está na imagem, considerar ele o objetivo mais próximo.
	# apenas se não houver nenhum objetivo vermelho**
    alvoAtualInalterado = False
    coordenadaObjetivos = coordenadasVerdes + coordenadasVermelhas
    if(coordenadasVermelhas == []):
        for pt in coordenadaObjetivos:
            if(pt == alvoAtual):
                alvoAtualInalterado = True
                break;
    if(alvoAtualInalterado):
        # alvo atual ainda está na imagem, então ele segue sendo o objetivo
        coordenadaObjetivo = alvoAtual
    else:
        # caso contrário localiza o objetivo mais proximo
        coordenadaObjetivo  = objetivoMaisProximo(coordenadaMeuTanque, coordenadaObjetivos)
        alvoAtual           = coordenadaObjetivo

    direcao = direcaoObjetivo(coordenadaMeuTanque, coordenadaObjetivo)
    if(direcao != False):
        if(direcao != direcaoAnterior):
            #se a direcao for oposta da direcao anterior ele ignora, pois está em um "dilema"
            if(not dilema(direcao, direcaoAnterior) or direcaoAnterior == 0):
                SendInput(Keyboard(direcaoAnterior, KEYEVENTF_KEYUP))
                direcaoAnterior = direcao
                SendInput(Keyboard(direcao))
            else:
                SendInput(Keyboard(direcaoAnterior, KEYEVENTF_KEYUP))
                direcaoAnterior = 0
                print("dilema")

    #indepenente da imagem, aperta o botão de tiro em frames pares e keyup em frames ímpares
    #start e coin também
    if(cont%2 == 0):
        SendInput(Keyboard(shoot))
        SendInput(Keyboard(start))
        SendInput(Keyboard(coin))
    else:
        SendInput(Keyboard(shoot, KEYEVENTF_KEYUP))
        SendInput(Keyboard(start, KEYEVENTF_KEYUP))
        SendInput(Keyboard(coin, KEYEVENTF_KEYUP))

    cont += 1
    print(cont)

    #if(cont >= 60):
    if(cont>=60000):
        break

    if keyboard.is_pressed('q'):
        print("Apertou Q para sair do programa")
        break
