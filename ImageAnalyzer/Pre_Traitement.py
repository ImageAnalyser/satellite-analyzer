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


from Data import Data
from scenario import scenario


class Pre_Traitement:
    def __init__(self, data, scen):
        self.scen = scen
        self.data = data 
        #self.Y = Y    
                       
    def trait(self):    
        areas = ['ra']
        labelFields = {}
        cNames = ['inactiv', 'activ']
        height = self.data.getheight()
        width = self.data.getwidth()
        spConf = RegularLatticeMapping((height, width, 1))
        graph = graph_from_lattice(ones((height, width, 1), dtype=int))
        Y = self.data.post_lecture()
        J = Y.shape[0]
        l = int(sqrt(J))
        FlagZ = 1
        q_Z0 = zeros((self.scen.M, self.scen.K, J), dtype=float64)
        if not FlagZ:
            q_Z0 = q_Z
        FlagH = 1
        TT, m_h = getCanoHRF(self.scen.Thrf - self.scen.dt, self.scen.dt)
        hrf0 = hrf0 = array(m_h).astype(float64)
        Sigma_H0 = eye(hrf0.shape[0])
        if not FlagH:
            hrf0 = h_H
            Sigma_H0 = Sigma_H
        return Y, graph, hrf0, Sigma_H0, q_Z0, width, height, FlagZ, FlagH
        
