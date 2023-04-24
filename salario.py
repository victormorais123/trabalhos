name = str(input("Insira o nome do vendedor "))
salarioFixo = float(input("Insira seu salário fixo "))
vendasMES = float(input("Insira a quantidade de vendas, em reais "))
resultadoMES = salarioFixo + vendasMES * 0.15
print("Parabéns", name, "suas vendas no mês totalizaram  %0.2f ",vendasMES)


