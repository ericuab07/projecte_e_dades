import os
import uuid
from PIL import Image

ROOT_DIR = r"generated_images"
IMAGE_DEFAULT = "42be33f4-a5c4-488a-80c1-5d10c713e0dc.png"
DISPLAY_MODE = 0

def get_root() -> str:
    return os.path.realpath(ROOT_DIR)

def get_uuid(filename: str = "") -> str:
    return uuid.uuid5(uuid.NAMESPACE_URL, filename)

def get_canonical_pathfile(filename: str) -> str:
    file = os.path.normpath(filename)
    file = os.path.relpath(file, ROOT_DIR)
    return file.replace(os.sep, '/')

def read_png_metadata(path):
    with Image.open(path) as img:
        return dict(getattr(img, "text", {}) or {})