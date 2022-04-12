import pyomo.environ as pe
#import pyomo.opt as po
from random import choice

# Definition du Graphe

nodes = set()
edges = set()
with open("C:\\Users\\landr\\pyomo2\\fgames120.col.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        newLine = line.split(" ")
        if newLine[0] == "e":
            nodes.add(int(newLine[1]))
            nodes.add(int((newLine[2].split("\n"))[0]))
            edges.add((int(newLine[1]),int((newLine[2].split("\n"))[0])))

# Création du modèle pour la programmation linear integer number
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








