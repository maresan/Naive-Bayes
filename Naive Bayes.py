import csv
from random import *
from math import *

def cargarDatos(archivo):
    entrenamiento = []
    pruebas = []
    with open(archivo, 'rb') as csvfile:
        lineas = csv.reader(csvfile)
        dataset = list(lineas)
        shuffle(dataset)
        for i in range(len(dataset)):
            dataset[i] = [float(x) for x in dataset[i]]
            for j in range(len(dataset[0])-1):
                dataset[i][j] = float(dataset[i][j])
            if i < len(dataset)*0.9:
                entrenamiento.append(dataset[i])
            else:
                pruebas.append(dataset[i])
    return entrenamiento, pruebas

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------Funciones para crear el modelo--------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
def separarTipos(dataset):
    separado = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if (vector[-1] not in separado):
            separado[vector[-1]] = []
        separado[vector[-1]].append(vector)
    return separado

def calcularPromedio(numeros):
    suma = 0
    for i in range (len(numeros)):
        suma = suma + numeros[i]
    return suma/float(len(numeros))

def desviacionEstandar(numeros):
    suma = 0
    promedio = calcularPromedio(numeros)
    for i in numeros:
        suma = suma + (i - promedio)**2
    diferencia = suma/float(len(numeros)-1)
    return sqrt(diferencia)

def resumen(dataset):
    matrizResumenes = []
    for atributo in zip(*dataset):
        listaAux = [calcularPromedio(atributo), desviacionEstandar(atributo)]
        matrizResumenes.append(listaAux)
    del matrizResumenes[-1]
    return matrizResumenes

def resumenPorTipo(dataset):
    separado = separarTipos(dataset)
    resumenes = {}
    for tipoDeValor, instancias in separado.iteritems():
        resumenes[tipoDeValor] = resumen(instancias)
    return resumenes

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------Funciones para probar modelo--------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
def calcularProbabilidades(tuplasResumenes, prueba_i):
    probabilidades = {}
    for tipoDeValor, resumenClass in tuplasResumenes.iteritems():
        probabilidades[tipoDeValor] = 1
        for i in range(len(resumenClass)):
            promedio, desvEstandar = resumenClass[i]
            #----calculo de la probabilidad----
            x = prueba_i[i]
            exponente = exp(-(((x - promedio)**2)/(2*((desvEstandar)**2))))
            probabilidad = (1 / (sqrt(2*pi) * desvEstandar)) * exponente
            probabilidades[tipoDeValor] = probabilidades[tipoDeValor] * probabilidad
    return probabilidades

def predecir(tuplasResumenes, vectorEntrada):
    mejorEtiqueta = None
    mejorProbabilidad = -1
    probabilities = calcularProbabilidades(tuplasResumenes, vectorEntrada)
    for tipoDeValor, probabilidad in probabilities.iteritems():
        if (mejorEtiqueta is None or probabilidad > mejorProbabilidad):
            mejorProbabilidad = probabilidad
            mejorEtiqueta = tipoDeValor
    return mejorEtiqueta

def obtenerPredicciones(tuplasResumenes, pruebas):
    predicciones = []
    for i in range(len(pruebas)):
        prediccion = predecir(tuplasResumenes, pruebas[i])
        predicciones.append(prediccion)
    return predicciones

#-----------------------------------------------------------------------------------------------------------------------
def calcularPorcentaje(pruebas, predicciones):
    correcta = 0
    negativosCiertos = 0
    positivosCiertos = 0
    negativosFalsos = 0
    positivosFalsos = 0
    for i in range(len(pruebas)):
        print "prediccion: ", predicciones[i], "resultado de la prueba: ", pruebas[i][-1],
        if (pruebas[i][-1] == predicciones[i]):
            correcta += 1
            print " Prediccion correcta"
            if(pruebas[i][-1] == 0 ):
                negativosCiertos = negativosCiertos + 1
            else:
                positivosCiertos = positivosCiertos + 1
        else:
            print " Prediccion incorrecta"
            if(pruebas[i][-1] == 0 ):
                negativosFalsos = negativosFalsos + 1
            else:
                positivosFalsos = positivosFalsos + 1
    print "De ", len(predicciones), "predicciones ", correcta, " son correctas"
    print
    print "matriz de confusion"
    print "positivos ciertos:", positivosCiertos
    print "negativos falsos:", negativosFalsos
    print "positivos falsos:", positivosFalsos
    print "negativos ciertos:", negativosCiertos

    aux = float(len(pruebas))
    return (correcta/aux) * 100.0

#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------- Programa Principal -----------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
entrenamiento, pruebas  = cargarDatos("dataset.csv")
print"Cantidad entrenadas: {0}, Cantidad de prueba: {1}".format(len(entrenamiento), len(pruebas))
tuplasResumenes = resumenPorTipo(entrenamiento) #preparo el modelo
predicciones = obtenerPredicciones(tuplasResumenes, pruebas) #pruebo el modelo
print('Porcentaje de exactitud: {0}%').format(calcularPorcentaje(pruebas, predicciones))
