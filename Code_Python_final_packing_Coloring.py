import random
import pandas as pd
import os
from pathlib import Path
import pyomo.environ as pe
import pyomo.opt as po
from random import choice
from yaml import *

def returnGraphe(file):
    nodes = set()
    edges = set()
    with open(file,'r') as fich:
        lines = fich.readlines()
        for line in lines:
            newWords = line.split(" ")
            if newWords[0] == "e" :
                nodes.add(int(newWords[1]))
                nodes.add(int((newWords[2].split("\n"))[0]))
                edges.add((int(newWords[1]),int((newWords[2].split("\n"))[0])))
    return nodes,edges

def modelClassicAS(*grapheTuple):
    nodes=grapheTuple[0][0]
    edges=grapheTuple[0][1]
    # Création du modèle
    model = pe.ConcreteModel()
    # Définition des paramètres du système et leur initialisation
    model.H = pe.RangeSet(0,max(nodes))
    model.nodes = pe.Set(initialize=nodes)
    model.edges = pe.Set(within=model.nodes*model.nodes, initialize=edges)
    # Définition des variables binaires
    model.x = pe.Var(model.H,model.nodes, domain=pe.Binary)
    model.w = pe.Var(model.H, domain=pe.Binary)
    #Définition de la fonction objective
    model.obj = pe.Objective( sense=pe.minimize, expr = sum(model.w[i] for i in model.H))
    
    #Définition des contrainte
    model.con1 = pe.ConstraintList()
    for v in model.nodes:
        gauche = sum(model.x[i,v] for i in model.H)
        model.con1.add(gauche == 1)
    model.con2 = pe.ConstraintList()
    for (u,v) in model.edges:
        for i in model.H:
            model.con2.add( model.x[i,u]+model.x[i,v] <= model.w[i])
    #je renvoie le model et le nomDuFichier
    return model

def modelClassicSS(*grapheTuple):
    nodes=grapheTuple[0][0]
    edges=grapheTuple[0][1]
    # Création du modèle
    model = pe.ConcreteModel()
    # Définition des paramètres du système et leur initialisation
    model.H = pe.RangeSet(0,max(nodes))
    model.nodes = pe.Set(initialize=nodes)
    model.edges = pe.Set(within=model.nodes*model.nodes, initialize=edges)
    # Définition des variables binaires
    model.x = pe.Var(model.H,model.nodes, domain=pe.Binary)
    model.w = pe.Var(model.H, domain=pe.Binary)
    #Définition de la fonction objective
    model.obj = pe.Objective( sense=pe.minimize, expr = sum(model.w[i] for i in model.H))
    #Définition des contrainte
    model.con1 = pe.ConstraintList()
    for v in model.nodes:
        gauche = sum(model.x[i,v] for i in model.H)
        model.con1.add(gauche == 1)
    model.con2 = pe.ConstraintList()
    for (u,v) in model.edges:
        for i in model.H:
            model.con2.add( model.x[i,u]+model.x[i,v] <= model.w[i])
    model.con3 = pe.ConstraintList()
    for i in model.H:
        model.con3.add( model.w[i] <= sum(model.x[i,v] for v in model.nodes))
    model.con4 = pe.ConstraintList()
    for i in list(model.H)[1:]:
        model.con4.add( model.w[i] <= model.w[i-1] )
     #je renvoie le model et le nomDuFichier
    return model

# Fonction qui renvoie la liste des noeuds non adjacents à un noeud

def notAddjacentnodes(edges,nodes,node):
    node_adj = set()
    for elt in edges:
        if node in elt:
            node_adj.update([elt[0], elt[1]])
    return nodes - node_adj

# Fonction qui renvoie la liste des liens formés des noeuds non adjacents à un noeud

def notAddjacentedges(edges,notAdjnodes):
    edge_adj = set()
    for (v,w) in edges:
        if (v in notAdjnodes) and (w in notAdjnodes):
            edge_adj.add((v,w))
    return edge_adj

