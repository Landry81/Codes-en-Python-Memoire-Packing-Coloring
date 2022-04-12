import pyomo.environ as pe
import pyomo.opt as po

# Definition du Graphe

nodes = set()
edges = set()
with open("C:\\Users\\landr\\pyomo2\\fqueen8_8.col.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        newWords = line.split(" ")
        if newWords[0] == "e":
            nodes.add(int(newWords[1]))
            nodes.add(int((newWords[2].split("\n"))[0]))
            edges.add((int(newWords[1]),int((newWords[2].split("\n"))[0])))

# Création du modèle

model = pe.ConcreteModel()

# Définition des paramètres

model.nodes = pe.Set(initialize=nodes)
model.edges = pe.Set(within=model.nodes*model.nodes, initialize=edges)
model.x = pe.Var(model.nodes,model.nodes, domain=pe.Binary)

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



#Définition de la fonction objective

model.obj = pe.Objective(sense=pe.minimize, expr=sum(model.x[u,u]
                                                        for u in model.nodes))

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

#pyomo solve --solver=cplex Model_Repres.py

#solver = po.SolverFactory('cplex')
#results = solver.solve(model,tee=True)
#print (results)
