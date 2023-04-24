segundos = int(input("Digite os segundos"))
horas = segundos // 3600
segundos = int(segundos - horas * 3600)
minutos = segundos // 60
segundos = segundos - minutos * 60
print(str(horas),":",str(minutos),":",str(segundos))
