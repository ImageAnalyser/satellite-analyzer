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
