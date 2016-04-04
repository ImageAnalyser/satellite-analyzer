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
        
        self.imageList = self.builder.get_object("listbox1")
        self.imageScrolled = self.builder.get_object('scrolledwindow2')
        self.imageList.connect('row-activated', lambda w, row: self.show_image(row.data))
        
    def run(self):
        """connect signals and run Gtk window"""
        self.builder.connect_signals(EventHandler(self))
        self.win.show_all()
        Gtk.main()

            # ajouter image dans View
    def show_image(self, name):
        """Show image on image view

        :param name: image file path
        :type name: str
        """
        # size = self.imageView.get_allocation()
        # pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(name, size.width, size.height)
        # self.imageView.set_from_pixbuf(pixbuf)
        old_viewport = self.imageScrolled.get_child()
        if old_viewport:
            old_viewport.destroy()
        old_viewport = self.imageBox.get_child()
        if old_viewport:
            old_viewport.destroy()
        with TiffFile(name) as img:
            fig = imshow(img.asarray())[0]
            canvas = FigureCanvas(fig)
            self.imageScrolled.add_with_viewport(canvas)
            toolbar = NavigationToolbar(canvas, self.win)
            self.imageBox.add_with_viewport(toolbar)
            pyplot.close(fig)

            self.shape = img.asarray().shape
            self.xmax.set_range(self.xmin.get_value_as_int() + 1, self.shape[0])
            self.ymax.set_range(self.ymin.get_value_as_int() + 1, self.shape[1])

        self.imageScrolled.show_all()
if __name__ == '__main__':
    app = App()
    app.run()
