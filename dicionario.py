contatos = {
    'marcos' : '+55544',
    'maria' : '+555555555',
}

#adicionar elementos
contatos['joao'] = '+5555555555'
#alterar
contatos['maria'] = '+999999999'

#delete elementos com try except
try:
    del contatos['maria']
except KeyError:
    print('Chave não encontrada')


#func pop remove e exibe um erro se não for encontrado
contatos.pop('marias', 'Chave não encontrada')


for key, value in contatos.items():
    print(key, value)