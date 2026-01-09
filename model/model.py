import copy

import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self._list_albums = []
        self._dict_albums = {}
        self._map_albums_playlists = {}
        self._G = None

        self._comp = None

        self._best_set_album = None
        self._duration = None


    def get_albums(self):
        return self._list_albums

    def build_graph(self, d):
        self._G = nx.Graph()

        self._list_albums = DAO.read_albums(d)
        for album in self._list_albums:
            self._dict_albums[album.id] = album

        self._G.add_nodes_from(self._list_albums)

        self._map_albums_playlists = DAO.get_album_playlist_map(self._list_albums, self._dict_albums)

        for i, a1 in enumerate(self._list_albums):
            for a2 in self._list_albums[i+1:]:
                if self._map_albums_playlists[a1].intersection(self._map_albums_playlists[a2]):
                    self._G.add_edge(a1, a2)

        return self._G.number_of_nodes(), self._G.number_of_edges()

    def get_connected_comp(self, a_id):
        a = self._dict_albums[a_id]
        self._comp =  nx.node_connected_component(self._G, a)
        return self._comp

    def get_set_album(self, id_album, tot_d):
        comp = list(self._comp)
        album = self._dict_albums[id_album]
        self._best_set_album = []

        self._ricorsione([album], comp, tot_d, album.duration)
        return self._best_set_album, self._duration

    def _ricorsione(self, parziale, albums, tot_d, current_duration):
        if len(parziale) > len(self._best_set_album):
            self._best_set_album = copy.deepcopy(parziale)
            self._duration = current_duration

        for i, a in enumerate(albums):
            if a in parziale:
                continue

            new_duration = current_duration + a.duration
            if new_duration < tot_d:
                parziale.append(a)
                self._ricorsione(parziale, albums, tot_d, new_duration)

                parziale.pop()