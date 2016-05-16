#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from math import pi, sqrt
from numpy import (
    arange, array, power, exp, asarray, float64, zeros, ones, linspace, eye
)
from pylab import (
    show, legend, hold, matshow, colorbar, reshape, savefig, std, mean, title,
    plot, figure, find, figtext, suptitle
)

from scipy import stats
from matplotlib.pyplot import get_cmap, cm, subplots
from pyhrf.boldsynth.hrf import getCanoHRF
from pyhrf.graph import graph_from_lattice
from pyhrf.vbjde.Utils import Main_vbjde_Extension_TD
from pyhrf.boldsynth.boldsynth.scenarios import RegularLatticeMapping
import pyhrf.verbose
from tifffile import imread


class Resultat:
    """
    Affichage des Résultats
    :param hrf: liste des figures HRF
    :type hrf: []
    :param Nrl: liste des figures NRL
    :type Nrl: []
    """
    
    def __init__(self, hrf, nrl):
        self.hrf = hrf
        self.nrl = nrl
   
    def Res_Hrf(self):
        """Resultat de la HRF"""
        #fg = Analyseur.gen_hrf(nitmin, nitmax, scale)
        #if Analyseur.shower == 1:
        #    show()
        return self.hrf

    def Res_nrl(self):
        """Resultat de la NRL"""
        #fgs = Analyseur.gen_nrl()
        #if Analyseur.shower == 1:
        #    show()
        return self.nrl
