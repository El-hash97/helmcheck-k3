# Helmcheck K3

Deteksi pekerja tanpa helm di area pabrik dengan YOLOv8. Tersedia website Flask untuk upload foto, kurva training, dan heatmap evaluasi, serta notebook untuk belajar dan melatih model sendiri.

## Coba cepat (pakai model yang sudah dilatih)

1. Unduh [`helmet_run.zip`](https://github.com/El-hash97/helmcheck-k3/releases/download/v1.0/helmet_run.zip) dari [Release v1.0](https://github.com/El-hash97/helmcheck-k3/releases/tag/v1.0), lalu ekstrak ke folder `runs/` di project ini, sehingga ada `runs/helmet/weights/best.pt`.
2. Pasang dependensi dan jalankan website:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
3. Buka http://127.0.0.1:5000, lalu unggah foto area kerja.

Model v1.0: YOLOv8n, 50 epoch, 640 px, 4000 gambar latih. Hasil pada data validasi: precision 92,7%, recall 91,0%, mAP50 95,4%. Pada 500 gambar test: mAP50 91,7%.

## Isi repo

| File | Isi |
|---|---|
| `train_colab.ipynb` | Training cepat di Colab dari `dataset.zip` (format YOLO) di Google Drive: perbaiki `data.yaml`, ubah kelas `head` → `no_helmet`, training, evaluasi, `metrics.json`, zip hasil untuk website. |
| `belajar_yolo_helm.ipynb` | Tutorial bertahap (Bahasa Indonesia): dataset → konversi VOC ke YOLO → split → training → kurva → evaluasi + heatmap → inference → export untuk website. Siap dijalankan di Google Colab (T4 GPU). |
| `brand/` | Logo Helmcheck K3 (monogram H berhelm): master SVG, lockup, varian warna, set ikon web, papan presentasi, dan panduan di `brand/GUIDELINES.md`. |
| `app.py`, `templates/`, `static/` | Website Flask: deskripsi model, kurva training interaktif, heatmap confusion matrix dan sebaran posisi kepala, cara pakai, dan upload foto untuk menandai orang tanpa helm. |

Melatih model sendiri:

1. Jalankan `train_colab.ipynb` (dari `dataset.zip` di Google Drive) atau `belajar_yolo_helm.ipynb` (unduh dari Kaggle) di Colab. Sel terakhir mengunduh `helmet_run.zip`.
2. Ekstrak zip ke folder project sehingga ada `runs/helmet/weights/best.pt`.
3. `pip install -r requirements.txt`, lalu `python app.py`, dan buka http://127.0.0.1:5000

Folder hasil training lain bisa dipakai lewat environment variable `HELMET_RUN=path/ke/run`.

**Kredit:**
- Dikembangkan dari [addeligero/YOLOV8-safety-helmet-detection](https://github.com/addeligero/YOLOV8-safety-helmet-detection). README asli ada di bawah.
- Dataset: [Hard Hat Workers](https://www.kaggle.com/datasets/andrewmvd/hard-hat-detection) (Kaggle).
- Font: Archivo (SIL OFL).

---

This project implements a Safety Helmet Detection System using YOLOv8.
The model is trained to detect whether construction workers are wearing a helmet or not using a dataset originally sourced from Kaggle (Hard Hat Workers Dataset).

📌 Project Overview

Task: Object Detection

Model: YOLOv8

Framework: Ultralytics

Dataset Format: YOLOv8

Classes:

0 → helmet

1 → no_helmet (head)

The project converts Pascal VOC (.xml) annotations into YOLO format, trains a YOLOv8 model, and evaluates its performance using Precision, Recall, and mAP50.

YOLOv8-csc/
│
├── dataset/
│ ├── images/ # Original images
│ ├── annotations/ # Pascal VOC (.xml) annotations
│ ├── yolo_labels/ # Converted YOLO labels (.txt)
│
├── data/
│ ├── train/
│ │ ├── images/
│ │ └── labels/
│ ├── val/
│ │ ├── images/
│ │ └── labels/
│
├── voc_to_yolo.py # Converts VOC XML → YOLO format
├── split_dataset.py # Splits dataset into train/validation
├── data.yaml # YOLO dataset configuration
├── requirements.txt # Python dependencies
├── .gitignore
└── README.md

Environment Setup
1️⃣ Create Virtual Environment (Recommended)
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Dataset Source

The dataset is sourced from Kaggle:

🔗 https://www.kaggle.com/datasets/andrewmvd/hard-hat-detection

It contains:

~5,000 images

Pascal VOC annotations

Labels: helmet, head, person

Only helmet and head are used in this project.

Convert Annotations to YOLO Format

Run the conversion script:

python voc_to_yolo.py

This will:

Read .xml annotation files

Convert bounding boxes to YOLO format

Skip unused labels such as person

Save .txt labels to dataset/yolo_labels/

Split Dataset (Train / Validation)

Run:

python split_dataset.py

This will:

Create data/train and data/val folders

Copy images and labels into YOLO-ready structure

Dataset Configuration (data.yaml)

Example:

path: data
train: train/images
val: val/images

names:
0: helmet
1: no_helmet

Training the YOLOv8 Model

Train the model for 20–50 epochs:

yolo detect train model=yolov8n.pt data=data.yaml epochs=40 imgsz=640

Training outputs will be saved automatically in:

runs/detect/train/

📊 Evaluation Metrics

After training, YOLOv8 automatically generates:
Precision (P)

Recall (R)

mAP@0.5

mAP@0.5:0.95

Confusion Matrix

Training Curves

These results are used for performance evaluation and reporting.

🔍 Inference (Testing)

To test the trained model on an image or video:

yolo detect predict model=runs/detect/train/weights/best.pt source=your_image.jpg
