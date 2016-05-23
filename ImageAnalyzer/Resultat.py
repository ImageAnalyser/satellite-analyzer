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

from Analyseur import Analyseur
from scenario import scenario
from Data import Data


class Resultat:
    """
    Affichage des Résultats
    :param hrf: liste des figures HRF
    :type hrf: []
    :param Nrl: liste des figures NRL
    :type Nrl: []
    """
    
    def __init__(self, data, scen, analy):
        self.scen = scen
        self.data = data
        self.analy = analy 
        self.bande = self.data.bande 
        self.beta = self.scen.beta 
        self.sigmaH = self.scen.sigmaH 
        self.Thrf = self.scen.Thrf
        #self.pl = self.scen.pl  
        self.dt = self.scen.dt 
           
    def gaussian(self, x, mu, sig):
        return 1. / (sqrt(2. * pi) * sig) * exp(-power((x - mu) / sig, 2.) / 2)
        
    def ConditionalNRLHist(self, nrls, labels):
        """
         Analyze method
        :param nrls: 
        :type nrls: 
        :param labels:
        :type labels:
        :rtype: Resultlist of figures 
        """
        figures = []
        for m in range(0, self.scen.M):
            q = labels[m, 1, :]
            ind = find(q >= 0.5)
            ind2 = find(q < 0.5)
            r = nrls[ind]
            xmin, xmax = min(nrls), max(nrls)
            lnspc = linspace(xmin, xmax, 100)
            m, s = stats.norm.fit(r)
            pdf_g = stats.norm.pdf(lnspc, m, s)
            r = nrls[ind2]
            # xmin, xmax = min(r), max(r)
            lnspc2 = linspace(xmin, xmax, 100)  # len(r)
            m, s = stats.norm.fit(r)
            pdf_g2 = stats.norm.pdf(lnspc2, m, s)
            fg = figure()
            plot(lnspc, pdf_g / len(pdf_g), label="Norm")
            hold(True)
            plot(lnspc2, pdf_g2 / len(pdf_g2), 'k', label="Norm")
            legend(['Posterior: Activated', 'Posterior: Non Activated'])
            # xmin, xmax = min(xt), max(xt)
            # ind2 = find(q <= 0.5)
            figures.append(fg)
        if self.shower:
            show()
        return figures
        
    def set_flags(self, pl=1, save=0, savepl=1, shower=0, nf=1):
        """
            initialization parameters for saving results		
                :param pl: low frequency component 
        :type pl: int
        :param save: variable to indicate the state of outputs
        :type save: int 
        :param savepl: pl are saved in the directory OUTDIR
        :type savepl: int
        :param shower: show or not images results
        :type shower: int   
        :param nf: int
        :type nf: int
        """
        # pl =0 sans PL ,pl =1 avec PL
        self.pl = pl
        # save = 1  les outputs sont sauvgardés
        self.save = save
        # savepl les PL sont sauvgardés dans le repertoir outDir
        self.savepl = savepl
        self.shower = shower
        self.nf = nf
     
    def gen_hrf(self):
        m_A, q_Z, mu_k, m_H, sigma_k, width, height, hrf0 = self.analy.Vbjde() 
        fgs = self.ConditionalNRLHist(m_A, q_Z)
        MMin = -1.0  # Y.min()
        MMax = 1.0  # Y.max()
        pas = (MMax - MMin) / 100
        xx = arange(MMin, MMax, pas)
        nf = 1
        g0 = self.gaussian(xx, mu_k[0][0], sigma_k[0][0])
        g1 = self.gaussian(xx, mu_k[0][1], sigma_k[0][1])
        print (g0, g1)
        fgs.insert(0, figure((self.nf + 1) * 123))
        title("Fonction de reponse", fontsize='xx-large')
        figtext(0.2, 0.04,
                'bande = ' + str(self.bande)+
                ' beta =' + str(self.beta) +
                ' sigma = ' + str(self.sigmaH) +
                ' pl = ' + str(self.pl) +
                ' dt = ' + str(self.dt) +
                ' thrf = ' + str(self.Thrf),
                #'mu_k = '+ str(self.mu_k) +
                #'sigma_k = '+ str(self.sigma_k),
               fontsize='x-large')
        plot(m_H)
        if self.shower == 1:
            show()
        return fgs

    def gen_nrl(self):
        """
        generation of nrl figures

        :param hh:
        :type hh:
        :param z1:
        :type z1:
        :param z2:
        :type z2:
        :param fg:
        :type fg:
        :param fig:
        :type fig:
        """
        m_A, q_Z, mu_k, m_H, sigma_k, width, height, hrf0 = self.analy.Vbjde() 
        fgs = self.ConditionalNRLHist(m_A, q_Z)
        print fgs
        figures = []
        nf = 1
        for m in range(0, self.scen.M):
            hh = m_H
            z1 = m_A[:, m]
            #self.Y = self.data.lecture_data()
            #self.width = self.data.getwidth()
            #self.height = self.data.getheight()
            z2 = reshape(z1, (height, width))
            fg = figure((self.nf + 1) * 110)
            fig, ax = subplots()
            # figure Nrl ########,cmap=get_cmap('gray')
            data = ax.matshow(z2, cmap=get_cmap('gray'))
            fig.colorbar(data)
            title("Niveau de reponse", fontsize='xx-large')
            figtext(0.2, 0.04,
                    'bande = ' + str(self.bande) +
                    ' beta =' + str(self.beta) +
                    ' sigma = ' + str(self.sigmaH) +
                    ' pl = ' + str(self.pl) +
                    ' dt = ' + str(self.dt) +
                    ' thrf = ' + str(self.Thrf),
                    fontsize='x-large')
            figures.append(fig)
            #title("Niveau activation = " + str(m))
            if self.save == 1:
                savefig(self.output_dir + 'nrl bande =' + str(self.bande) + 'beta=' + str(self.beta) + 'sigma= ' +
                        str(self.sigmaH) + 'pl=' + str(self.pl) + 'dt=' + str(self.dt) + 'thrf' + str(self.Thrf) + '.png')
            q = q_Z[m, 1, :]
            q2 = reshape(q, (height, width))
            # q2 = seuillage(q2,0.5)
            fig, ax = subplots()
            data = ax.matshow(q2, cmap=get_cmap('gray'))
            fig.colorbar(data)
            title("Label d'activation", fontsize='xx-large')
            figtext(0.2, 0.04,
                    'bande = ' + str(self.bande) +
                    ' beta =' + str(self.beta) +
                    ' sigma = ' + str(self.sigmaH) +
                    ' pl = ' + str(self.pl) +
                    ' dt = ' + str(self.dt) +
                    ' thrf = ' + str(self.Thrf),
                    fontsize='x-large')
            figures.append(fig)
        return figures
