"""Website deteksi safety helmet (Flask).

Jalankan:  python app.py   lalu buka http://127.0.0.1:5000
Hasil training dibaca dari folder RUN_DIR (default: runs/helmet),
yaitu folder yang dihasilkan notebook belajar_yolo_helm.ipynb.
"""
import base64
import csv
import io
import json
import os
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_from_directory
from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError

RUN_DIR = Path(os.environ.get("HELMET_RUN", "runs/helmet")).resolve()
WEIGHTS = RUN_DIR / "weights" / "best.pt"
ALLOWED = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
COLORS = {"helmet": (34, 139, 84), "no_helmet": (200, 16, 46)}  # hijau = aman, merah = pelanggaran

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB per upload
_model = None


def get_model():
    global _model
    if _model is None:
        from ultralytics import YOLO  # import berat, tunda sampai dibutuhkan
        _model = YOLO(str(WEIGHTS))
    return _model


def read_results():
    """results.csv -> {kolom: [nilai per epoch]} dengan nama kolom tanpa spasi."""
    path = RUN_DIR / "results.csv"
    if not path.exists():
        return None
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return None
    cols = {k.strip(): [] for k in rows[0]}
    for row in rows:
        for k, v in row.items():
            cols[k.strip()].append(float(v))
    return cols


def run_images():
    """Gambar hasil plot Ultralytics yang ada di RUN_DIR (nama file beda antar versi)."""
    want = {
        "labels": ["labels.jpg"],
        "confusion": ["confusion_matrix_normalized.png"],
        "pr": ["BoxPR_curve.png", "PR_curve.png"],
        "f1": ["BoxF1_curve.png", "F1_curve.png"],
        "val_pred": ["val_batch0_pred.jpg"],
        "val_labels": ["val_batch0_labels.jpg"],
    }
    return {k: next((n for n in names if (RUN_DIR / n).exists()), None) for k, names in want.items()}


def read_metrics():
    """metrics.json ditulis oleh notebook (langkah evaluasi): confusion matrix + metrik per kelas."""
    path = RUN_DIR / "metrics.json"
    return json.loads(path.read_text()) if path.exists() else None


def draw(img, dets):
    out = img.copy()
    d = ImageDraw.Draw(out)
    w = max(2, round(max(img.size) / 300))
    try:
        font = ImageFont.truetype("arial.ttf", max(12, round(max(img.size) / 45)))
    except OSError:
        font = ImageFont.load_default()
    for det in dets:
        x1, y1, x2, y2 = det["box"]
        color = COLORS.get(det["label"], (30, 30, 30))
        d.rectangle([x1, y1, x2, y2], outline=color, width=w)
        text = f"{'Tanpa helm' if det['label'] == 'no_helmet' else 'Helm'} {det['conf']:.0%}"
        l, t, r, b = d.textbbox((0, 0), text, font=font)
        th = b - t + 2 * w
        ty = y1 - th if y1 - th > 0 else y2  # label di atas kotak, atau di bawah kalau mepet tepi
        d.rectangle([x1, ty, x1 + r - l + 2 * w, ty + th], fill=color)
        d.text((x1 + w - l, ty + w - t), text, fill="white", font=font)
    return out


@app.get("/")
def index():
    return render_template(
        "index.html",
        has_model=WEIGHTS.exists(),
        run_dir=str(RUN_DIR),
        results=read_results(),
        images=run_images(),
        metrics=read_metrics(),
    )


@app.get("/run/<path:name>")
def run_file(name):
    if Path(name).suffix.lower() not in {".png", ".jpg"}:
        abort(404)
    return send_from_directory(RUN_DIR, name)  # send_from_directory menolak path traversal


@app.post("/api/detect")
def detect():
    if not WEIGHTS.exists():
        return jsonify(error=f"Model belum ada. Taruh hasil training di {RUN_DIR} (lihat bagian Cara pakai)."), 503
    file = request.files.get("image")
    if not file or Path(file.filename or "").suffix.lower() not in ALLOWED:
        return jsonify(error="Pilih file gambar JPG, PNG, BMP, atau WEBP."), 400
    try:
        img = ImageOps.exif_transpose(Image.open(file.stream)).convert("RGB")
    except (UnidentifiedImageError, OSError):
        return jsonify(error="File tidak bisa dibaca sebagai gambar. Coba file lain."), 400
    conf = min(max(request.form.get("conf", 0.4, type=float), 0.05), 0.95)

    res = get_model().predict(img, conf=conf, imgsz=640, verbose=False)[0]
    dets = [
        {"label": res.names[int(c)], "conf": float(p), "box": [round(v) for v in b]}
        for b, c, p in zip(res.boxes.xyxy.tolist(), res.boxes.cls.tolist(), res.boxes.conf.tolist())
    ]
    dets.sort(key=lambda d: (d["label"] != "no_helmet", -d["conf"]))

    buf = io.BytesIO()
    draw(img, dets).save(buf, "JPEG", quality=88)
    return jsonify(
        image="data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(),
        no_helmet=sum(d["label"] == "no_helmet" for d in dets),
        helmet=sum(d["label"] == "helmet" for d in dets),
        detections=dets,
        speed_ms=round(sum(v for v in res.speed.values() if v)),
        conf=conf,
    )


@app.errorhandler(413)
def too_large(_):
    return jsonify(error="Ukuran file lebih dari 10 MB. Perkecil gambarnya dulu."), 413


if __name__ == "__main__":
    # Tanpa debug/reloader: reloader ikut memantau site-packages dan me-restart server
    # saat Ultralytics di-import pada upload pertama, sehingga request terputus.
    app.run()
