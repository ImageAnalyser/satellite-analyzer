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


class Data:
    """
	initialisation des paramètres de lecture data
    :param image: liste de data 
    :type image: []
    :param bande: paramétre de configuration
    :type bande: int 
    :param facteur: paramètre de configuration facteur
    :type facteur: int
    :param xmin: valeur minimale largeur
    :type xmin: int  
    :param xmax: valeur maximale largeur
    :type xmax: int
    :param ymin: valeur minimale hauteur
    :type ymin: int
    :param ymax: valeur maximale hauteur
    :type ymax: int
    """

    def __init__(self,
                 images=[],
                 bande=0,
                 facteur=1000):
        self.images = images
        self._bande = bande
        self._facteur = facteur

    @property
    def xmin(self):
        return self._xmin

    @property
    def xmax(self):
        return self._xmax

    @property
    def ymin(self):
        return self._ymin

    @property
    def ymax(self):
        return self._ymax

    @property
    def facteur(self):
        return self._facteur

    @property
    def bande(self):
        return self._bande

    @xmin.setter
    def xmin(self, value):
        self._xmin = float(value)

    @xmax.setter
    def xmax(self, value):
        self._xmin = float(value)

    @ymin.setter
    def ymin(self, value):
        self._ymin = float(value)

    @ymax.setter
    def ymax(self, value):
        self._ymax = value

    @facteur.setter
    def facteur(self, value):
        self._facteur = value

    @bande.setter
    def bande(self, value):
        self._bande = value
        
    def getwidth (self):
        self.width = self.ymax - self.ymin
        return self.width
    
    def getheight(self):
	    self.height = self.xmax - self.xmin
	    return self.height	
        
    def lecture_data(self):
        """méthode qui assure la lecture de image"""
        start = 0
        end = -1
        #Y = []
        images = self.images[start:end]
        signal = []
        for image in self.images:
            print(image)
            labels = imread(image)
            labels = labels[self.xmin:self.xmax, self.ymin:self.ymax, self.bande].astype(float)
            if (self.facteur > 1):
                labels = labels / self.facteur
            signal.append(labels.flatten())
        self.Y = asarray(signal)
        #self.Y1 = self.Post_lecture(self.Y)
        return self.Y
        
        
