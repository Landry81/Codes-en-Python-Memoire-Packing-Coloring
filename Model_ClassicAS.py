# knapsack.py
import pyomo.environ as pe
import pyomo.opt as po


# Definition du Graphe

nodes = set()
edges = set()

# C:\Users\landr\pyomo2
# split() => methode qui permet de casser ou separer une chaine de caracteres en 1 ou plusieurs morceaux

with open("C:\\Users\\landr\\pyomo2\\fdavid.col.txt", "r") as file:
    lines = file.readlines()  #Vecteur de lignes=(c FILE: myciel3.col, c SOURCE: Michael Trick (trick@cmu.edu), etc...)
    for line in lines:
        newWords = line.split(" ") #Vecteur de mots=((c,FILE:,myciel3.col),(c,SOURCE:,Michael,Trick,(trick@cmu.edu)),(e,1,3),(e,1,4),etc...)
        if newWords[0] == "e":
            nodes.add(int(newWords[1])) #casting en integer du 2eme elt du vecteur de mot car newWord[1] est un String  
            nodes.add(int((newWords[2].split("\n"))[0])) #{newWords[2].split("\n")}[0] => ("2\n" devient "2" "\n" et on prend le 1er elt du tab[0]=2
            edges.add((int(newWords[1]),int((newWords[2].split("\n"))[0])))

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

#pyomo solve --solver=cplex test.py

#solver = po.SolverFactory('cplex')
#results = solver.solve(model,tee=True)
#print (results)
