import os

TRAIN_IMG = "yolo_dataset/images/train"
VAL_IMG   = "yolo_dataset/images/val"

TRAIN_LBL = "yolo_dataset/labels/train"
VAL_LBL   = "yolo_dataset/labels/val"

os.makedirs(TRAIN_LBL, exist_ok=True)
os.makedirs(VAL_LBL, exist_ok=True)

IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")

def infer_class_from_path(path: str) -> int:
    p = path.lower()
    # check unmasked first because it contains masked
    if "unmasked" in p:
        return 1
    if "masked" in p:
        return 0
    raise ValueError(f"Cannot infer class from path: {path}")

def write_full_box(label_path: str, class_id: int):
    with open(label_path, "w") as f:
        f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")

def process(img_root: str, lbl_root: str):
    created = 0
    for root, _, files in os.walk(img_root):
        for fname in files:
            if not fname.lower().endswith(IMG_EXTS):
                continue

            img_path = os.path.join(root, fname)
            cid = infer_class_from_path(img_path)

            base = os.path.splitext(fname)[0]
            label_path = os.path.join(lbl_root, base + ".txt")

            write_full_box(label_path, cid)
            created += 1
    return created

train_count = process(TRAIN_IMG, TRAIN_LBL)
val_count   = process(VAL_IMG, VAL_LBL)

print(f"✅ Created {train_count} train labels and {val_count} val labels.")
print("Check: yolo_dataset/labels/train and yolo_dataset/labels/val")
