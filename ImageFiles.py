# -*- coding: utf-8 -*-
"""
ImageFiles.py : Func1 - llistat d'imatges PNG
Guarda quins arxius PNG hi ha al disc i recorda què ha canviat des de l'última lectura.
"""

import os
import cfg


class ImageFiles:

    def __init__(self):
        self.files = set()      # arxius que hi havia en l'última lectura
        self.added = []         # arxius nous des de l'última lectura
        self.removed = []       # arxius que han desaparegut des de l'última lectura

    def reload_fs(self, path=None):
        if path is None:
            path = cfg.get_root()

        # 1. Busquem tots els PNG dins la carpeta i les seves subcarpetes
        new_files = set()
        for folder, subfolders, names in os.walk(path):
            for name in names:
                if name.lower().endswith(".png"):
                    full_path = os.path.join(folder, name)
                    relative = os.path.relpath(full_path, path)     # ex: "cyberpunk\a.png"
                    new_files.add(relative.replace("\\", "/"))      # ex: "cyberpunk/a.png"

        # 2. Comparem amb la lectura anterior
        #    (A - B = els elements que són a A però no a B)
        self.added = sorted(new_files - self.files)
        self.removed = sorted(self.files - new_files)
        self.files = new_files

    def files_added(self):
        return self.added

    def files_removed(self):
        return self.removed

    def __len__(self):
        return len(self.files)

    def __str__(self):
        return "ImageFiles: " + str(len(self.files)) + " arxius PNG"