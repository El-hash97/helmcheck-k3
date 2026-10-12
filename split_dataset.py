import os
import random
import shutil

IMG_DIR = "dataset/images"
LBL_DIR = "dataset/yolo_labels"

train_img_dir = "dataset/images/train"
val_img_dir = "dataset/images/val"
train_lbl_dir = "dataset/labels/train"
val_lbl_dir = "dataset/labels/val"

os.makedirs(train_img_dir, exist_ok=True)
os.makedirs(val_img_dir, exist_ok=True)
os.makedirs(train_lbl_dir, exist_ok=True)
os.makedirs(val_lbl_dir, exist_ok=True)

images = [f for f in os.listdir(IMG_DIR) if f.endswith(('.jpg', '.png'))]

random.Random(42).shuffle(images)
n_val = int(len(images) * 0.2)
val_imgs, train_imgs = images[:n_val], images[n_val:]

def copy_split(files, split_img_dir, split_lbl_dir):
    for img in files:
        lbl = img.replace(".png", ".txt").replace(".jpg", ".txt")

        shutil.copy(os.path.join(IMG_DIR, img), os.path.join(split_img_dir, img))
        shutil.copy(os.path.join(LBL_DIR, lbl), os.path.join(split_lbl_dir, lbl))

copy_split(train_imgs, train_img_dir, train_lbl_dir)
copy_split(val_imgs, val_img_dir, val_lbl_dir)

print("✅ Train/Val split completed!")
