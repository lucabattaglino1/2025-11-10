from networkx import DiGraph

from database.DAO import DAO



class Model:
    def __init__(self):
        self._graph = DiGraph()
        self._nodes = []
        self._idMapAO = {}

    def getNomiStore(self):
        return DAO.getAllStores()

    def buildGraph(self, store_name, k):

        self._graph.clear()
        self._nodes = DAO.getAllNodes(store_name)
        self._idMap = {}

        for n in self._nodes:
            self._idMap[n.order_id] = n

        self._graph.add_nodes_from(self._nodes)
        self.addEdges(k)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def addEdges(self, k):
        allEdges = DAO.getAllEdges(k, self._idMap)

        for t in allEdges:
            self._graph.add_edge(t[0], t[1], weight=t[2])

    def getNumEdges(self):
        return len(self._graph.edges)

    # stampare i 5 archi di peso maggiore
    def getTopArchi(self):

        archi = []
        for u, v, dati in self._graph.edges(data=True):
            archi.append((u, v, dati["weight"]))

        # Ordina per peso decrescente
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:5]

    # cammino piu lungo
    def getCamminoLungo(self, nodo_start):
        visited = set()
        max_path = []

        def dfs(node, path):
            nonlocal max_path
            visited.add(node)

            if len(path) > len(max_path):
                max_path = path[:]

            for neighbor in self._graph.successors(node):
                if neighbor not in visited:
                    path.append(neighbor)
                    dfs(neighbor, path)
                    path.pop()
            visited.remove(node)

        dfs(nodo_start, [nodo_start])
        return max_path

    # nel caso mi chiedesse il cammino più corto
    #def getCamminoMinimo(self, source, target):
        #return nx.shortest_path(self._graph, source, target, weight="weight")





