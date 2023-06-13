#1134929 RA
from func import limparTela, mostrarMenu, pedirPalavra, pedirDicas, mostrarDicas, pedirLetra

while True:
    limparTela()
    mostrarMenu()
    opcao = input(">>> ")
    if opcao == "1":
        limparTela()
        palavra = pedirPalavra()
        dicas = []
        if pedirDicas():
            limparTela()
            print("Digite as dicas:")
            while True:
                dica = input(">>> ")
                if dica == "":
                    break
                else:
                    dicas.append(dica)
            limparTela()
            mostrarDicas(dicas)
        else:
            limparTela()
        letrasErradas = []
        letrasCertas = []
        while True:
            mostrarPalavra = ""
            for letra in palavra:
                if letra in letrasCertas:
                    mostrarPalavra += letra
                else:
                    mostrarPalavra += "_"
            print(mostrarPalavra)
            print()
            print("Letras erradas:")
            for letra in letrasErradas:
                print(letra, end=" ")
            print()
            print()
            if "_" not in mostrarPalavra:
                print("Você venceu!")
                break
            elif len(letrasErradas) == 6:
                print("Você perdeu!")
                print("A palavra era:", palavra)
                break
            else:
                letra = pedirLetra()
                if letra in palavra:
                    letrasCertas.append(letra)
                else:
                    letrasErradas.append(letra)
        arquivo = open("dados.bd", "a")
        arquivo.write(palavra)
        arquivo.close()
    if opcao == "2":
        break
    if opcao == "3":
        try :
            arquivo = open("dados.bd", "r")
            palavras = arquivo.readlines()
            arquivo.close()
            print("Histórico de partidas:")
            for palavra in palavras:
                print(palavra)
            input("Pressione ENTER para voltar ao menu...")
        except FileNotFoundError:
            arquivo = open("dados.bd", "w")
            arquivo.close()
            print("Histórico de partidas:")
            print("Nenhuma partida jogada!")
            input("Pressione ENTER para voltar ao menu...")