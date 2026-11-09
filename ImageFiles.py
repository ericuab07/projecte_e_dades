# -*- coding: utf-8 -*-
"""
ImageFiles.py : Func1 - llistat d'imatges PNG
Guarda quins arxius PNG hi ha al disc i recorda què ha canviat des de l'última lectura.
estructura: set (conjunt) i llistes
"""

import os
import cfg


class ImageFiles:

    def __init__(self):
        self.root = None        # carpeta arrel de l'última lectura
        self.files = set()      # arxius que hi havia en l'última lectura
        self.added = []         # arxius nous des de l'última lectura
        self.removed = []       # arxius que han desaparegut des de l'última lectura

    def reload_fs(self, path=None):
        # 0. Si no ens diuen carpeta, fem servir l'arrel de la pràctica
        if path is None:
            path = cfg.get_root()
        path = os.path.abspath(path)        # ruta absoluta: no depèn del directori de treball
        self.root = path

        # 1. Busquem tots els PNG dins la carpeta i les seves subcarpetes
        new_files = set()
        for folder, subfolders, names in os.walk(path):
            for name in names:
                if name.lower().endswith(".png"):
                    full_path = os.path.join(folder, name)
                    if not os.path.isfile(full_path):       # descartem enllaços trencats
                        continue
                    relative = os.path.relpath(full_path, path)     # ex: "cyberpunk\a.png"
                    new_files.add(relative.replace("\\", "/"))      # ex: "cyberpunk/a.png"

        # 2. Comparem amb la lectura anterior
        #    (A - B = els elements que són a A però no a B)
        self.added = sorted(new_files - self.files)
        self.removed = sorted(self.files - new_files)
        self.files = new_files

    def files_added(self):
        return list(self.added)         # còpia, perquè qui ho cridi no pugui modificar l'estat

    def files_removed(self):
        return list(self.removed)       # còpia, igual que a dalt

    def __len__(self):
        return len(self.files)

    def __str__(self):
        return "ImageFiles: " + str(len(self.files)) + " arxius PNG"
