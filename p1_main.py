# -*- coding: utf-8 -*-
"""
p1_main.py : Programa de prova de la Fase I
"""

import cfg
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from ImageViewer import ImageViewer
from Gallery import Gallery
from SearchMetadata import SearchMetadata

files = ImageFiles()
ids = ImageID()
data = ImageData()
viewer = ImageViewer(data)
search = SearchMetadata(data)

# Func1, Func2 i Func3: llistar arxius, generar UUID i llegir metadades
files.reload_fs(cfg.get_root())
for file in files.files_added():
    uuid = ids.generate_uuid(file)
    if uuid is not None:
        data.add_image(uuid, file)
        data.load_metadata(uuid)
print(files)
print(ids)
print(data)

# Func4: veure una imatge
viewer.show_image(data.get_uuids()[0], cfg.DISPLAY_MODE)

# Func6: cerques
by_model = search.model("SD")
by_prompt = search.prompt("cat")
print("Model SD:", len(by_model), "| prompt cat:", len(by_prompt))
print("AND:", len(search.and_operator(by_model, by_prompt)))
print("OR:", len(search.or_operator(by_model, by_prompt)))

# Func7: galeria a partir d'una cerca
gallery = Gallery(ids, viewer)
gallery.gallery_name = "Cerca: model SD"
for uuid in by_model:
    gallery.add_image_at_end(uuid)
gallery.remove_first_image()
gallery.remove_last_image()
print(gallery)
gallery.show(0)