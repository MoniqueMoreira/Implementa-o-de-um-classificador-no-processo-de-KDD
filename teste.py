from id3 import grafo
import pandas as pd

#print(grafo.nodes())

#Base de treinamento
def Base():
    Teste = pd.read_excel('c:/Users/moniq/Documents/UFAL/IA 2021.1/KDD/Teste.xlsx')
    Teste.reset_index(inplace=True, drop=True)
    return Teste

def Inicio(Colunas):
    for e in Colunas:
        if Ligados(grafo,"INICIO",e) == True:
            return e

def Variaçoes(Tabela,Atb,T):
    lista = []
    #print(T)
    for i in range(T):
        n=0
        #print(Atb)
        for k in lista:
            if k == Tabela.loc[i,Atb]:
                n = 1
        if n == 0:
            lista.append(Tabela.loc[i,Atb])
            #print(lista)
    return lista

def Ligados(grafo,v1,v2):
    return grafo.has_edge(v1,v2)

def Busca(Teste,T,i,atb,C,):
    if atb == True or atb == False:
        if atb == False:
            Teste.loc[i,"Busca"] = False
            #print(atb,"->","False")
        else:
            Teste.loc[i,"Busca"] = True
            #print(atb,"->","True")
        
        return
    C.remove(atb)
    f = Variaçoes(Teste,atb,T)
    for h in f:
        if Teste.loc[i,atb] == h:
            k=h
            #print("-----",k)
    for t in C:
        if Ligados(grafo, k, t) == True:
            #print(k,"->",t) 
            Busca(Teste,T,i,t,C)

def Metricas(Teste,T):
    VP = 0
    FN = 0
    FP = 0
    VN = 0
    for i in range(T):
        if Teste.loc[i,"Faculdade?"] == True:
            if Teste.loc[i,"Busca"] == True:
                VP = VP + 1
            else:
                 FN = FN + 1
        if Teste.loc[i,"Faculdade?"] == False:
            if Teste.loc[i,"Busca"] == False:
                FP = FP + 1
            else:
                 VN = VN + 1

    print('|VP = {}|\t|FN = {}|\n|FP = {}|\t|VN = {}|'.format(VP,FN,FP,VN))
    Acurácia = (VP + VN)/(VP + VN + FN + FP)
    print("Acurácia = {}".format(Acurácia))
    Erro = (FP + FN)/(VP + VN + FN + FP)
    print("Tx. Erro = {}".format(Erro))
    Recall =  VP / (VP + FN) 
    print("Recall = {:.3f}".format(Recall))
    Precisão = VP / (VP + FP)
    print("Precisão = {:.3f}".format(Precisão))

def Classificador():
    #print(grafo.edges)
    Teste = Base()
    Colunas = ['Idade', 'Gênero', 'Trabalha?', 'Filhos?','EnsinoMédio?','Educação?', True, False]
    T = Teste[Teste.columns[0]].count()
    atb = Inicio(Colunas)
    #print(atb)
    for i in range(T):
        #print(i)
        w = Colunas.copy()
        C= Colunas.copy()
        #print(C)
        Busca(Teste,T,i,atb,C)
        Teste.loc[:, ~Teste.columns.str.match('Unnamed')]
    Teste.to_excel("Teste.xlsx")
    Metricas(Teste,T)
Classificador()