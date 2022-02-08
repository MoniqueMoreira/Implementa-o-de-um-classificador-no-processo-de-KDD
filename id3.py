from turtle import pos
import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx
import pandas as pd

#Base de treinamento
Treinamento = pd.read_excel('c:/Users/moniq/Documents/UFAL/IA 2021.1/KDD/Treinamento.xlsx')

grafo = nx.Graph()

#Achando quantidade de variações
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

# Entropia Total
def Entropia_total(Tabela,Res, Atb, T):
    E_t = Entropia(Tabela,Res,T) - Entropia_Atb(Tabela,Res,Atb,T)
    #print(E_t)
    return E_t

#Entropia do atributo
def Entropia_Atb(Tabela,Res, Atb,T):
    lista_var_atb = Variaçoes(Tabela,Atb,T)
    lista_var_res = Variaçoes(Tabela,Res,T)
    
    #print(lista_var_atb)
    #print(lista_var_res)
    
    numero_casos = []
    E_st = []
    E_Atb_t = 0 

    for u in lista_var_atb:
        #print("----",u)
        quantidades = []
        Sv =0 
        for w in lista_var_res:
            n = 0
            for i in range(T):
                if Tabela.loc[i,Atb] == u:
                    if Tabela.loc[i,Res] == w:  
                        Sv = Sv + 1
                        n = n+1
            quantidades.append(n)

        numero_casos.append(Sv)
        '''
        print("Quantidade",quantidades)
        print("Casos",numero_casos)
        '''
        E_s = 0 
        for y in range(len(quantidades)):
            #print("Quantidade",quantidades[y])
            #print("Casos",Sv)
            quantidades[y] = quantidades[y]/Sv
            if quantidades[y] != 0:
                E_s= E_s - (quantidades[y]*math.log(quantidades[y],2))
        
        E_st.append(E_s)
        #print(E_st)

    for v in range(len(E_st)):
        E_Atb_t = E_Atb_t + (E_st[v]*numero_casos[v]/T)
    #print(E_Atb_t)
    return E_Atb_t

# Entropia
def Entropia(Tabela,Atb,T):
    #print(Atb)
    lista = Variaçoes(Tabela,Atb,T)
    
    quantidades = []
    for u in lista:
        #print(Tabela.loc[i,"Irá para faculdade?"])
        n = 0
        for i in range(T):
            if Tabela.loc[i,Atb] == u:
                n= n + 1
        quantidades.append(n)
    #print(quantidades)
    E_s =0 
    for y in range(len(quantidades)):
        quantidades[y] = quantidades[y]/T
        E_s= E_s - (quantidades[y]*math.log(quantidades[y],2))
    #print(E_s)
    return E_s
    

# ID3
def ID3(Tabela,Atributos,Res,T,grafo,Atb_usado):
    Classes = Variaçoes(Tabela,Res,T)
    #print(Classes)
    if len(Classes) > 1:
        #print(len(Atributos))
        if len(Atributos) > 0:
            esc = 0.0
            menor_E = 99999999
            for g in Atributos:
                #print(g)
                esc=Entropia_total(Tabela,Res,g,T)
                if esc < menor_E:
                    z = g 
                    menor_E=esc

            Atb = Variaçoes(Tabela,z,T)
            groups = Tabela.groupby(z)
            Atributos.remove(z)
            #print(Atributos)
            grafo.add_node(z)
            grafo.add_edge(Atb_usado,z)
            for i in Atb:
                #print(i)
                b = groups.get_group(i)
                
                grafo.add_node(i)
                #print(grafo.nodes())
                
                b.reset_index(inplace=True, drop=True)
                b.loc[:, ~b.columns.str.match('Unnamed')]
                c = b[[z,Res]]
                #print(c.head(160))
                b = b.drop(columns=[z])
                T = b[b.columns[0]].count()
                ID3(b,Atributos,Res,T,grafo,i)
                grafo.add_edge(z,i)
                
        else:
            qt = []
            for u in Classes:
                n = 0
                for i in range(T):
                    if Tabela.loc[i,Res] == u:
                        n= n + 1
                qt.append(n)
            if qt[0] == qt[1]:
                grafo.add_node(False)
                grafo.add_edge(Atb_usado,False)
            else:
                if qt[0]>qt[1]:
                    escolhido = Classes[0]
                else:
                    escolhido = Classes[1]
                grafo.add_node(escolhido)
                grafo.add_edge(Atb_usado,escolhido)
            return
            
    else:
        if Classes[0] ==True:
            grafo.add_node(True)
            grafo.add_edge(Atb_usado,True)
        else:
            grafo.add_node(False)
            grafo.add_edge(Atb_usado,False)
        return
   
def Menu():
    Tabela = Treinamento
    
    grafo.add_node("INICIO")
    Res = "Faculdade?"
    T = 160
    Atributos = ['Idade', 'Gênero', 'Trabalha?', 'Filhos?','EnsinoMédio?','Educação?']
    #print(Atributos)
    ID3(Tabela,Atributos,Res,T,grafo,"INICIO")
    pos = nx.spring_layout(grafo, seed=10)
    nx.draw(grafo,pos,with_labels=True)
    plt.savefig("grafo.png")

Menu()

