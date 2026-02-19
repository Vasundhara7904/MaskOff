import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from PIL import Image

# ===== PATHS (based on your structure) =====
SOURCE_MASKED = "./augment-masked"
SOURCE_UNMASKED = "./augment-unmasked"

OUTPUT_MASKED = "./augmented_dataset/masked"
OUTPUT_UNMASKED = "./augmented_dataset/unmasked"

TARGET = 1000
IMG_SIZE = (128, 128)

# Ensure output folders exist
os.makedirs(OUTPUT_MASKED, exist_ok=True)
os.makedirs(OUTPUT_UNMASKED, exist_ok=True)

datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.15,
    height_shift_range=0.15,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest'
)

def process_class(source_folder, output_folder):
    images = [f for f in os.listdir(source_folder)
              if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    count = 0

    # Clear old images (optional but recommended)
    for f in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, f))

    # Copy originals first
    for img_name in images:
        try:
            img_path = os.path.join(source_folder, img_name)
            img = load_img(img_path, target_size=IMG_SIZE)
            img.save(os.path.join(output_folder, f"orig_{count}.jpg"))
            count += 1
            if count >= TARGET:
                return
        except:
            print(f"Skipping corrupted file: {img_name}")

    # Generate augmented images
    i = 0
    while count < TARGET:
        img_name = np.random.choice(images)
        img_path = os.path.join(source_folder, img_name)

        try:
            img = load_img(img_path, target_size=IMG_SIZE)
            x = img_to_array(img)
            x = x.reshape((1,) + x.shape)

            for batch in datagen.flow(x, batch_size=1):
                batch_img = batch[0].astype('uint8')
                Image.fromarray(batch_img).save(
                    os.path.join(output_folder, f"aug_{i}.jpg")
                )
                count += 1
                i += 1
                break
        except:
            print(f"Skipping corrupted file: {img_name}")

print("Processing masked images...")
process_class(SOURCE_MASKED, OUTPUT_MASKED)

print("Processing unmasked images...")
process_class(SOURCE_UNMASKED, OUTPUT_UNMASKED)

print("✅ DONE — 1000 masked and 1000 unmasked images created.")
