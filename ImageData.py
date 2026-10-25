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

    # Noms amb què pot venir cada camp dins del PNG (sempre en minúscules i amb "_")
    FIELDS = {
        "prompt": ["prompt"],
        "seed": ["seed"],
        "cfg_scale": ["cfg_scale", "cfg", "cfgscale", "guidance_scale"],
        "steps": ["steps", "num_inference_steps"],
        "sampler": ["sampler", "sampler_name"],
        "model": ["model", "model_name"],
        "generated": ["generated"],
        "created_date": ["created_date", "created", "date"],
    }

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

    def find_path(self, file):
        # Funció auxiliar: busca l'arxiu al disc i en retorna el path complet
        root = cfg.get_root()

        # Treiem els "../" i la carpeta arrel del davant (ex: "../generated_images/a.png" -> "a.png")
        clean = file.replace("\\", "/")
        root_name = os.path.basename(os.path.normpath(cfg.ROOT_DIR))
        changed = True
        while changed:
            changed = False
            for prefix in ("./", "../", root_name + "/"):
                if clean.startswith(prefix):
                    clean = clean[len(prefix):]
                    changed = True

        candidates = [
            os.path.join(root, file),                       # ex: root + "cyberpunk/a.png"
            os.path.normpath(os.path.join(root, file)),     # el mateix, sense els "../"
            file,                                           # el path tal com ens l'han donat
            os.path.join(root, clean),                      # ex: root + "a.png"
            os.path.join(root, os.path.basename(file)),     # només el nom de l'arxiu
        ]
        for candidate in candidates:
            if os.path.isfile(candidate):
                return candidate
        return candidates[0]        # si no hi és enlloc, retornem el primer perquè l'error el mostri

    def read_metadata(self, path):
        # Funció auxiliar: llegeix els camps del PNG i els retorna com a {nom: String}
        raw = None
        reader = getattr(cfg, "read_png_metadata", None)
        if reader is not None:
            raw = reader(path)              # si cfg ja sap llegir-les, la fem servir

        if not raw:
            # Si no, llegim nosaltres els "text chunks" del PNG
            img = Image.open(path)
            raw = {}
            for key, value in img.info.items():
                if isinstance(value, str):
                    raw[key] = value
            for key, value in getattr(img, "text", {}).items():
                raw[key] = value
            img.close()

        # Normalitzem els noms: "CFG Scale", "CFG_Scale" i "cfg_scale" són el mateix camp
        metadata = {}
        for key, value in raw.items():
            name = str(key).strip().lower().replace(" ", "_").replace("-", "_")
            metadata[name] = str(value)
        return metadata

    def load_metadata(self, uuid):
        # No retorna res (si hi ha algun problema, ho diu per pantalla)
        if uuid not in self.images:
            print("ERROR: la imatge", uuid, "no existeix.")
            return

        image = self.images[uuid]
        path = self.find_path(image["file"])        # path complet al disc

        try:
            metadata = self.read_metadata(path)
            img = Image.open(path)
            width, height = img.size
            img.close()
        except Exception as error:
            print("ERROR: no es pot llegir", path, ":", error)
            return

        # Si un camp no hi és (o està buit), posem "None"
        for field, names in self.FIELDS.items():
            image[field] = "None"
            for name in names:
                if metadata.get(name, "") != "":
                    image[field] = metadata[name]
                    break
        image["width"] = width
        image["height"] = height

    # ---- Funcions per consultar ----
    # Si el UUID no existeix, totes retornen None (com get_filename)

    def get_filename(self, uuid):
        if uuid not in self.images:
            return None
        return self.images[uuid]["file"]

    def get_dimensions(self, uuid):
        if uuid not in self.images:
            return None
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
        # Funció auxiliar: retorna un camp d'una imatge, o None si la imatge no existeix
        if uuid not in self.images:
            return None
        return self.images[uuid][field]

    def get_uuids(self):
        return list(self.images.keys())

    def __len__(self):
        return len(self.images)

    def __str__(self):
        return "ImageData: " + str(len(self.images)) + " imatges"