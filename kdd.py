import random
import pandas as pd

tab = pd.read_excel('c:/Users/moniq/Documents/UFAL/IA 2021.1/ID3/tabela.xlsx')

# Retirada de Colunas(Atributos) indesejadas
tab.drop(columns=["ID","Nome","Endereço","Email"],inplace=True)
#print(tab.head(200))


# Transformando Coluna idade para faixa etaria
#print(tab.loc[0:199,["Idade"]])
for x in range(200):
    if tab.loc[x,"Idade"] <= 32:
        tab.loc[x,"Idade"] = "18-32"
    elif tab.loc[x,"Idade"] > 32 and tab.loc[x,"Idade"]<= 46:
        tab.loc[x,"Idade"] = "33-46"
    else:
        tab.loc[x,"Idade"] = "46-60"
#print(tab.loc[0:199,["Idade"]])
#print(tab.head(200))

# Transformando Coluna Trabalha para empregado e desempregado
for x in range(200):
    if tab.loc[x,"Trabalha?"] == True:
        tab.loc[x,"Trabalha?"] = "Empregado"
    else:
        tab.loc[x,"Trabalha?"] = "Desempregado"

# Transformando Coluna Filhos  para Tenho e Não Tenho
for x in range(200):
    if tab.loc[x,"Filhos?"] == True:
        tab.loc[x,"Filhos?"] = "Tenho"
    else:
        tab.loc[x,"Filhos?"] = "NTenho"

# Transformando Coluna Teminou o ensino médio  para Terminei e Não Terminei
for x in range(200):
    if tab.loc[x,"EnsinoMédio?"] == True:
        tab.loc[x,"EnsinoMédio?"] = "Terminei"
    else:
        tab.loc[x,"EnsinoMédio?"] = "NTerminei"

# Transformando Coluna Estudo em escola particular para Fiz e Fiz
for x in range(200):
    if tab.loc[x,"Educação?"] == True:
        tab.loc[x,"Educação?"] = "Particular"
    else:
        tab.loc[x,"Educação?"] = "Publica"

# Transformando Coluna Estudo em escola particular para Fiz e Fiz
for x in range(200):
    if tab.loc[x,"Gênero"] == "Male":
        tab.loc[x,"Gênero"] = "M"
    else:
        tab.loc[x,"Gênero"] = "F"

#Separando tabela para Treinamento(80%) e Teste(20%) Hold Out
#Assim para tabela de 200 casos seram 40 casos teste
lista = []
while(1):
    k = random.randrange(0,200)
    n = 0
    for i in lista:
        if k == i:
            n = 1
    if n == 0:
        lista.append(k)
    if len(lista) == 40:
        #print(lista)
        break

Teste = tab
Treinamento = tab
for i in range(199):
    n = 0 
    for t in lista:
        if t == i:
            n = 1
    if n == 0:
        Teste = Teste.drop(i)
    else:    
        Treinamento = Treinamento.drop(i)

# Add uma coluna para resultado da busca em Teste.xlsx
Teste=Teste.assign(Busca="-")

#print(Teste.head(200))
Teste.to_excel("Teste.xlsx") 
#print(Treinamento.head(200))
Treinamento.to_excel("Treinamento.xlsx") 