def modelrepreAS(*grapheTuple):
    nodes=grapheTuple[0][0]
    edges=grapheTuple[0][1]
    # Création du modèle
    model = pe.ConcreteModel()
    # Définition des paramètres
    model.nodes = pe.Set(initialize=nodes)
    model.edges = pe.Set(within=model.nodes*model.nodes, initialize=edges)
    model.x = pe.Var(model.nodes,model.nodes, domain=pe.Binary)
    #Définition de la fonction objective
    model.obj = pe.Objective(sense=pe.minimize, expr=sum(model.x[u,u]for u in model.nodes))
    #Définition des contraintes des nodes adjacents
    model.con1 = pe.ConstraintList()
    for (u,v) in model.edges:
        model.con1.add(model.x[u,v] + model.x[v,u]==0)
    #Définition des contraintes des nodes non adjacents
    model.con2 = pe.ConstraintList()
    for v in model.nodes:
        not_adj = list(notAddjacentnodes(model.edges,model.nodes,v))
        not_adj.append(v)
        gauche = sum(model.x[u,v] for u in not_adj)
        model.con2.add(gauche >= 1)
    model.con3 = pe.ConstraintList()
    for u in model.nodes:
        for (v,w) in notAddjacentedges(model.edges,notAddjacentnodes(model.edges,model.nodes,u)):
            gauche = model.x[u,v] + model.x[u,w]
            droite = model.x[u,u]
            model.con3.add(gauche <= droite)
    #je renvoie le model et le nomDuFichier
    return model

def modelrepreSS(*grapheTuple):
    nodes=grapheTuple[0][0] 
    edges=grapheTuple[0][1]
    # Création du modèle
    model = pe.ConcreteModel()
    # Définition des paramètres
    model.nodes = pe.Set(initialize=nodes)
    model.edges = pe.Set(within=model.nodes*model.nodes, initialize=edges)
    model.x = pe.Var(model.nodes,model.nodes, domain=pe.Binary)
    #Définition de la fonction objective
    model.obj = pe.Objective(sense=pe.minimize, expr=sum(model.x[u,u]for u in model.nodes))
    #Contrainte d'elimination de tous les nodes adjacents
    model.con1 = pe.ConstraintList()
    for (u,v) in model.edges:
        model.con1.add(model.x[u,v] + model.x[v,u]==0)
        #Contrainte d'elimination de la symétrie du modèle des representants (on prend comme representant le plus petit node)
    model.con2 = pe.ConstraintList()
    for u in  model.nodes:
        for v in model.nodes:
            if u > v:
                model.con2.add(model.x[u,v]==0)
    #Définition des contraintes des nodes non adjacents
    model.con3 = pe.ConstraintList()
    for v in model.nodes:
        not_adj = list(notAddjacentnodes(model.edges,model.nodes,v))
        not_adj.append(v)
        gauche = sum(model.x[u,v] for u in not_adj)
        model.con3.add(gauche >= 1)
    model.con4 = pe.ConstraintList()
    for u in model.nodes:
        for (v,w) in notAddjacentedges(model.edges,notAddjacentnodes(model.edges,model.nodes,u)):
            gauche = model.x[u,v] + model.x[u,w]
            droite = model.x[u,u]
            model.con4.add(gauche <= droite)
    #je renvoie le model et le nomDuFichier
    return model

def modelpop(*grapheTuple):
    nodes=grapheTuple[0][0]
    edges=grapheTuple[0][1]
    
    # Création du modèle
    model = pe.ConcreteModel()
    
    # Définition des paramètres
    model.nodes = pe.Set(initialize=nodes)
    model.edges = pe.Set(within=model.nodes*model.nodes, initialize=edges)
    model.H = pe.RangeSet(1,max(nodes))
    
        # définition des variables binaires
    model.y = pe.Var(model.H, model.nodes, domain=pe.Binary)
    model.z = pe.Var(model.nodes, model.H, domain=pe.Binary)

     # q est un sommet arbitraire ou aléatoire
    q = choice(list(model.nodes))


    #Définition de la fonction objective
    model.obj = pe.Objective(sense=pe.minimize, expr = 1 + sum(model.y[i,q]
                                                            for i in model.H))

    #Définition des contraintes
    model.con1 = pe.ConstraintList()
    for v in model.nodes:
        model.con1.add(model.z[v,1] == 0)

    model.con2 = pe.ConstraintList()
    for v in model.nodes:
        model.con2.add(model.y[max(model.H),v] == 0)

    model.con3 = pe.ConstraintList()
    for v in model.nodes:
        for i in list(model.H)[:-1]:
            model.con3.add(model.y[i,v] - model.y[i+1,v] >= 0)

    model.con4 = pe.ConstraintList()
    for v in model.nodes:
        for i in list(model.H)[:-1]:
            model.con4.add(model.y[i,v] + model.z[v,i+1] == 1)

    model.con5 = pe.ConstraintList()
    for (u,v) in model.edges:
        for i in model.H:
            model.con5.add(model.y[i,u] + model.z[u,i] + model.y[i,v] + model.z[v,i] >= 1)

    model.con6 = pe.ConstraintList()
    for v in model.nodes:
        for i in list(model.H)[:-1]:
            model.con6.add(model.y[i,q] - model.y[i,v] >= 0)

    #je renvoie le model et le nomDuFichier
    return model

