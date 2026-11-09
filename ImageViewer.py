# -*- coding: utf-8 -*-
"""
ImageViewer.py : Func4 - visualitzar imatges
mode 0: només metadades | mode 1: metadades + imatge | mode 2: només imatge
estructura: cap (consulta ImageData)
"""

import os
import cfg
from PIL import Image


class ImageViewer:

    def __init__(self, image_data):
        self.data = image_data

    def print_image(self, uuid):
        # Imprimeix les metadades que ja són a memòria
        if self.data.get_filename(uuid) is None:
            print("ERROR: la imatge", uuid, "no existeix.")
            return

        width, height = self.data.get_dimensions(uuid)
        print("Visualitzant [" + self.data.get_filename(uuid) + "]")
        print(" Dimensions:", str(width) + "x" + str(height), "pixels")
        print(" Prompt:    ", self.data.get_prompt(uuid)[:100])      # màxim 100 lletres
        print(" Model:     ", self.data.get_model(uuid))
        print(" Seed:      ", self.data.get_seed(uuid))
        print(" CFG Scale: ", self.data.get_cfg_scale(uuid))
        print(" Steps:     ", self.data.get_steps(uuid))
        print(" Sampler:   ", self.data.get_sampler(uuid))
        print(" Generated: ", self.data.get_generated(uuid))
        print(" Created:   ", self.data.get_created_date(uuid))
        print(" UUID:      ", uuid)

    def show_file(self, file):
        # Obre la imatge amb el visualitzador del sistema
        path = os.path.join(cfg.get_root(), file)
        try:
            img = Image.open(path)
            img.show()
        except Exception as error:
            print("ERROR: no es pot mostrar la imatge", file, ":", error)

    def show_image(self, uuid, mode=None):
        if mode is None:
            mode = cfg.DISPLAY_MODE

        if mode < 2:                        # modes 0 i 1: imprimim metadades
            self.print_image(uuid)
        if mode > 0:                        # modes 1 i 2: mostrem la imatge
            file = self.data.get_filename(uuid)
            if file is not None:
                self.show_file(file)

    def __str__(self):
        return "ImageViewer: mode " + str(cfg.DISPLAY_MODE)
