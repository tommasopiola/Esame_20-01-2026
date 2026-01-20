import networkx as nx
from database.dao import DAO
from model.artist import Artist

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self._artist_map = {}

        self.load_all_artists()
        self._artisti_selez = []

        self._nodes = []
        self._edges = []

        self._best_sol = []
        self._best_peso = 0

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        for artist in self._artists_list:
            self._artist_map[artist.id] = artist
        #print(f"Artisti: {self._artists_list}")


    def load_artists_with_min_albums(self, min_albums):
        self._artisti_selez = DAO.get_artisti_selez(min_albums)

        for artist in self._artisti_selez:
            #print(artist)
            nodo = self._artist_map[artist]
            #print(nodo)

            self._nodes.append(nodo)


    def build_graph(self):
        self._graph.clear()

        self._graph.add_nodes_from(self._nodes)

        self._edges = DAO.get_artist_collegati()
        for edge in self._edges:

            nodo_u = self._artist_map[edge[0]]
            nodo_v = self._artist_map[edge[1]]
            peso = edge[2]

            if nodo_u in self._graph and nodo_v in self._graph:
                self._graph.add_edge(nodo_u, nodo_v, weight=peso)


    def get_number_of_nodes(self):
        print(len(self._graph.nodes))
        return self._graph.number_of_nodes()

    def get_number_of_edges(self):
        print(len(self._graph.edges))
        return self._graph.number_of_edges()

    def get_path(self, d_min, n_art, artista):
        #artista viene già passato come nodo
        durata_minima = float(d_min)
        num_artisti = int(n_art)

        self._best_sol = []
        self._best_peso = -1

        parziale = []
        parziale.append(artista)

        self._ricorsione(parziale, 0, d_min, n_art)
        return self._best_sol, self._best_peso


    def _ricorsione(self, parziale, costo_corr, d_min, n_art):
        ultimo_nodo = parziale[-1]

        # caso finale
        if len(parziale) == n_art:
            if costo_corr > self._best_peso:
                self._best_peso = costo_corr
                self._best_sol = list(parziale)
            return
        pass


'''
def _ricorsione_max(self, parziale, costo_corr, target):
    ultimo_nodo = parziale[-1]

    # 1. CASO BASE (Ho raggiunto la destinazione)
    if ultimo_nodo == target:
        # Qui DEVO controllare se ho fatto meglio
        if costo_corr > self.best_cost:
            self.best_cost = costo_corr
            self.best_path = list(parziale)
        return

    # 2. ESPLORAZIONE VICINI
    # Qui è CRUCIALE filtrare i nodi già visitati in 'parziale' per non andare in loop
    vicini = [n for n in self.grafo.neighbors(ultimo_nodo) if n not in parziale]

    for v in vicini:
        peso = self.get_peso(ultimo_nodo, v)

        parziale.append(v)

        self._ricorsione_max(parziale, costo_corr + peso, target)

        parziale.pop()
'''