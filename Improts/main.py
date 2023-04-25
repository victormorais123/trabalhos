import os
import time
from funcoes import limparTela, esperarSegundos, celsiusParaFahrenheit, mudarCor


limparTela()
print("seja bem vindo")
esperarSegundos(segundos=2)
while True:
    print("(0) Sair")
    print("(1) celsius")
    print("(2) fahrenheit")
    opcao = input()
    if opcao == "0":
        break
    elif opcao == "1":
        print("converetendo C")
        fahrenheit = float(input("Digite a temperatura em Fahrenheit: "))
        print(f"{fahrenheit}°F = {celsiusParaFahrenheit(fahrenheit)}°C")
    elif opcao == "5":
        print("Mudar cor")
        cor = int(input("Informe o codigo da cor: "))
        mudarCor(cor)

    elif opcao == "0":
        print("converetendo f")
    else:
        print("opcao invalida")
print("Volte sempre")

#   