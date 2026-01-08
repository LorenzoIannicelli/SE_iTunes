import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self._list_albums = []
        self._dict_albums = {}
        self._map_albums_playlists = {}
        self._G = None


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
        comp =  nx.node_connected_component(self._G, a)
        return comp