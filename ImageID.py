# -*- coding: utf-8 -*-
"""
ImageID.py : Func2 - generar identificadors (UUID) d'imatges
Cada arxiu té un UUID. Guardem dos diccionaris per poder anar d'un a l'altre.
"""

import cfg


class ImageID:

    def __init__(self):
        self.uuid_by_file = {}      # "cyberpunk/a.png"  ->  "e2960755-..."
        self.file_by_uuid = {}      # "e2960755-..."     ->  "cyberpunk/a.png"

    def generate_uuid(self, file):
        new_uuid = str(cfg.get_uuid(file))

        # Si el UUID ja existeix, no fem servir aquest arxiu
        if new_uuid in self.file_by_uuid:
            print("AVIS: el UUID", new_uuid, "ja existeix. L'arxiu", file, "no s'utilitzara.")
            return None

        self.uuid_by_file[file] = new_uuid
        self.file_by_uuid[new_uuid] = file
        return new_uuid

    def get_uuid(self, file):
        # .get() retorna None si l'arxiu no hi és (en lloc de donar error)
        return self.uuid_by_file.get(file)

    def remove_uuid(self, uuid):
        if uuid in self.file_by_uuid:
            file = self.file_by_uuid[uuid]
            del self.file_by_uuid[uuid]
            del self.uuid_by_file[file]

    def __len__(self):
        return len(self.file_by_uuid)

    def __str__(self):
        return "ImageID: " + str(len(self.file_by_uuid)) + " identificadors"