# -*- coding: utf-8 -*-
from gi.repository import Gtk, Gdk, GdkPixbuf
#import Data
from Data import Data
from EventData import EventData
from EventScenario import EventScenario
from EventResultat import EventResultat
from Data import*
from EventAnalyseur import EventAnalyseur
from scenario import scenario
from scenario import*
from Resultat import Resultat
from Analyseur import Analyseur
from Analyseur import*


class EventHandler():
    """Signal Event handlers definition"""
    fgs = []
    fgs1 = []

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
        self.app.xmin.set_value(2660)
        self.app.xmax.set_value(2730)
        self.app.ymin.set_value(2600)
        self.app.ymax.set_value(2680)
        self.app.beta.set_value(0.1)
        self.app.sigmah.set_value(0.01)
        self.app.vh.set_value(0.001)
        self.app.dt.set_value(1)
        self.app.thrf.set_value(4)
        self.app.tr.set_value(1)
        self.app.k.set_value(2)
        self.app.m.set_value(1)
        self.app.nitmin.set_value(30)
        self.app.nitmax.set_value(30)
        self.app.scale.set_value(1)
        self.app.facteur.set_text(str(1000))
        self.app.pl.set_active(True)
        self.app.notebook.set_current_page(0)

    def on_add_clicked(self, *args):
        """Launch multi-select image file chooser dialog and append new files
        to the image list and show last selected file"""
        chooser = Gtk.FileChooserDialog("Choose an image", self.app.win,
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        chooser.set_select_multiple(True)

        image_filter = Gtk.FileFilter()
        image_filter.set_name("Image files")
        image_filter.add_pattern("*.tiff")
        image_filter.add_pattern("*.TIIF")
        image_filter.add_pattern("*.TIF")
        image_filter.add_pattern("*.tif")
        # any_filter = Gtk.FileFilter()
        # any_filter.set_name("Any files")
        # any_filter.add_pattern("*")

        chooser.add_filter(image_filter)
        # chooser.add_filter(any_filter)
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            self.app.add_images(chooser.get_filenames())
        chooser.destroy()

    def on_about_clicked(self, *args):
        """show about dialog"""
        self.app.win.about.show_all()
        # .run
        # .destroy

    def on_about_closed(self, *args):
        """close about dialog"""
        self.app.win.about.hide()

    def on_search_changed(self, *args):
        self.app.imageList.invalidate_filter()

    def on_exec_clicked(self, *args):
        """analyser les images importées
        """
        while self.app.resultList.get_row_at_index(0):
            self.app.resultList.get_row_at_index(0).destroy()
        old_viewport = self.app.resultScrolled.get_child()
        if old_viewport:
            old_viewport.destroy()

        imgs = []
        f1 = []
        f2 = []
        i = 0

        while self.app.imageList.get_row_at_index(i):
            imgs.append(self.app.imageList.get_row_at_index(i).data)
            i += 1
        EvenD = EventData(self.app, imgs)
        data = EvenD.on_exec_clicked_data()
        
        EvenS = EventScenario(self.app)
        Scen = EvenS.on_exec_scenario()
        
        pre = Pre_Traitement(data, Scen)
        analy = Analyseur(pre, Scen, data)
        
        EvenA = EventAnalyseur(self.app, analy)
        Analys = EvenA.on_exec_clicked_analyse()
        
        Res = Resultat(data, Scen, analy)
        
        EvenR = EventResultat(self.app, Res, analy, data, Scen, pre)
        EvenR.on_exec_result()
          
    def on_item_delete(self, widget, ev, *args):
        if ev.keyval == Gdk.KEY_Delete:
            r = self.app.imageList.get_selected_row()
            if r:
                r.destroy()

    def on_xmin_changed(self, *args):
        print("changed")
        self.app.xmax.set_range(
            self.app.xmin.get_value_as_int() + 1, self.app.shape[0])

    def on_xmax_changed(self, *args):
        print("changed")
        self.app.xmin.set_range(0, self.app.xmax.get_value_as_int() - 1)

    def on_ymin_changed(self, *args):
        print("changed")
        self.app.ymax.set_range(
            self.app.ymin.get_value_as_int() + 1, self.app.shape[1])

    def on_ymax_changed(self, *args):
        print("changed")
        self.app.ymin.set_range(0, self.app.ymax.get_value_as_int() - 1)

    def on_facteur_ok(self, *args):
        self.app.facteur.set_text(
            str(self.app.spinbutton_facteur.get_value_as_int()))
        self.app.window_facteur.hide()

    def on_details_clicked(self, *args):
        self.app.window_details.show_all()
