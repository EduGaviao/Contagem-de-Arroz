#===============================================================================
# Trabalho 4: Contando arroz
#-------------------------------------------------------------------------------
# Autor: Eduarda Simonis Gavião e Willian Rodrigo Huber
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import statistics
import math
import numpy as np
import cv2


INPUT_IMAGE =  '205.bmp'

#algoritmo para processar as imagens
def process(img):
    copia=img.copy()
    copia = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #coloca imagem em escala de cinza 
    
    kernel = np.ones((3, 3), np.uint8) #define o kernel
    
    thresh = cv2.adaptiveThreshold(copia, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,101, -27) #treshold adaptativo
    
   #faz processo de abertura 
    img_erode = cv2.erode(thresh, kernel, iterations=2) #primeiro erode
    img_dilated = cv2.dilate(img_erode, kernel,iterations=1) #depois Dilata
    
    contagem(img_dilated,img) #chama função para contagem dos arrozes, passa a imagem sem ruídos e a original
    
    
def contagem(opening,img):
    
    arroz,_ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.RETR_EXTERNAL = conta apenas os contornos externos
    
    cv2.drawContours(img, arroz, -1, (255, 0,0), 2)#desenha os contornos na copia da imagem original
    
    area_m=[cv2.contourArea(contador) for contador in arroz]#área dos contornos fechados
    
    mediana=statistics.median(area_m) #mediana das áreas do contorno
    
    count = 0
    for i in range(len(arroz)): #for para os contornos do arroz
        area = cv2.contourArea(arroz[i]) #acha a área de cada contorno
        if area >mediana: #compara com a área mediana, se for maior, que dizer que tem mais de um grão 
            count += round(area/mediana) #faz a divisão da área pela mediana para estimar a quantidade de grãos
        else: #caso contrário
            count += 1 #soma mais um 
            
    
    print ('Arrozes contados:',count) #printa o número de arrozes
    cv2.imshow("Detectados", img)#mostra a imagem com contornos 

    
def main ():

    # Abre a imagem 
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR) 
    
    #prepara caso dê erro ao abrir a imagem
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    processamento=process(img) #chama a função de processamento
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

#===============================================================================
