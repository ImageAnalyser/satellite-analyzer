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
    def __init__(self, app, Resultat, Analys, data, scen, pt):
        self.app = app
        self.Res = Resultat
        self.Analys = Analys
        self.data = data
        self.scen = scen
        self.pt = pt
        
    def on_exec_result(self, *args):
        """Execution de résultat"""
        Analys = Analyseur(self.pt, self.scen, self.data)
        m_A, q_Z, mu_k, m_H, sigma_k, width, height, hrf0 = Analys.Vbjde()
        self.Res.set_flags(pl=1 if self.app.pl.get_active() else 0)
        fgs1 = self.Res.gen_hrf()
        #fgs2 = Anlys.gen_nrl()
        #return Resultat(fgs1, fgs2), Anlys
        #fg = self.Res.Res_Hrf()
        self.app.add_result('fonction de réponse', fgs1[0])
        self.app.add_result('Mélange à posteriori', fgs1[1])
        fg1 = self.Res.gen_nrl()
        #fg1 = Res.Res_Nrl()
        self.app.add_result('Niveau de réponse', fg1[0])
        self.app.add_result('Label activation', fg1[1])
        self.app.notebook.set_current_page(2)
        #try:
        ttp = self.scen.dt * (hrf0.argmax())
        #except Exception:
         #   ttp = 0
        MaxH = max(m_H)
        indMaxH = m_H.argmax()
        #mid = (m_H == MaxH / 2).nonzero()
        #IndUnder = m_H.argmin()
        #Under = m_H.min()
        tmp1 = abs(m_H[0:indMaxH] - MaxH / 2.0)
        #tmp2 = abs(m_H[indMaxH:IndUnder] - MaxH / 2.0)
        #ind1 = tmp1.argmin()
        #try:
        #ind2 = indMaxH + tmp2.argmin()
        #except Exception:
        #    ind2 = 0
        #FWHM = abs(ind2 - ind1)

        self.app.ttp.set_text(str(ttp))
        self.app.MaxH.set_text(str(MaxH))
        self.app.indMaxH.set_text(str(indMaxH))
        #self.app.mid.set_text(str(mid))
        #self.app.IndUnder.set_text(str(IndUnder))
        #self.app.Under.set_text(str(Under))
        self.app.tmp1.set_text(str(tmp1))
        #self.app.tmp2.set_text(str(tmp2))
        #self.app.ind1.set_text(str(ind1))
        #self.app.ind2.set_text(str(ind2))
        #self.app.FWHM.set_text(str(FWHM))
        #return fgs1, fg1
