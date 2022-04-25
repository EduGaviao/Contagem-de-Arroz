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


INPUT_IMAGE =  '150.bmp'

#algoritmo para processar as imagens
def process(img):
    copia=img.copy()
    copia = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #coloca imagem em escala de cinza 
    
    kernel = np.ones((2, 2), np.uint8) #define o kernel
    
    thresh = cv2.adaptiveThreshold(copia, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,101, -27) #treshold adaptativo
    
   #faz processo de abertura 
    img_erode = cv2.erode(thresh, kernel, iterations=3) #primeiro erode
    img_dilated = cv2.dilate(img_erode, kernel,iterations=2) #primeiro Dilata
    
    
    
    borda=cv2.Canny(img_dilated,100,200)
    contagem(borda,img) #chama função para contagem dos arrozes, passa a imagem sem ruídos e a original
    
    
def contagem(opening,img):
    
    arroz,_ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.RETR_EXTERNAL = conta apenas os contornos externos
    
    cv2.drawContours(img, arroz, -1, (255, 0,0), 2)#desenha os contornos na copia da imagem original
    
    area_m=[cv2.contourArea(contador) for contador in arroz]#área dos contornos fechados
    
    mediana=statistics.median_high(area_m)
    minimo=np.min(area_m)
    dp=statistics.stdev(area_m)
    
    count = 0
    for i in range(len(arroz)):
        area = cv2.contourArea(arroz[i])
        if area >=minimo:
            count += 1
            rect = cv2.boundingRect (arroz[i]) # Extrai coordenadas de retangulo
            
            cv2.rectangle (img, rect, (0,255,0), 1) 
            if area >= (minimo+mediana): #mais de um grão de arroz 
                count += 1
                cv2.putText (img, str ({count, count-1}), (rect [0], rect [1]), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1) #escreve a coordenada
            else:
                cv2.putText (img, str (count), (rect [0], rect [1]), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1) #escreve a coordenada
        
    
    print ('Arrozes contados:',count)
    cv2.imshow("Detectados", img)

    
def main ():

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    processamento=process(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

#===============================================================================