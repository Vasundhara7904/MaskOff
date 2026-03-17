import os
import random
import shutil
import xml.etree.ElementTree as ET

# =====================================
# SOURCE DATASETS
# =====================================
XML1_IMAGES = r"dataset/xml_raw/images"
XML1_ANN = r"dataset/xml_raw/annotations"

XML2_IMAGES = r"dataset/hijab_xml/images"
XML2_ANN = r"dataset/hijab_xml/annotations"

# =====================================
# OUTPUT YOLO DATASET
# =====================================
YOLO_IMG_TRAIN = r"yolo_dataset/images/train"
YOLO_IMG_VAL = r"yolo_dataset/images/val"
YOLO_LBL_TRAIN = r"yolo_dataset/labels/train"
YOLO_LBL_VAL = r"yolo_dataset/labels/val"

TRAIN_RATIO = 0.8
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".jfif"]

# =====================================
# CLASS MAP
# =====================================
CLASS_MAP = {
    "with_mask": 0,
    "without_mask": 1,
    "mask_weared_incorrect": 2,
    "hijab": 3
}

# =====================================
# HELPERS
# =====================================
def ensure_dirs():
    for folder in [YOLO_IMG_TRAIN, YOLO_IMG_VAL, YOLO_LBL_TRAIN, YOLO_LBL_VAL]:
        os.makedirs(folder, exist_ok=True)

def clear_output_dirs():
    for folder in [YOLO_IMG_TRAIN, YOLO_IMG_VAL, YOLO_LBL_TRAIN, YOLO_LBL_VAL]:
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

def find_matching_image(base_name, image_dir):
    for ext in IMAGE_EXTENSIONS:
        img_path = os.path.join(image_dir, base_name + ext)
        if os.path.exists(img_path):
            return img_path
    return None

def convert_box_to_yolo(img_w, img_h, xmin, ymin, xmax, ymax):
    x_center = ((xmin + xmax) / 2.0) / img_w
    y_center = ((ymin + ymax) / 2.0) / img_h
    box_width = (xmax - xmin) / img_w
    box_height = (ymax - ymin) / img_h
    return x_center, y_center, box_width, box_height

def parse_xml_annotation(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    img_w = int(size.find("width").text)
    img_h = int(size.find("height").text)

    yolo_labels = []

    for obj in root.findall("object"):
        class_name = obj.find("name").text.strip()

        if class_name not in CLASS_MAP:
            continue

        class_id = CLASS_MAP[class_name]

        bndbox = obj.find("bndbox")
        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)

        # Clamp coordinates
        xmin = max(0, min(xmin, img_w))
        xmax = max(0, min(xmax, img_w))
        ymin = max(0, min(ymin, img_h))
        ymax = max(0, min(ymax, img_h))

        if xmax <= xmin or ymax <= ymin:
            continue

        x_center, y_center, box_width, box_height = convert_box_to_yolo(
            img_w, img_h, xmin, ymin, xmax, ymax
        )

        yolo_labels.append(
            f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"
        )

    return yolo_labels

def collect_dataset(annotation_dir, image_dir, prefix):
    xml_files = [f for f in os.listdir(annotation_dir) if f.lower().endswith(".xml")]
    items = []

    for xml_file in xml_files:
        base_name = os.path.splitext(xml_file)[0]
        xml_path = os.path.join(annotation_dir, xml_file)
        img_path = find_matching_image(base_name, image_dir)

        if img_path is None:
            print(f"Skipping {xml_file}: matching image not found")
            continue

        items.append({
            "xml_path": xml_path,
            "img_path": img_path,
            "base_name": f"{prefix}_{base_name}"
        })

    return items

def write_split(items, split_name):
    img_out_dir = YOLO_IMG_TRAIN if split_name == "train" else YOLO_IMG_VAL
    lbl_out_dir = YOLO_LBL_TRAIN if split_name == "train" else YOLO_LBL_VAL

    written = 0

    for item in items:
        yolo_labels = parse_xml_annotation(item["xml_path"])
        if not yolo_labels:
            continue

        img_ext = os.path.splitext(item["img_path"])[1]
        dst_img_name = item["base_name"] + img_ext
        dst_img_path = os.path.join(img_out_dir, dst_img_name)
        dst_lbl_path = os.path.join(lbl_out_dir, item["base_name"] + ".txt")

        shutil.copy(item["img_path"], dst_img_path)

        with open(dst_lbl_path, "w") as f:
            f.write("\n".join(yolo_labels))

        written += 1

    return written

# =====================================
# MAIN
# =====================================
def main():
    ensure_dirs()
    clear_output_dirs()

    # Collect both XML datasets
    dataset1 = collect_dataset(XML1_ANN, XML1_IMAGES, "xml")
    dataset2 = collect_dataset(XML2_ANN, XML2_IMAGES, "hijab")

    all_items = dataset1 + dataset2
    random.shuffle(all_items)

    split_index = int(len(all_items) * TRAIN_RATIO)
    train_items = all_items[:split_index]
    val_items = all_items[split_index:]

    print(f"Total combined XML files: {len(all_items)}")
    print(f"Train split: {len(train_items)}")
    print(f"Val split: {len(val_items)}")

    train_written = write_split(train_items, "train")
    val_written = write_split(val_items, "val")

    print(f"✅ Written train samples: {train_written}")
    print(f"✅ Written val samples: {val_written}")
    print("✅ Combined XML datasets converted to YOLO format successfully.")

if __name__ == "__main__":
    main()