def modelpop2(*grapheTuple):
    nodes=grapheTuple[0][0]
    edges=grapheTuple[0][1]
    
    # Création du modèle
    model = pe.ConcreteModel()
    
    # Définition des paramètres
    model.nodes = pe.Set(initialize=nodes)
    model.edges = pe.Set(within=model.nodes*model.nodes, initialize=edges)
    model.H = pe.RangeSet(1,max(nodes))

    # définition des variables binaires
    model.y = pe.Var(model.H, model.nodes, domain=pe.Binary)
    model.z = pe.Var(model.nodes, model.H, domain=pe.Binary)
    model.x = pe.Var(model.nodes, model.H, domain=pe.Binary)

     # q est un sommet arbitraire ou aléatoire
    q = choice(list(model.nodes))


    #Définition de la fonction objective
    model.obj = pe.Objective(sense=pe.minimize, expr = 1 + sum(model.y[i,q]
                                                            for i in model.H))

    #Définition des contraintes
    model.con1 = pe.ConstraintList()
    for v in model.nodes:
        model.con1.add(model.z[v,1] == 0)

    model.con2 = pe.ConstraintList()
    for v in model.nodes:
        model.con2.add(model.y[max(model.H),v] == 0)

    model.con3 = pe.ConstraintList()
    for v in model.nodes:
        for i in list(model.H)[:-1]:
            model.con3.add(model.y[i,v] - model.y[i+1,v] >= 0)

    model.con4 = pe.ConstraintList()
    for v in model.nodes:
        for i in list(model.H)[:-1]:
            model.con4.add(model.y[i,v] + model.z[v,i+1] == 1)

    model.con5 = pe.ConstraintList()
    for (u,v) in model.edges:
        for i in model.H:
            model.con5.add(model.y[i,u] + model.z[u,i] + model.y[i,v] + model.z[v,i] >= 1)

    model.con6 = pe.ConstraintList()
    for v in model.nodes:
        for i in list(model.H)[:-1]:
            model.con6.add(model.y[i,q] - model.y[i,v] >= 0)

    # Reduction du nombre de variables non nulles et vérification de l'unicité de la clr du sommet
    model.con7 = pe.ConstraintList()
    for (u,v) in model.edges:
        for i in model.H:
            model.con7.add(model.x[u,i] + model.x[v,i] <= 1)
        
    #je renvoie le model et le nomDuFichier
    return model


def executionModel(model):
    solver = po.SolverFactory('cplex')
    solver.options['timelimit'] = 1200
    resultat = solver.solve(model,tee=True)
    return resultat

if __name__== "__main__" :
    cheminFiles="C:\\Users\\landr\\OneDrive\\Bureau\\instances\\"
    files=os.listdir(cheminFiles)#Repertoire où le programme va rechercher le jeux de donnees
    liste=["fichierResultatModel_ClassicAS","fichierResultatModel_ClassicSS","fichierResultatModel_RepreAS",
           "fichierResultatModel_RepreSS","fichierResultatModel_pop","fichierResultatModel_pop2"]
    for elt in liste:
        for filename in files:
           #if(filename.endswith(".col")or filename.endswith(".txt")):
            if(filename.endswith(".txt")):
                graphe=returnGraphe(filename)
                if(elt=="fichierResultatModel_ClassicAS"):
                    model=modelClassicAS(graphe)
                elif(elt=="fichierResultatModel_ClassicSS"):
                    model=modelClassicSS(graphe)
                elif(elt=="fichierResultatModel_RepreAS"):
                    model=modelrepreAS(graphe)
                elif(elt=="fichierResultatModel_RepreSS"):
                    model=modelrepreSS(graphe)
                elif(elt=="fichierResultatModel_pop"):
                    model=modelpop(graphe)    
                else:
                    model=modelpop2(graphe)
                result=executionModel(model)
                #Repertoire ou il va stocker  le resultat
                chemin="C:\\Users\\landr\\OneDrive\\Bureau\\ResultatTest\\"+elt[:]+"\\"+filename[:-4]+".txt"
                with open(chemin,'a')as file:
                  file.write(str(result))
