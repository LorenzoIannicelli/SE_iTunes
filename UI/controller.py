import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.selected_album = None

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try :
            duration = int(self._view.txt_durata.value)
            albums, edges = self._model.build_graph(duration)

            self._view.lista_visualizzazione_1.controls.clear()
            txt = f'Grafo creato: {albums} album, {edges} archi'
            self._view.lista_visualizzazione_1.controls.append(ft.Text(txt))
            self._view.update()

            self.populate_dd()

        except ValueError :
            self._view.show_alert('Inserire un valore valido per la durata (int).')

    def populate_dd(self):
        dd = self._view.dd_album
        albums = self._model.get_albums()

        dd.options.clear()
        for a in albums:
            dd.options.append(ft.DropdownOption(key=a.id, text=a.title))

        self._view.update()


    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        self.selected_album = int(self._view.dd_album.value)

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        comp = self._model.get_connected_comp(self.selected_album)
        dim_comp = len(comp)
        tot_duration = 0
        for a in comp:
            tot_duration += a.duration

        txt1 = f'Dimensione componente: {dim_comp}'
        txt2 = f'Durata toale: {tot_duration:.2f} minuti'

        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(txt1))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(txt2))
        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        try :
            tot_duration = int(self._view.txt_durata_totale.value)
            album_set, duration = self._model.get_set_album(self.selected_album, tot_duration)

            self._view.lista_visualizzazione_3.controls.clear()
            txt1 = f'Set trovato ({len(album_set)} album, durata {duration:.2f} minuti):'
            self._view.lista_visualizzazione_3.controls.append(ft.Text(txt1))
            for a in album_set:
                self._view.lista_visualizzazione_3.controls.append(ft.Text(a))
            self._view.update()

        except ValueError :
            self._view.show_alert('Inserire un valore valido per la durata totale (int).')