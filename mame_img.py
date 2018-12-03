from PIL import ImageGrab
import win32gui
import time
import win32gui, win32com.client
import cv2
import numpy as np
#from scipy.spatial import distance as dist

toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

#testa se está aberto o processo do mame
existe = False
for hwnd, title in winlist:
    if 'mame:' in title.lower():
        existe = True
        break
if not existe:
    print("Por favor abra o Mame para continuar.")
    #return False   (quando for uma função na lib)
    exit()

mame = [(hwnd, title) for hwnd, title in winlist if 'mame:' in title.lower()]
# just grab the hwnd for first window matching mame
mame = mame[0]
hwnd = mame[0]
print(mame)
#print(hwnd)
#win32gui.SetForegroundWindow(hwnd)
#time.sleep(0.015)

#win32gui.ShowWindow(hwnd, 8)     #MAIS RÁPIDO
#win32gui.SetForegroundWindow(hwnd)
#time.sleep(0.0001)

def getImg():
    #grande gambiarra  (que talvez seja muito útil futuramente!)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')

    win32gui.SetForegroundWindow(hwnd)
    atual = win32gui.GetForegroundWindow()

    if(hwnd != atual):
        time.sleep(0.001)
        return getImg()
    else:
        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox)  #formato PIL
        imgcv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)     #formato do opencv
        return imgcv2

# testa se a img_small está contida na img_big, se estiver, retorna todas coordenadas onde isso ocorre
# a img_big DEVE estar convertida pelo comando img_big = cv2.cvtColor(img_tela, cv2.COLOR_BGR2GRAY)
def imgMatch(img_big, img_small):
    retorno = []
    res = cv2.matchTemplate(img_big, img_small, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        retorno.append(pt)
    return retorno

# image match com cor, ambas imagens DEVEM ter os 3 canais de cor (b, g, r)
def imgMatchComCor(img_big, img_small):
    #nao foi necessario dar o split e testar uma por uma, mas caso futuramente seja necessario é só fazer isso
    #img_big_blue, img_big_green, img_big_red = cv2.split(img_big)
    #img_small_small, img_small_green, img_small_red = cv2.split(img_small)

    retorno = []
    res = cv2.matchTemplate(img_big, img_small, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        retorno.append(pt)
    return retorno

# image match com transparencia, ignorando tudo que for da cor XXXXXX (a definir)
def imgMatchComTransparencia(img_big, img_small):
    #cor para ignorar (definir OU pegar o primeiro pixel...?)
    color_to_ignore = (255, 255, 255)
    #máscara normal, 1 channel apenas
    mask = cv2.inRange(img_small, color_to_ignore, color_to_ignore)
    #cv2.imshow("mask", mask)
    #máscara em RGB, para que a função matchTemplate aceite
    mask2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    #cv2.imshow("mask2", mask2)
    #inverte a máscara
    mask3 = cv2.bitwise_not(mask2)
    #cv2.imshow("mask3", mask3)

    retorno = []
    res = cv2.matchTemplate(img_big, img_small, cv2.TM_CCORR_NORMED, None, mask3)
    threshold = 0.93
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        retorno.append(pt)
    return retorno

# retorna o ponto mais proximo do alvo, primeiro parâmetro é o target e o segundo um array com vários pontos
def nearestPoint(target, points):
    nearest = 100000
    pt = False
    for point in points:
        D = distance(target, point)
        if(D < nearest):
            nearest = D
            pt = point
    return pt

# retorna o ponto mais distante do alvo, primeiro parâmetro é o target e o segundo um array com vários pontos
def farthestPoint(target, points):
    farthest = 0
    pt = False
    for point in points:
        D = distance(target, point)
        if(D > farthest):
            farthest = D
            pt = point
    return pt

# calcula a distancia entre 2 pontos, descobrir qual método é mais rapido/eficiente
def distance(target, point):
    #metodo 1
    #D = dist.euclidean(target, point)
    #return D

    #metodo 2
    a = np.array(target)
    b = np.array(point)
    D = np.sqrt(np.sum((a - b) ** 2))

    return D

#imagem = getImg()
#imagem.show()

#FUNCIONA, MAS NAO EM TELA CHEIA

#HWND = Handle to A Window (Windows programming)

#https://stackoverflow.com/questions/3260559/how-to-get-a-window-or-fullscreen-screenshot-in-python-3k-without-pil
