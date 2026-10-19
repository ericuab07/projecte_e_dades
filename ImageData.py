# -*- coding: utf-8 -*-
"""
ImageData.py : Func3 - metadades de les imatges
Per cada UUID guardem un diccionari amb el path, les dimensions i les metadades.
Tot són Strings i "None" vol dir "camp buit".
"""

import os
import cfg
from PIL import Image


class ImageData:

    def __init__(self):
        self.images = {}        # uuid -> diccionari amb les dades de la imatge

    def add_image(self, uuid, file):
        # Només guardem el path. Les metadades queden buides ("None")
        self.images[uuid] = {
            "file": file, "width": -1, "height": -1,
            "prompt": "None", "seed": "None", "cfg_scale": "None", "steps": "None",
            "sampler": "None", "model": "None", "generated": "None", "created_date": "None",
        }

    def remove_image(self, uuid):
        if uuid in self.images:
            del self.images[uuid]

    def load_metadata(self, uuid):
        if uuid not in self.images:
            print("ERROR: la imatge", uuid, "no existeix.")
            return False

        image = self.images[uuid]
        path = os.path.join(cfg.get_root(), image["file"])      # path complet al disc

        try:
            metadata = cfg.read_png_metadata(path)
            if not metadata:
                metadata = {}
            img = Image.open(path)
            width, height = img.size
            img.close()
        except Exception as error:
            print("ERROR: no es pot llegir", path, ":", error)
            return False

        # Si un camp no hi és, posem "None"
        image["prompt"] = str(metadata.get("Prompt", "None"))
        image["seed"] = str(metadata.get("Seed", "None"))
        image["cfg_scale"] = str(metadata.get("CFG_Scale", "None"))
        image["steps"] = str(metadata.get("Steps", "None"))
        image["sampler"] = str(metadata.get("Sampler", "None"))
        image["model"] = str(metadata.get("Model", "None"))
        image["generated"] = str(metadata.get("Generated", "None"))
        image["created_date"] = str(metadata.get("Created_Date", "None"))
        image["width"] = width
        image["height"] = height
        return True

    # ---- Funcions per consultar ----

    def get_filename(self, uuid):
        if uuid not in self.images:
            return None
        return self.images[uuid]["file"]

    def get_dimensions(self, uuid):
        if uuid not in self.images:
            return (-1, -1)
        return (self.images[uuid]["width"], self.images[uuid]["height"])

    def get_prompt(self, uuid):
        return self.get_field(uuid, "prompt")

    def get_model(self, uuid):
        return self.get_field(uuid, "model")

    def get_seed(self, uuid):
        return self.get_field(uuid, "seed")

    def get_cfg_scale(self, uuid):
        return self.get_field(uuid, "cfg_scale")

    def get_steps(self, uuid):
        return self.get_field(uuid, "steps")

    def get_sampler(self, uuid):
        return self.get_field(uuid, "sampler")

    def get_generated(self, uuid):
        return self.get_field(uuid, "generated")

    def get_created_date(self, uuid):
        return self.get_field(uuid, "created_date")

    def get_field(self, uuid, field):
        # Funció auxiliar: retorna un camp d'una imatge, o "None" si la imatge no existeix
        if uuid not in self.images:
            return "None"
        return self.images[uuid][field]

    def get_uuids(self):
        return list(self.images.keys())

    def __len__(self):
        return len(self.images)

    def __str__(self):
        return "ImageData: " + str(len(self.images)) + " imatges"