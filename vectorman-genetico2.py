"""
-- ===========================
--        Sonic_genetico
-- ===========================
--
--            **** Universidad de Panama ****
-- ** Faculta de Informatica, Electronica y Comunicacion **
--           **** Inteligencia Artificial ****
--    Participantes del Examen:          
--              
--    Andres Morales          
--    Ricardo Vargas           
--    Victor Alfonso
--    Leonardo Ortega               
--    Felipe de Leon
--
-- 
-- ===========================
--         Copyright
-- ===========================
-- Todos lo derechos reservados
-- 
"""
import retro
import pygame
import json
import os.path as path 
import random
from pygame.locals import *

largo = 5000 #La longitud del material genetico de cada individuo
num = 50 #La cantidad de individuos que habra en la poblacion
pressure = 25 #Cuantos individuos se seleccionan para reproduccion. 
mutation_chance = 0.3 #La probabilidad de que un individuo mute
valor_estatico = 0

def crea_genes():#["B",                "A",          "MODE",        "START",         "UP",            "DOWN",           "LEFT",             "RIGHT",             "C",           "Y",             "X",            "Z"]
    return (random.randint(0,1), valor_estatico, valor_estatico, valor_estatico, valor_estatico, random.randint(0,1), valor_estatico, random.randint(0,1), valor_estatico, valor_estatico, valor_estatico, valor_estatico)

def crearPoblacion():#se verifica si existe el archivo de una poblacion existente y la carga, sino, crea una pobalcion de individuos
    
    if path.exists('population.txt'):
       poblacion = []
       archivo = open("population.txt", "r")
       datos = archivo.read()
       archivo.close()
       poblacion = json.loads(datos)
       return poblacion
    
    else:
        poblacion = []
        for i in range(num):
            individuo = []
            for j in range(largo):
                individuo.append(crea_genes())
            poblacion.append(individuo)
        return poblacion
                
def evaluar_poblacion(env, poblacion):
    #se recorre el array de la poblacion para renderizar cada uno de los movimientos en pantalla
    puntuados = []
    vidas = 3
    for individuo in poblacion:
        _obs = env.reset() 
        for action in individuo:
            env.render()
            video_size = env.observation_space.shape[1], env.observation_space.shape[0]
            screen = pygame.display.set_mode(video_size)
            _obs, _rew, done, _info = env.step(action)
            vida = _info['lives']
            if vida < vidas:
                break
            if done:
                break
        a = _info['x']
        puntuados.append([a, individuo]) #Calcula el fitness de un individuo concreto y luego se carga junto al individuo en un arreglo
               
        print (_info['x'])    
    
    """
        Se puntua todos los elementos de la poblacion y se queda con los mejores
        guardandolos dentro de 'selected'.
        Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
        llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
        modificar).
  
        Por ultimo muta a los individuos y se carga la nueva poblacion en el archivo population.txt
  
    """
    puntuados = [i[1] for i in sorted(puntuados)]       
    poblacion = puntuados   
    
    selected =  puntuados[(len(puntuados)-pressure):] 
    
    for i in range(len(poblacion)-pressure):
        punto = random.randint(1,largo-1) 
        padre = random.sample(selected, 2) 
        poblacion[i][:punto] = padre[0][:punto] 
        poblacion[i][punto:] = padre[1][punto:]
        
  
    for i in range(len(poblacion)-pressure):
        if random.random() <= mutation_chance:#Cada individuo de la poblacion (menos los padres) tienen una probabilidad de mutar 
            punto = random.randint(1,largo-1) #Se elige un punto al azar   
            poblacion[i][punto] = crea_genes()#y un nuevo valor para este punto
            
    print ("nueva poblacion")
    datos = json.dumps(poblacion)
    f = open('population.txt', 'w')
    f.write(datos)
    f.close()
    print (len(poblacion))
            
    return poblacion
               
env = retro.make(game='vectorman2-Genesis', state='Level2') 
poblacion = crearPoblacion()#Inicializar una poblacion

# Se evolucion la poblacion mil veces    
for i in range (1000):
    poblacion = evaluar_poblacion(env, poblacion)
    
    
      


