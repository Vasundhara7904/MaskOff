import os, random, shutil

SOURCE = "labelled-dataset"   # masked/ unmasked/
OUT = "yolo_dataset"
TRAIN_RATIO = 0.8

IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".jfif")

classes = {"masked": 0, "unmasked": 1}

# Create dirs (without deleting)
for split in ["train", "val"]:
    os.makedirs(os.path.join(OUT, "images", split), exist_ok=True)
    os.makedirs(os.path.join(OUT, "labels", split), exist_ok=True)

def write_label(path, cid):
    with open(path, "w") as f:
        f.write(f"{cid} 0.5 0.5 1.0 1.0\n")  
        

for cname, cid in classes.items():
    src_dir = os.path.join(SOURCE, cname)
    files = [f for f in os.listdir(src_dir) if f.lower().endswith(IMG_EXTS)]
    random.shuffle(files)

    split_point = int(len(files) * TRAIN_RATIO)
    splits = {
        "train": files[:split_point],
        "val": files[split_point:]
    }

    for split, split_files in splits.items():
        for f in split_files:
            src_img = os.path.join(src_dir, f)

            # unique name
            base, ext = os.path.splitext(f)
            new_name = f"{cname}_{base}{ext}"

            dst_img = os.path.join(OUT, "images", split, new_name)
            dst_lbl = os.path.join(OUT, "labels", split, f"{cname}_{base}.txt")

            shutil.copy(src_img, dst_img)
            write_label(dst_lbl, cid)

print("✅ YOLO dataset created successfully!")
print("Check yolo_dataset/images/train, yolo_dataset/images/val")
