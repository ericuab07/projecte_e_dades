import cfg
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from SearchMetadata import SearchMetadata

files, ids, data = ImageFiles(), ImageID(), ImageData()
files.reload_fs(cfg.get_root())
for f in files.files_added():
    u = ids.generate_uuid(f)
    data.add_image(u, f)
    data.load_metadata(u)

print(len(data), "imatges")
print(SearchMetadata(data).prompt("cat"))