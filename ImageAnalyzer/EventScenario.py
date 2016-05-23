# -*- coding: utf-8 -*-
from gi.repository import Gtk, Gdk, GdkPixbuf
#import Data
#from Data import Data
#from Data import*
#from scenario import scenario
from scenario import scenario
#from Resultat import Resultat
#from Analyseur import Analyseur
#from Analyseur import*


class EventScenario:
    """Signal Event scenario definition"""
    def __init__(self, app):
        self.app = app

    def on_exec_scenario(self, *args):
        """Récupération des paramètres d'analyse"""
        Scen = scenario()
        Scen.beta=self.app.beta.get_value()
        Scen.sigmaH=self.app.sigmah.get_value()
        #Scen.v_h_facteur= self.app.vh.get_value()
        #Scen.v_h_facteur=(Scen.v_h_facteur)
        Scen.dt=self.app.dt.get_value_as_int()
        Scen.Thrf=self.app.thrf.get_value_as_int()
        Scen.TR=self.app.tr.get_value_as_int()
        Scen.K=self.app.k.get_value_as_int()
        Scen.M=self.app.m.get_value_as_int()
        Scen.scale=self.app.scale.get_value_as_int()
        return Scen
