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


class EventResultat:
    """Signal Event Resultat definition"""
    def __init__(self, app, Resultat, Analys):
        self.app = app
        self.Res = Resultat
        self.Analys = Analys
        
    def on_exec_result(self, *args):
        """Execution de résultat"""
        fg = self.Res.Res_Hrf()
        self.app.add_result('fonction de réponse', fg[0])
        self.app.add_result('Mélange à posteriori', fg[1])
        fg1 = self.Res.Res_nrl()
        #fg1 = Res.Res_Nrl()
        self.app.add_result('Niveau de réponse', fg1[0])
        self.app.add_result('Label activation', fg1[1])
        self.app.notebook.set_current_page(2)
        try:
            ttp = dat.dt * (Scen.hrf0.argmax())
        except Exception:
            ttp = 0
        MaxH = max(self.Analys.m_H)
        indMaxH = self.Analys.m_H.argmax()
        mid = (self.Analys.m_H == MaxH / 2).nonzero()
        IndUnder = self.Analys.m_H.argmin()
        Under = self.Analys.m_H.min()
        tmp1 = abs(self.Analys.m_H[0:indMaxH] - MaxH / 2.0)
        tmp2 = abs(self.Analys.m_H[indMaxH:IndUnder] - MaxH / 2.0)
        ind1 = tmp1.argmin()
        try:
            ind2 = indMaxH + tmp2.argmin()
        except Exception:
            ind2 = 0
        FWHM = abs(ind2 - ind1)

        self.app.ttp.set_text(str(ttp))
        self.app.MaxH.set_text(str(MaxH))
        self.app.indMaxH.set_text(str(indMaxH))
        self.app.mid.set_text(str(mid))
        self.app.IndUnder.set_text(str(IndUnder))
        self.app.Under.set_text(str(Under))
        self.app.tmp1.set_text(str(tmp1))
        self.app.tmp2.set_text(str(tmp2))
        self.app.ind1.set_text(str(ind1))
        self.app.ind2.set_text(str(ind2))
        self.app.FWHM.set_text(str(FWHM))
