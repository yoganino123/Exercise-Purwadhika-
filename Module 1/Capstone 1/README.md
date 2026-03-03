# Rental Mobil App (Terminal)

Aplikasi terminal berbasis Python untuk manajemen rental mobil dengan MySQL.
Project dibuat modular (tanpa class).

## Library yang digunakan
- `mysql-connector-python`: koneksi Python ke MySQL, eksekusi query, dan commit transaksi.
- `numpy`: perhitungan numerik (contoh: median pada statistik).
- `pandas`: olah data tabel/DataFrame untuk baca, filter, sort, dan tampil data.
- `matplotlib`: visualisasi data (pie chart, bar chart, histogram).

## Fitur utama
- Lihat data rental (filter jenis mobil, metode pembayaran, sorting total bayar).
- Tambah data rental (validasi input + hitung otomatis total bayar).
- Statistik rental (total transaksi, pendapatan, mean, median, mobil terlaris, rata-rata lama sewa).
- Visualisasi data rental.
- Tambah dummy data 10 record dari menu utama.

## Struktur file
- `app.py` → entry point aplikasi.
- `config.py` → konfigurasi credential/database.
- `database.py` → koneksi dan operasi database.
- `features.py` → fitur menu utama.
- `utils.py` → helper input/validasi.
- `queries.py` → kumpulan query SQL.
- `query/` → file query `.sql` terpisah untuk pengumpulan.

## Tutorial instalasi
1. Masuk ke folder project:
   ```powershell
   cd "D:\File IT\TRAINING DINO\AI ENGINEERING PURWADIKA\Exercise\Exercise-Purwadhika-\Module 1\Capstone 1"
   ```
2. (Opsional) buat virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install semua dependency:
   ```powershell
   python -m pip install mysql-connector-python numpy pandas matplotlib
   ```

## Cara menjalankan
```powershell
python app.py
```

## Alur menu saat start
1. Jika gagal konek server MySQL:
   - Input credential
   - Test connection
   - Kembali ke menu utama
   - Exit
2. Jika server terkoneksi tapi database belum ada:
   - Create database `rental_mobil_db`
   - Test database ada/tidak
   - Kembali ke menu utama
   - Exit
3. Jika server dan database sudah tersedia:
   - Masuk ke `=== Aplikasi Rental Mobil ===`

## Troubleshooting singkat
- Error `No module named 'matplotlib'`:
  ```powershell
  python -m pip install matplotlib
  ```
- Error `No module named 'mysql'` / `mysql.connector`:
  ```powershell
  python -m pip install mysql-connector-python
  ```
- Jika tetap error, cek interpreter aktif:
  ```powershell
  python -c "import sys; print(sys.executable)"
  ```
