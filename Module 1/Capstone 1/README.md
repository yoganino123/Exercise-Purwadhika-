# Rental Mobil App (Terminal)

Aplikasi terminal Python untuk manajemen data rental mobil berbasis MySQL.

## Menu Utama Rental Mobil

- Lihat data rental dengan filter `LIKE` (jenis mobil & metode pembayaran) dan sorting `total_bayar` (asc,desc).
- Tambah data rental baru dengan validasi input.
- Statistik rental (total transaksi, pendapatan, mean, median, mobil terlaris).
- Visualisasi data (pie, bar, histogram).
- Lihat daftar jenis mobil & metode pembayaran
- Tambah 10 data dummy.

## Instalasi singkat

1. Masuk ke folder project:
   ```powershell
   cd "Module 1/Capstone 1"
   ```
2. Buat dan aktifkan virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependency:

   ```powershell
   python -m pip install mysql-connector-python numpy pandas matplotlib
   ```

   - `mysql-connector-python`: koneksi Python ke MySQL (connect, query, commit).
   - `numpy`: bantu perhitungan numerik (contoh median di statistik).
   - `pandas`: olah data tabular ke `DataFrame` untuk analisis/tampilan data.
   - `matplotlib`: membuat visualisasi grafik (pie, bar, histogram).

## Menjalankan aplikasi

```powershell
python app.py
```

## Flow Aplikasi

1. Aplikasi mengecek koneksi ke server MySQL dan menyediakan menu untuk input kredensial MySQL dan test connection.
2. Jika database belum ada, tersedia menu untuk membuat database.
3. Jika tabel `rental_mobil` belum ada, teradpart menu:
   - `1. Create Table`
   - `2. Exit`
4. Jika tabel sudah ada, aplikasi akan masuk ke menu utama rental.
