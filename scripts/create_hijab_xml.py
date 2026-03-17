import os
import shutil
from PIL import Image
import xml.etree.ElementTree as ET

# =========================
# PATHS
# =========================
HIJAB_RAW_DIR = r"dataset/hijab_raw"

HIJAB_XML_IMG_DIR = r"dataset/hijab_xml/images"
HIJAB_XML_ANN_DIR = r"dataset/hijab_xml/annotations"

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".jfif")

CLASS_NAME = "hijab"

# =========================
# HELPERS
# =========================
def ensure_dirs():
    os.makedirs(HIJAB_XML_IMG_DIR, exist_ok=True)
    os.makedirs(HIJAB_XML_ANN_DIR, exist_ok=True)

def clear_output_dirs():
    for folder in [HIJAB_XML_IMG_DIR, HIJAB_XML_ANN_DIR]:
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

def create_pascal_voc_xml(filename, width, height, depth):
    annotation = ET.Element("annotation")

    folder = ET.SubElement(annotation, "folder")
    folder.text = "images"

    fname = ET.SubElement(annotation, "filename")
    fname.text = filename

    path = ET.SubElement(annotation, "path")
    path.text = filename

    source = ET.SubElement(annotation, "source")
    database = ET.SubElement(source, "database")
    database.text = "Unknown"

    size = ET.SubElement(annotation, "size")
    w = ET.SubElement(size, "width")
    w.text = str(width)

    h = ET.SubElement(size, "height")
    h.text = str(height)

    d = ET.SubElement(size, "depth")
    d.text = str(depth)

    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = "0"

    # object
    obj = ET.SubElement(annotation, "object")

    name = ET.SubElement(obj, "name")
    name.text = CLASS_NAME

    pose = ET.SubElement(obj, "pose")
    pose.text = "Unspecified"

    truncated = ET.SubElement(obj, "truncated")
    truncated.text = "0"

    difficult = ET.SubElement(obj, "difficult")
    difficult.text = "0"

    # full-image bounding box
    bndbox = ET.SubElement(obj, "bndbox")

    xmin = ET.SubElement(bndbox, "xmin")
    xmin.text = "1"

    ymin = ET.SubElement(bndbox, "ymin")
    ymin.text = "1"

    xmax = ET.SubElement(bndbox, "xmax")
    xmax.text = str(width)

    ymax = ET.SubElement(bndbox, "ymax")
    ymax.text = str(height)

    return annotation

def prettify_and_save_xml(root, save_path):
    tree = ET.ElementTree(root)
    tree.write(save_path, encoding="utf-8", xml_declaration=True)

# =========================
# MAIN
# =========================
def main():
    ensure_dirs()
    clear_output_dirs()

    image_files = [
        f for f in os.listdir(HIJAB_RAW_DIR)
        if f.lower().endswith(IMAGE_EXTENSIONS)
    ]

    print(f"Found {len(image_files)} hijab images.")

    for img_name in image_files:
        src_img_path = os.path.join(HIJAB_RAW_DIR, img_name)
        dst_img_path = os.path.join(HIJAB_XML_IMG_DIR, img_name)

        # Copy image into hijab_xml/images
        shutil.copy(src_img_path, dst_img_path)

        # Read image size
        with Image.open(src_img_path) as img:
            width, height = img.size
            depth = len(img.getbands())  # usually 3 for RGB

        # Create XML
        xml_root = create_pascal_voc_xml(img_name, width, height, depth)

        base_name = os.path.splitext(img_name)[0]
        xml_save_path = os.path.join(HIJAB_XML_ANN_DIR, base_name + ".xml")
        prettify_and_save_xml(xml_root, xml_save_path)

    print("✅ Hijab images converted to Pascal VOC XML format successfully.")

if __name__ == "__main__":
    main()