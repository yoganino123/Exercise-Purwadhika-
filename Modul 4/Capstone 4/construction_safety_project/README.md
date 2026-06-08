# Construction Safety Capstone Project

Project ini dibuat untuk Capstone Project Module 4 dengan kasus Construction Safety. Solusi mencakup training model object detection, analisis kepatuhan APD pekerja, dan integrasi ke aplikasi Streamlit.

## Objective

- Mendeteksi objek `helmet`, `no-helmet`, `no-vest`, `person`, dan `vest`
- Menghitung jumlah objek terdeteksi pada gambar
- Menilai pekerja yang patuh dan tidak patuh terhadap penggunaan APD
- Menyediakan aplikasi Streamlit sederhana untuk demo inferensi

## Project Structure

```text
construction_safety_project/
|-- app.py
|-- train.py
|-- requirements.txt
|-- README.md
|-- artifacts/
|-- runs/
`-- src/
    |-- __init__.py
    |-- config.py
    |-- predictor.py
    `-- ppe_analysis.py
```

## Dataset

- Dataset folder: `../construction safety.v1i.yolov12`
- Dataset config: `../construction safety.v1i.yolov12/data.yaml`
- Example image: `../Contoh Data Test/construction-workers.jpg`

Dataset sudah dalam format YOLO sehingga bisa langsung dipakai oleh Ultralytics.

## Setup

```bash
pip install -r requirements.txt
```

## Training

```bash
python train.py --epochs 30 --imgsz 640 --batch 16 --device cpu
```

### Run Training di Google Colab (Recommended)

1. Upload folder `construction_safety_project` dan folder dataset `construction safety.v1i.yolov12` ke Google Drive.
2. Buka Google Colab dan pilih runtime GPU:
   - Runtime > Change runtime type > Hardware accelerator > T4 GPU
3. Jalankan cell berikut di Colab:

```python
from google.colab import drive
drive.mount('/content/drive')
```

4. Sesuaikan path project, lalu install dependency:

```bash
%cd /content/drive/MyDrive/path_ke_project/construction_safety_project
!pip install -r requirements.txt
```

5. Jalankan training di GPU:

```bash
!python train.py --epochs 30 --imgsz 640 --batch 16 --device 0
```

6. Setelah selesai, model terbaik akan tersedia di:
   - `construction_safety_project/artifacts/best.pt`

7. Download `best.pt` ke laptop atau biarkan di Drive, lalu pakai untuk inferensi di Streamlit lokal.

Tips Colab:

- Jika session sering disconnect, simpan hasil model tiap selesai training.
- Jika OOM (out of memory), turunkan `--batch` ke 8 atau 4.
- Untuk quick test, pakai `--epochs 10` dulu sebelum final run.

Catatan:

- Jika tersedia GPU, ganti `--device cpu` menjadi `--device 0`
- Hasil training tersimpan di folder `runs/`
- File model terbaik akan disalin ke `artifacts/best.pt`

## Run Streamlit App

```bash
streamlit run app.py
```

## Minimum Features Implemented

- Load model object detection hasil training
- Upload image atau gunakan sample image
- Visualisasi bounding box hasil prediksi
- Hitung jumlah object per class
- Analisis PPE compliance per pekerja
- Ringkasan total pekerja patuh dan tidak patuh

## Suggested Presentation Flow

- Jelaskan objective dan dataset yang dipilih
- Tunjukkan pipeline preprocessing dan training
- Tampilkan metrik hasil model
- Demo aplikasi Streamlit dengan gambar uji
- Jelaskan bagaimana hasil deteksi diubah menjadi analisis compliance pekerja
