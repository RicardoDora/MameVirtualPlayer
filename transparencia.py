# Street Fighter - apenas para testar a transparência na função match template

from gigante import *
from mame_keys import *
from mame_img import *
import time
import keyboard
import random
import cv2
import numpy as np

print ("PRESSIONE 'i' PARA INICIAR O ALGORITMO!")
keyboard.wait('i')

# imagens
img_ryu = cv2.imread('imgs/sf2_ryu_trans.jpg', 1)

#loop por frame? adicionar uma biblioteca que recebe a funcao como parametro?
cont = 0
while(True):
    achou = 0

    # imagem da tela
    img = getImg()
    img_tela = img
    img_gray = cv2.cvtColor(img_tela, cv2.COLOR_BGR2GRAY)

    # mostra imagem original
    #cv2.imshow('original', img_tela)

    # mostra imagem original
    #cv2.imshow('ryu', img_ryu)

    # localiza a imagem do ryu, considerando a "transparência"
    b, g, r = cv2.split(img_ryu)
    w, h = b.shape[::-1]
    coordenadas = imgMatchComTransparencia(img_tela, img_ryu)
    for pt in coordenadas:
        cv2.rectangle(img_tela, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        achou = 1
        #break

    if(achou == 0):
        print("nao achou")
    else:
        print("achou")
        cv2.imshow('resultado', img_tela)
        cv2.waitKey(0)

    # mostra imagem resultante
    #cv2.imshow('resultado', img_tela)

    #cv2.waitKey(0)
    #exit(0)
