# -*- coding: utf-8 -*-
from gi.repository import Gtk, Gdk, GdkPixbuf
import Data
from Data import Data
from Data import*
from scenario import scenario
from scenario import*
from Resultat import Resultat
from Analyseur import Analyseur
from Analyseur import*


class EventAnalyseur:
    """Signal Event Analyseur definition"""
    def __init__(self, app, Analys):
        self.app = app
        #self.data = data
        self.Analys = Analys
        #self.Pt = Pt
        
    def on_exec_clicked_analyse(self, *args):
        """génération des résultats sous forme de figure"""
        #Anlys = Analyseur(self.Pt)
        #Anlys.set_flags(pl=1 if self.app.pl.get_active() else 0)
        self.Analys.Vbjde(nItmin=self.app.nitmin.get_value_as_int(),nItmax=self.app.nitmax.get_value_as_int())
                  
        
