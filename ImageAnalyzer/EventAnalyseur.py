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
    def __init__(self, app, data, Scenario):
        self.app = app
        self.data = data
        self.S = Scenario
    def on_exec_clicked_analyse(self, *args):
        """génération des résultats sous forme de figure"""
        Anlys = Analyseur(self.data, self.S)
        Anlys.set_flags(pl=1 if self.app.pl.get_active() else 0)
        fgs1 = Anlys.gen_hrf(nItmin=self.app.nitmin.get_value_as_int(),
                             nItmax=self.app.nitmax.get_value_as_int(),
                            )
        fgs2 = Anlys.gen_nrl()
        return Resultat(fgs1, fgs2), Anlys
