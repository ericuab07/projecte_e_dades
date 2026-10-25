# -*- coding: utf-8 -*-
"""
Gallery.py : Func5 i Func7 - galeries d'imatges
Una galeria és una llista ordenada d'UUID.
"""

import os
import json
import cfg


class Gallery:

    def __init__(self, image_id, image_viewer):
        self.image_id = image_id
        self.viewer = image_viewer
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        self.images = []            # llista d'UUID, en ordre

    def clean_path(self, path):
        # Funció auxiliar: treu del davant d'un path el que no identifica l'arxiu
        # ex: "generated_images/a.png" -> "a.png"   i   "../a.png" -> "a.png"
        root_name = os.path.basename(os.path.normpath(cfg.ROOT_DIR))        # ex: "generated_images"
        root_full = cfg.get_root().replace("\\", "/") + "/"                 # ex: "/tmp/x/generated_images/"
        path = path.replace("\\", "/")

        changed = True
        while changed:
            changed = False
            for prefix in ("./", "../", root_name + "/", root_full):
                if path.startswith(prefix):
                    path = path[len(prefix):]
                    changed = True
        return path

    def find_uuid(self, path):
        # Funció auxiliar: busca el UUID d'un path del JSON
        # ImageID.get_uuid() només el troba si el path és idèntic al que es va registrar,
        # i el JSON porta "generated_images/a.png" mentre que la col·lecció pot tenir "a.png".
        root_name = os.path.basename(os.path.normpath(cfg.ROOT_DIR))
        parts = path.replace("\\", "/").split("/")

        # 1. Provem les formes habituals del path
        candidates = []
        try:
            candidates.append(cfg.get_canonical_pathfile(path))
        except Exception:
            pass
        for i in range(len(parts)):
            suffix = "/".join(parts[i:])                    # ex: "generated_images/a.png", després "a.png"
            candidates.append(suffix)
            candidates.append("../" + suffix)               # ex: "../a.png"
            candidates.append(root_name + "/" + suffix)     # ex: "generated_images/a.png"
            candidates.append(os.path.join(cfg.get_root(), suffix).replace("\\", "/"))     # path complet

        tried = set()
        for candidate in candidates:
            if candidate in tried:
                continue
            tried.add(candidate)
            try:
                uuid = self.image_id.get_uuid(candidate)
            except Exception:
                uuid = None
            if uuid is not None:
                return uuid

        # 2. Si no, mirem tots els arxius que ImageID coneix i comparem els paths nets
        #    (un ha de ser el final de l'altre: "city.png" = "sub/city.png", però "sub1/city.png" != "sub2/city.png")
        wanted = self.clean_path(path)
        registered = getattr(self.image_id, "uuid_by_file", {})
        for file, uuid in registered.items():
            other = self.clean_path(file)
            if other == wanted or other.endswith("/" + wanted) or wanted.endswith("/" + other):
                return uuid
        return None

    def load_file(self, file):
        # Llegim el fitxer JSON. Retorna quantes imatges s'han carregat (o None si no es pot llegir)
        try:
            f = open(file, "r", encoding="utf-8")
            data = json.load(f)
            f.close()
        except Exception as error:
            print("ERROR: no es pot llegir la galeria", file, ":", error)
            return None

        if not isinstance(data, dict):
            print("ERROR: no es pot llegir la galeria", file, ": el JSON no és una galeria")
            return None

        self.gallery_name = str(data.get("gallery_name", ""))
        self.description = str(data.get("description", ""))
        self.created_date = str(data.get("created_date", ""))
        self.images = []

        paths = data.get("images", [])
        if not isinstance(paths, list):
            paths = []

        # Per cada path del JSON busquem el seu UUID
        for path in paths:
            uuid = None
            if isinstance(path, str):
                uuid = self.find_uuid(path)

            if uuid is None:
                print("AVIS: la imatge", path, "no existeix. S'ignora.")
            else:
                self.images.append(uuid)
        return len(self.images)

    def show(self, mode=None):
        if mode is None:
            mode = cfg.DISPLAY_MODE
        print("Galeria:", self.gallery_name, "-", len(self.images), "imatges")
        for uuid in self.images:
            self.viewer.show_image(uuid, mode)

    def add_image_at_end(self, uuid):
        self.images.append(uuid)

    def remove_first_image(self):
        # Treu la primera imatge (si n'hi ha). No retorna res
        if len(self.images) > 0:
            self.images.pop(0)

    def remove_last_image(self):
        # Treu l'última imatge (si n'hi ha). No retorna res
        if len(self.images) > 0:
            self.images.pop()

    def get_uuids(self):
        return list(self.images)

    def __len__(self):
        return len(self.images)

    def __str__(self):
        return "Gallery [" + self.gallery_name + "]: " + str(len(self.images)) + " imatges"