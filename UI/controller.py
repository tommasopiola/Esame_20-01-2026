import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            n_album = int(self._view.txtNumAlbumMin.value)
        except ValueError:
            self._view.show_alert("Inserire un intero valido")
            return

        self._model.load_artists_with_min_albums(n_album)
        self._model.build_graph()


        n_nodes = self._model.get_number_of_nodes()
        n_edges = self._model.get_number_of_edges()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato!\n"
                    f"Numero di nodi: {n_nodes}\n"
                    f"Numero di archi: {n_edges}"))


        self._view.ddArtist.disabled = False
        self.populate_ddArtists()
        self._view.btnArtistsConnected.disabled = False

        self._view.update_page()

    def handle_connected_artists(self, e):
        artista_id = int(self._view.ddArtist.value)

        artista = self._model._artist_map[artista_id]

        vicini = list(self._model._graph.neighbors(artista))

        #ordino gli artisti collegati per il peso

        #vicini.sort(self, key= vicini[3])

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Artisti collegati all'artista: {artista_id} {artista.name}\n"))


        #lista_edges = list(self._model._graph.edges(artista))
        #lista_edges.sort(key=lambda e: e[2])
        #print(lista_edges)
        '''
        for edge in lista_edges:
            self._view.txt_result.controls.append(
                ft.Text(f"}")
            )'''

        for vi in vicini:
            self._view.txt_result.controls.append(
                ft.Text(f"{vi.id} {vi.name} - Numero di generi in comune: {self._model._graph[artista][vi]['weight']}\n"))

        self._view.txtMaxArtists.disabled = False
        self._view.txtMinDuration.disabled = False
        self._view.btnSearchArtists.disabled = False

        self._view.update_page()


    def populate_ddArtists(self):
        for artista in self._model._graph._node:
            self._view.ddArtist.options.append(ft.dropdown.Option(key=artista.id, text=artista.name))

        self._view.update_page()

    def handle_path(self):
        try:
            d_min = float(self._view.txtMinDuration.value)
            n_art = int(self._view.txtMaxArtists.value)
            artista_id = int(self._view.ddArtist.value)

        except ValueError:
            self._view.show_alert("Inserire un float valido per la durata minima e un intero valido per il numero massimo di artisti")
            return

        artista = self._model._artist_map[artista_id]

        if d_min > 0 and 1 < n_art < len(self._model._graph.neighbors(artista)):
            self._model.get_path(d_min, n_art, artista)


        self._view.txt_result.controls.clear()
        self._view.update_page()