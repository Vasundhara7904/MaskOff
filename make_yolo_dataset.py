import os

TRAIN_IMG = "yolo_dataset/images/train"
VAL_IMG   = "yolo_dataset/images/val"

TRAIN_LBL = "yolo_dataset/labels/train"
VAL_LBL   = "yolo_dataset/labels/val"

os.makedirs(TRAIN_LBL, exist_ok=True)
os.makedirs(VAL_LBL, exist_ok=True)

IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")

def get_class_id(filename: str) -> int:
    """
    Assumes filenames contain 'masked' or 'unmasked'.
    Examples:
      masked_abc.jpg -> 0
      unmasked_xyz.jpg -> 1
    """
    name = filename.lower()

    # IMPORTANT: check 'unmasked' first, because it contains 'masked'
    if "unmasked" in name:
        return 1
    if "masked" in name:
        return 0

    raise ValueError(f"Cannot infer class from filename: {filename}")

def write_full_box(label_path: str, class_id: int):
    # YOLO format: class x_center y_center width height (normalized)
    # Full-image bounding box:
    with open(label_path, "w") as f:
        f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")

def process(img_dir, lbl_dir):
    created = 0
    for fname in os.listdir(img_dir):
        if not fname.lower().endswith(IMG_EXTS):
            continue
        class_id = get_class_id(fname)
        base = os.path.splitext(fname)[0]
        label_path = os.path.join(lbl_dir, base + ".txt")
        write_full_box(label_path, class_id)
        created += 1
    return created

train_count = process(TRAIN_IMG, TRAIN_LBL)
val_count = process(VAL_IMG, VAL_LBL)

print(f"✅ Created {train_count} train labels and {val_count} val labels.")
print("Now you can train YOLO.")
