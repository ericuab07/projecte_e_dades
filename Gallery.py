# -*- coding: utf-8 -*-
"""
Gallery.py : Func5 i Func7 - galeries d'imatges
Una galeria és una llista ordenada d'UUID.
"""

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

    def find_uuid(self, path):
        # Funció auxiliar: busca el UUID d'un path del JSON
        # El JSON porta el path des de fora de l'arrel ("generated_images/a.png"),
        # però la col·lecció guarda els paths relatius a l'arrel ("a.png").
        candidates = []

        # 1. El path canònic de cfg (relatiu a ROOT_DIR i amb "/")
        try:
            candidates.append(cfg.get_canonical_pathfile(path))
        except Exception:
            pass

        # 2. El path tal com és i, després, traient-li carpetes del davant
        parts = path.replace("\\", "/").split("/")
        for i in range(len(parts)):
            candidates.append("/".join(parts[i:]))      # ex: "generated_images/a.png", després "a.png"

        for candidate in candidates:
            uuid = self.image_id.get_uuid(candidate)
            if uuid is not None:
                return uuid
        return None

    def load_file(self, file):
        # Llegim el fitxer JSON. No retorna res
        try:
            f = open(file, "r", encoding="utf-8")
            data = json.load(f)
            f.close()
        except Exception as error:
            print("ERROR: no es pot llegir la galeria", file, ":", error)
            return

        self.gallery_name = data.get("gallery_name", "")
        self.description = data.get("description", "")
        self.created_date = data.get("created_date", "")
        self.images = []

        # Per cada path del JSON busquem el seu UUID
        for path in data.get("images", []):
            uuid = self.find_uuid(path)

            if uuid is None:
                print("AVIS: la imatge", path, "no existeix. S'ignora.")
            else:
                self.images.append(uuid)

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