# -*- coding: utf-8 -*-
from gi.repository import Gtk, Gdk, GdkPixbuf
from .core import ImageAnalyzer


class EventHandler():
    """Signal Event handlers definition"""

    def __init__(self, app):
        self.app = app
   
    def on_quit_clicked(self, *args):
        """clean and close the app"""
        Gtk.main_quit(*args)

    def on_clear_clicked(self, *args):
        """clear images list and image view
        recuperation of default value from graphical object
        """
        while self.app.imageList.get_row_at_index(0):
            self.app.imageList.get_row_at_index(0).destroy()
        while self.app.resultList.get_row_at_index(0):
            self.app.resultList.get_row_at_index(0).destroy()
        old_viewport = self.app.imageScrolled.get_child()
        if old_viewport:
            old_viewport.destroy()
        old_viewport = self.app.resultScrolled.get_child()
        if old_viewport:
            old_viewport.destroy()
        self.app.xmin.set_value(2658)
        self.app.xmax.set_value(2730)
        self.app.ymin.set_value(2600)
        self.app.ymax.set_value(2680)
        self.app.beta.set_value(0.1)
        self.app.sigmah.set_value(0.01)
        self.app.vh.set_value(0.1)
        self.app.dt.set_value(1)
        self.app.thrf.set_value(4)
        self.app.tr.set_value(1)
        

