# MameVirtualPlayer
Biblioteca em Python para criar jogadores virtuais para o emulador MAME

Para instalar a biblioteca é necessário realizar os seguintes passos:

1 - Baixar e instalar o Python 3.7.0

https://www.python.org/downloads/release/python-370/


2 - Atualizar o pip

python -m pip install --upgrade pip


3 - Instalar PIL

pip install Pillow


4 - Instalar win32gui

Vá até a pasta onde estão os arquivos, ou baixe a versão desejada do pypiwin32 no link abaixo:

https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32

E execue o comando

pip install pywin32-224-cp37-cp37m-win32.whl


5 - Instalar o OpenCV

pip install opencv-python

OU

https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv

pip install opencv_python-3.4.3-cp37-cp37m-win32.whl

OU

https://pypi.org/project/opencv-python/#files

pip install opencv_python-3.4.3.18-cp37-cp37m-win32.whl


6 - Instalar a biblioteca Keyboard

pip install keyboard


7 - Editar o arquivo mame.ini

Alterar o valor da propriedade keyboardprovider para dinput
keyboardprovider          dinput
