#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Gtk Interface for Image Analyzer using glade template"""

import os
from matplotlib import pyplot
from tifffile import imread, imshow, TiffFile
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

from .core import ImageAnalyzer
from .eventHandler import EventHandler

# imageList.set_sort_func(lambda r1, r2, data, notify_destroy: return -1, None, False)
# imageList.set_filter_func(lambda r, r2, data, notify_destroy: return True, None, False)


class App:
    """main logic for the graphical interface

    Usage::

        app = App()
        app.run()
    """

    def __init__(self):
        """recuperation of graphical object"""
        self.builder = Gtk.Builder()

        glade_file = os.path.join(os.path.dirname(__file__), 'app.glade')
        self.builder.add_from_file(glade_file)

        self.win = self.builder.get_object('window1')
        self.win.about = self.builder.get_object('aboutdialog1')

    

if __name__ == '__main__':
    app = App()
    app.run()
