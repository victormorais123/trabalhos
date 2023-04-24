print("************ BEM VINDO AO DETETIVE VITINHO ************")

perguntas = ["Você telefonou para a vitima?", 'Você esteve no local do crime?', 'Você mora perto da vitima?', 'Você já trabalhou com a vitima?']
respostas = []
print("Responda as", len(perguntas), "perguntas abaixo:")
for pergunta in perguntas:
    int(input(pergunta+ "(1) Sim (0)Não :"))
    respostas.append(respostas)
soma = 0
for resposta in respostas: 
    soma = soma + resposta
if soma < 2:
    print("Inocente")
elif soma == 2:
    print("Suspeito")
elif soma <= 4:
    print("Cumplice")
else:
    print("Assaltante")