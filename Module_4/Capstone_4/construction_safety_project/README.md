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

## Local Environment (.env)

Semua konfigurasi link model dan nilai sensitif disimpan di `.env`.

1. Copy file contoh:

```bash
cp .env.example .env
```

Untuk Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

2. Isi nilai di `.env`:

```text
MODEL_WEIGHTS_URL=https://drive.google.com/uc?export=download&id=1k-Fwbw5Kmeq6MJRfDNrR8mVnGvPEor4D
MODEL_FORCE_REFRESH=0
```

3. Jalankan app:

```bash
streamlit run app.py
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

## Deploy di Streamlit Cloud

Karena folder `artifacts/` ada di `.gitignore`, file model biasanya tidak ikut ke repo saat deploy.

Model akan diunduh ke `artifacts/best.pt` saat startup berdasarkan value dari Streamlit Secrets.

### Tutorial Deploy Streamlit Cloud

1. Push project ke GitHub.
2. Buka https://share.streamlit.io lalu sign in.
3. Klik **New app**.
4. Pilih repository, branch, dan file utama `app.py`.
5. Buka menu **Advanced settings** > **Secrets**.
6. Isi secrets berikut:

```toml
MODEL_WEIGHTS_URL = "https://drive.google.com/uc?export=download&id=1k-Fwbw5Kmeq6MJRfDNrR8mVnGvPEor4D"
MODEL_FORCE_REFRESH = "0"
```

7. Klik **Deploy**.
8. Tunggu proses install dependency dan startup model selesai.
9. Jika ingin update model dari Drive, ubah:

```toml
MODEL_FORCE_REFRESH = "1"
```

Lalu reboot app, setelah model terbaru terunduh kembalikan lagi ke `"0"`.

Set environment variable berikut pada Streamlit Cloud (optional override):

- `MODEL_WEIGHTS_URL`: override URL model .pt
- `MODEL_FORCE_REFRESH`: set `1` jika ingin paksa download ulang tiap startup

Contoh:

```text
MODEL_WEIGHTS_URL=https://drive.google.com/uc?export=download&id=1k-Fwbw5Kmeq6MJRfDNrR8mVnGvPEor4D
MODEL_FORCE_REFRESH=0
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
