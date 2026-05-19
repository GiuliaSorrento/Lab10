import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._graph = nx.Graph()  #grafo non orientato (anche non pesato in questo caso)
        self._idMapCountry = {}

    def buildGraph(self, anno):
        self._graph.clear() #pulire sempre il grafo inizialmente
        nodes = DAO.getAllNodes(anno)
        self._graph.add_nodes_from(nodes)  #popolo grafo con nodi
        self._idMapCountry = {country.CCode: country for country in nodes}  #popolo idMap
        self.addEdges(anno)

    def addEdges(self, anno):
        allEdges = DAO.getAllEdges(anno)
        for confine in allEdges:
            country1=self._idMapCountry.get(confine.nazione1)
            country2 = self._idMapCountry.get(confine.nazione2)   #usa sempre .get perchè se è none non ti da errore
            #AGGIUNGI ARCO SOLO SE ENTRAMBI GLI OGGETTI ESISTONO NELLA MAPPA
            if country1 and country2:
                 self._graph.add_edge(country1, country2) #no peso

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getStati(self):
        #Stampare l’elenco degli stati, indicando per ciascuno il numero di stati confinanti (grado del vertice)
        allStati = list(self._graph.nodes) #NB. SE RICHIAMI IL METODO DRL DAO PER PRENDERTI GLI STATI TE NE MANDA DI NUOVI CHE IL TUO GRAFO NON RICONOSCE
        #IL METODO DEL DAO PER PRENDERE I NODI E DA USARE UNA SOLA VOLTA QUANDO POPOLI IL GRAFO
        allGradi = list(self._graph.degree(allStati))  #ritorna una lista di tuple con nodo e proprio grado
        allGradi.sort(key=lambda x: x[0].StateNme)
        #sort: (key=lambda variabile: modo in cui ordinare la variabile)
        return allGradi

    def getNumCompConnesse(self):
        #Stampare il numero di componenti connesse nel grafo.
        return nx.number_connected_components(self._graph)

    def getAllStati(self):
        return list(self._graph.nodes)  #lista di oggetti di tipo stato, tutti quelli del grafo

    def get_raggiungibili_iterativo(self, stato_partenza):
        # Implementazione manuale richiesta dalla traccia
        visitati = []  # Lista dei nodi già esplorati definitivamente
        da_visitare = []  # Lista (fringe/frontiera) dei nodi da esplorare

        # Si inizia inserendo lo stato scelto nella lista daVisitare
        da_visitare.append(stato_partenza)

        # L'algoritmo continua fino a quando la lista dei nodi daVisitare non si svuota
        while len(da_visitare) > 0:
            # Estraiamo il primo nodo dalla lista (politica FIFO, tipica della visita in ampiezza BFS)
            corrente = da_visitare.pop(0)

            # Prendiamo tutti i nodi vicini a quello estratto nel grafo
            vicini = list(self._graph.neighbors(corrente))

            for vicino in vicini:
                # Inseriamo i vicini nella lista daVisitare solo se non sono già stati visitati
                # e se non sono già in coda per essere visitati
                if vicino not in visitati and vicino not in da_visitare:
                    da_visitare.append(vicino)

            # Infine, il nodo estratto viene inserito nella lista dei Visitati
            if corrente not in visitati:
                visitati.append(corrente)

        # La traccia dice "lista di tutti i nodi raggiungibili A PARTIRE da un vertice".
        # Se vogliamo escludere lo stato di partenza stesso dal conteggio dei raggiungibili:
        if stato_partenza in visitati:
            visitati.remove(stato_partenza)

        return visitati

    def get_raggiungibili_nx(self, stato_partenza):
        # Metodo alternativo usando NetworkX
        # nx.node_connected_component restituisce un set con tutti i nodi della componente connessa
        componente = nx.node_connected_component(self._graph, stato_partenza)

        lista_raggiungibili = list(componente)
        if stato_partenza in lista_raggiungibili: #il nodo iniziale non deve far parte della componente connessa
            lista_raggiungibili.remove(stato_partenza)

        return lista_raggiungibili