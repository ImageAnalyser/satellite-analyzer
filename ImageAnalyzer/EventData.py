# -*- coding: utf-8 -*-
from gi.repository import Gtk, Gdk, GdkPixbuf
#import Data
from Data import Data
from Data import*
#from scenario import scenario
#from scenario import*
#from Resultat import Resultat
#from Analyseur import Analyseur
#from Analyseur import*


class EventData:
    """Signal Event Data definition"""
    def __init__(self, app, imgs):
        self.app = app
        self.imgs = imgs

    def on_exec_clicked_data(self, *args):
        """Recupération de données a partir de la vue app
        et l'execution de data
        :param imgs:liste d'image
        :type imgs:[]
        """
        D = Data(sorted(self.imgs),
                 bande=float(self.app.bande.get_active_text()),
                 facteur=float(self.app.facteur.get_text()))
        D.xmin = self.app.xmin.get_value_as_int()
        D.xmax = self.app.xmax.get_value_as_int()
        D.ymin = self.app.ymin.get_value_as_int()
        D.ymax = self.app.ymax.get_value_as_int()
        D.lecture_data()
        return D
