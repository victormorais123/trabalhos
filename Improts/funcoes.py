import os
import time
def limparTela():
    os.system("cls")

def esperarSegundos(segundos):
    time.sleep(segundos)

def celsiusParaFahrenheit(fahrenheit):
    return (fahrenheit * 1.8) + 32

def mudarCor(codeCor):
    os.system("color " +str(codeCor))