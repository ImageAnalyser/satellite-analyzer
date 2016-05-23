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


class scenario:
    """
	initialization parameters for the analysis method ConditionalNRLHist
    :param beta: paramétre de regularité spaciale 
    :type beta: float
    :param sigmaH: paramétre de lissage de la HRF
    :type sigmaH: float 
    :param v_h_facteur:hyper parametre 
    :type v_h_facture: float
    :param dt: pas d'echelle Temporel de la HRF
    :type dt: float   
    :param Thrf: durée
    :type Thrf: int
    :param TR: temps de repetition
    :type TR: int
    :param K: nombre de class
    :type K: int
    :param M: nombre de coordonnées experimontales
    :type M: int
    """

    def __init__(self):
        self._beta = 0.1
        self._sigmaH = 0.01
        #self._v_h_facteur = 0.1 * self._sigmaH
        self._dt = 1
        self._Thrf = 4
        self._TR = 1
        self._K = 2
        self._M = 1
        self._scale = 1
        
    @property
    def beta(self):
        return self._beta

    @property
    def sigmaH(self):
		return self._sigmaH
	
    @property
    def v_h_facteur(self):
		return self._v_h_facteur
    
    @property
    def dt(self):
        return self._dt
    
    @property
    def Thrf(self):
		return self._Thrf
	
    @property
    def TR(self):
		return self._TR
	
    @property
    def k(self):
		return self._k
	
    @property
    def M(self):
		return self._M
	
    @property
    def scale(self):
		return self._scale
    
    @beta.setter
    def beta(self, value):
	    self._beta = value

    @sigmaH.setter
    def sigmaH(self, value):
        self._sigmaH = value

	@v_h_facteur.setter
	def v_h_facteur(self, value):
	    self._v_h_facteur = value * self._sigmaH

	@dt.setter
	def dt(self, value):
	    self._dt = value

	@Thrf.setter
	def Thrf(self, value):
	    self._Thrf = value

	@TR.setter
	def TR(self, value):
	    self._TR = value

	@K.setter
	def K(self, value):
	    self._K = value

	@M.setter
	def M(self, value):
	    self._M = value

	@scale.setter
	def scale(self, value):
	    self._scale = value
