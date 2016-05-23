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
from Pre_Traitement import Pre_Traitement

class Analyseur:
    """
    Analyser les scénarios d'analyse avec les data en entrées
    :param width: largeur en sortie
    :type width: int
    :param height: hauteur en sortie
    :int height: int
    """
    def __init__(self, Pt, scen, data):
		self.Pt = Pt
		self.scen = scen
		self.data = data
    
    
        
    def Vbjde(self,  
              nItmax=30,
              nItmin=30,
             ):
        """
        allow to generate figures	

        :param nItMin: Minimum number of iteration
        :type nItMin: int
        :param nItMax: Maximum number of iteration
        :type nItMax: int 
        :param estimateSigmaH: estimation of sigmaH
        :type estimateSigmaH: int
        :param estimateBeta: estimation of Beta
        :type estimateBeta: int   
        :param scale: scale factor
        :type scale: int
        """ 
        estimateSigmaH=0
        Onsets={'nuages': array([0])}
        estimateBeta=0
        pl=1
        #FlagZ=1
        #FlagH=1
        Y, graph, hrf0, Sigma_H0, q_Z0, width, height, FlagZ, FlagH = self.Pt.trait()
        m_A, m_H, q_Z, sigma_epsilone, mu_k, sigma_k, Beta, PL, Sigma_A, XX, Sigma_H = \
        Main_vbjde_Extension_TD(FlagH, hrf0, Sigma_H0, height, width, q_Z0, FlagZ,
        pl, graph, Y, Onsets, self.scen.Thrf, self.scen.K, self.scen.TR,
        self.scen.beta, self.scen.dt, self.scen.scale, estimateSigmaH, self.scen.sigmaH,
        nItmin, estimateBeta) 
        #fgs = self.ConditionalNRLHist(m_A, q_Z)
        return m_A, q_Z, mu_k, m_H, sigma_k, width, height, hrf0

        

