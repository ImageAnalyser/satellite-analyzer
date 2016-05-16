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


class Analyseur:
    """
    Analyser les scénarios d'analyse avec les data en entrées
    :param width: largeur en sortie
    :type width: int
    :param height: hauteur en sortie
    :int height: int
    """
    def __init__(self, data, scen):
        self.scen = scen
        self.data = data
        self.width = float
        self.height = float
        
        #d = Data()
        #scen = scenario()
        #Y = d.lecture_data(d._xmin, d._xmax, d._ymin, d._ymax, d._bande, d._facteur)
        STD = std(data.Y, 1)
        MM = mean(data.Y, 1)
        TT, self.NN = data.Y.shape
        self.centred = 1
        if self.centred:
            for t in xrange(0, TT):
                data.Y[t, :] = (data.Y[t, :] - MM[t]) / STD[t]
                #self.Y1 = data.Y[t, :]
        self.width = data.getwidth()
        self.height = data.getheight()
        #scen.init_params(scen.beta, scen.sigmaH, scen.v_h_facteur, scen.dt, scen.Thrf, scen.TR, scen.K, scen.M, scen.scale)

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

    def gen_hrf(self,
                estimateSigmaH=0,
                Onsets={'nuages': array([0])},
                nItmax=30,
                nItmin=30,
                estimateBeta=0,
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
        areas = ['ra']
        labelFields = {}
        cNames = ['inactiv', 'activ']
        spConf = RegularLatticeMapping((self.height, self.width, 1))
        graph = graph_from_lattice(
            ones((self.height, self.width, 1), dtype=int))
        J = self.data.Y.shape[0]
        l = int(sqrt(J))
        FlagZ = 1
        q_Z0 = zeros((self.scen.M, self.scen.K, J), dtype=float64)
        if not FlagZ:
            q_Z0 = q_Z
        FlagH = 1
        TT, m_h = getCanoHRF(self.scen.Thrf - self.scen.dt, self.scen.dt)
        hrf0 = array(m_h).astype(float64)
        Sigma_H0 = eye(hrf0.shape[0])
        if not FlagH:
            hrf0 = h_H
            Sigma_H0 = Sigma_H

        self.m_A, self.m_H, self.q_Z, sigma_epsilone, mu_k, sigma_k, Beta, PL, Sigma_A, XX, Sigma_H = \
            Main_vbjde_Extension_TD(
                FlagH, hrf0, Sigma_H0, self.height, self.width, q_Z0, FlagZ,
                self.pl, graph, self.data.Y, Onsets, self.scen.Thrf, self.scen.K, self.scen.TR,
                self.scen.beta, self.scen.dt, self.scen.scale, estimateSigmaH, self.scen.sigmaH,
                nItmin, estimateBeta)

        fgs = self.ConditionalNRLHist(self.m_A, self.q_Z)

        MMin = -1.0  # Y.min()
        MMax = 1.0  # Y.max()
        pas = (MMax - MMin) / 100
        xx = arange(MMin, MMax, pas)
        g0 = self.gaussian(xx, mu_k[0][0], sigma_k[0][0])
        g1 = self.gaussian(xx, mu_k[0][1], sigma_k[0][1])
        fgs.insert(0, figure((self.nf + 1) * 123))
        title("Fonction de reponse", fontsize='xx-large')
        figtext(0.2, 0.04,
                'bande = ' + str(self.data.bande) +
                ' beta =' + str(self.scen.beta) +
                ' sigma = ' + str(self.scen.sigmaH) +
                ' pl = ' + str(self.pl) +
                ' dt = ' + str(self.scen.dt) +
                ' thrf = ' + str(self.scen.Thrf),
                fontsize='x-large')
        plot(self.m_H)
        if self.shower == 1:
            show()
        return fgs
        
    def gaussian(self, x, mu, sig):
        r = 1. / (sqrt(2. * pi) * sig) * exp(-power((x - mu) / sig, 2.) / 2)
        print(x, mu, sig, r)
        return r
        
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
        figures = []
        for m in range(0, self.scen.M):
            hh = self.m_H
            z1 = self.m_A[:, m]
            z2 = reshape(z1, (self.height, self.width))
            fg = figure((self.nf + 1) * 110)
            fig, ax = subplots()
            # figure Nrl ########,cmap=get_cmap('gray')
            data = ax.matshow(z2, cmap=get_cmap('gray'))
            fig.colorbar(data)
            title("Niveau de reponse", fontsize='xx-large')
            figtext(0.2, 0.04,
                    'bande = ' + str(self.data.bande) +
                    ' beta =' + str(self.scen.beta) +
                    ' sigma = ' + str(self.scen.sigmaH) +
                    ' pl = ' + str(self.pl) +
                    ' dt = ' + str(self.scen.dt) +
                    ' thrf = ' + str(self.scen.Thrf),
                    fontsize='x-large')
            figures.append(fig)
            # title("Est: m = " + str(m))
            if self.save == 1:
                savefig(self.output_dir + 'nrl bande =' + str(self.scen.bande) + 'beta=' + str(self.scen.beta) + 'sigma= ' +
                        str(self.scen.sigmaH) + 'pl=' + str(self.scen.pl) + 'dt=' + str(self.scen.dt) + 'thrf' + str(self.scen.Thrf) + '.png')
            q = self.q_Z[m, 1, :]
            q2 = reshape(q, (self.height, self.width))
            # q2 = seuillage(q2,0.5)
            fig, ax = subplots()
            data = ax.matshow(q2, cmap=get_cmap('gray'))
            fig.colorbar(data)
            title("Label d'activation", fontsize='xx-large')
            figtext(0.2, 0.04,
                    'bande = ' + str(self.data.bande) +
                    ' beta =' + str(self.scen.beta) +
                    ' sigma = ' + str(self.scen.sigmaH) +
                    ' pl = ' + str(self.pl) +
                    ' dt = ' + str(self.scen.dt) +
                    ' thrf = ' + str(self.scen.Thrf),
                    fontsize='x-large')
            figures.append(fig)
        return figures
