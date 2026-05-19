from model.model import Model

mymodel=Model()
mymodel.buildGraph(2000)

n,a = mymodel.getGraphDetails()
print(f"numero nodi: {n}, numero archi {a}")
c = mymodel.getNumCompConnesse()
print(f"numero comp connesse: {c}")

# Metti questi print temporanei dentro il tuo controller o tstModel per stanare il bug:
print(f"Nodi totali registrati nel grafo: {n}")
print(f"Archi totali registrati nel grafo: {a}")

# Vediamo quanti nodi isolati (grado 0) vede NetworkX
isolati = [nn for nn in mymodel._graph.nodes if mymodel._graph.degree(nn) == 0]
print(f"Stati isolati (senza confini terrestri) visti da NetworkX: {len(isolati)}")