import time
import os

def limparTela():
    os.system("cls")

def esperarSegundos(segundos):
    time.sleep(segundos)

def mostrarMenu():
    print("########JOGO DA FORCA########")
    print("1 - Jogar")
    print("2 - Sair")
    print("3 - Histórico de partidas")

def pedirPalavra():
    print("Digite a palavra secreta:")
    palavra = input(">>> ").upper()
    if palavra.isalpha():
        return palavra
    else:
        print("A palavra deve conter apenas letras!")
        esperarSegundos(1)
        limparTela()
        return pedirPalavra()  

def pedirDicas():
    print("Deseja receber dicas? (S/N)")
    dicas = input(">>> ").upper()
    if dicas == "S":
        return True
    elif dicas == "N":
        return False
    else:
        print("Opção inválida!")
        esperarSegundos(1)
        limparTela()
        return pedirDicas()
    
def mostrarDicas(dicas):
    print("Dicas:")
    for dica in dicas:
        print(dica)
    print()
    
def pedirLetra():
    print("Digite uma letra:")
    letra = input(">>> ").upper()
    if letra.isalpha() and len(letra) == 1:
        return letra
    else:
        print("Digite apenas uma letra!")
        esperarSegundos(1)
        limparTela()
        return pedirLetra()

def mostrarPalavra(palavra, letras):
    for letra in palavra:
        if letra in letras:
            print(letra, end=" ")
        else:
            print("_", end=" ")
    print()

def mostrarLetras(letras):
    print("Letras já usadas:")
    for letra in letras:
        print(letra, end=" ")
    print()

