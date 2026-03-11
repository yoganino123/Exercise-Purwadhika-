# Rental Mobil App (Terminal)

Aplikasi terminal Python untuk manajemen data rental mobil.

## Menu Utama Rental Mobil

- Lihat data rental dengan filter `LIKE` (jenis mobil & metode pembayaran) dan sorting `total_bayar` (asc,desc).
- Tambah data rental baru dengan validasi input.
- Statistik rental (total transaksi, pendapatan, mean, median, mobil terlaris).
- Visualisasi data (pie, bar, histogram).
- Lihat daftar jenis mobil & metode pembayaran
- Tambah 10 data dummy.

## Module / Library

- `mysql-connector-python`: koneksi Python ke MySQL (connect, query, commit).
- `numpy`: bantu perhitungan numerik (contoh median di statistik).
- `pandas`: olah data tabular ke `DataFrame` untuk analisis/tampilan data.
- `matplotlib`: membuat visualisasi grafik (pie, bar, histogram).

## Struktur Project (Modular) :

- app.py: entry point aplikasi.
- config.py: konfigurasi database dari `.env`.
- database.py: koneksi dan operasi database.
- features.py: implementasi menu utama.
- queries.py + query/: kumpulan SQL query.
- utils.py: helper validasi input.

## Konfigurasi Credential (.env)

- Credential database disimpan di file `.env`.
- Jika file `.env` belum ada, aplikasi akan membuat otomatis saat dijalankan.
- Menu **Input Credential MySQL** akan memperbarui nilai `DB_HOST`, `DB_USER`, `DB_PASSWORD`, dan `DB_DATABASE` di `.env`.

## Flow Aplikasi

1. Aplikasi mengecek koneksi ke server MySQL dan menyediakan menu untuk input kredensial MySQL dan test connection.
2. Jika database belum ada, tersedia menu untuk membuat database.
3. Jika tabel `rental_mobil` belum ada, teradpart menu:
   - `1. Create Table`
   - `2. Exit`
4. Jika tabel sudah ada, aplikasi akan masuk ke menu utama rental.

## Instalasi singkat

Tujuannya agar dependency terpasang lokal di project ini, bukan secara global di sistem.

### Windows (PowerShell)

1. Masuk ke folder project:
   ```powershell
   cd "Module 1/Capstone 1"
   ```
2. Buat virtual environment:
   ```powershell
   python -m venv .venv
   ```
3. Aktifkan virtual environment:
   ```powershell
   .\.venv\Scripts\activate
   ```
4. Install dependency:
   ```powershell
   python -m pip install mysql-connector-python numpy pandas matplotlib
   ```
5. Jalankan aplikasi:
   ```powershell
   python app.py
   ```

### macOS (zsh)

1. Masuk ke folder project:
   ```bash
   cd "Module 1/Capstone 1"
   ```
2. Buat virtual environment:
   ```bash
   python3 -m venv .venv
   ```
3. Aktifkan virtual environment:
   ```bash
   source .venv/bin/activate
   ```
4. Install dependency:
   ```bash
   python -m pip install mysql-connector-python numpy pandas matplotlib
   ```
5. Jalankan aplikasi:
   ```bash
   python app.py
   ```

> Jika belum mengaktifkan virtual environment di macOS, jalankan aplikasi dengan:
>
> ```bash
> .venv/bin/python app.py
> ```
