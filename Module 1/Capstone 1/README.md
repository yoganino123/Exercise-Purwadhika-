# Rental Mobil App (Terminal)

Aplikasi terminal Python untuk manajemen data rental mobil berbasis MySQL.

## Fitur Menu Utama

- Lihat data rental dengan filter `LIKE` (jenis mobil & metode pembayaran) dan sorting `total_bayar` (asc,desc).
- Tambah data rental baru dengan validasi input.
- Statistik rental (total transaksi, pendapatan, mean, median, mobil terlaris).
- Visualisasi data (pie, bar, histogram).
- Lihat daftar jenis mobil, metode pembayaran, dan tambah 10 data dummy.

## Instalasi singkat

```powershell
# dari folder root project
cd "Module 1/Capstone 1"
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install mysql-connector-python numpy pandas matplotlib
```

## Menjalankan aplikasi

```powershell
python app.py
```

## Alur awal aplikasi

1. Cek koneksi MySQL server.
2. Jika database belum ada, bisa create database.
3. Jika tabel `rental_mobil` belum ada, menu hanya:
   - `1. Create Table`
   - `2. Exit`
4. Jika tabel sudah ada, masuk ke menu utama rental.
