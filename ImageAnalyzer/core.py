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


class ImageAnalyzer:
    output_dir = 'ParaguayOut/'

    def __init__(self, images,
                 output_dir=output_dir,
                 facteur=1000.0,
                 centred=0,
                 bande=0,
                 verbosity=2
                 ):
        self.output_dir = output_dir
        if not os.path.isdir(output_dir):
            print('creating output directory...')
            os.mkdir(output_dir)
        self.images = images
        self.facteur = facteur
        self.centred = centred
        self.bande = bande
        pyhrf.verbose.set_verbosity(verbosity)
   
