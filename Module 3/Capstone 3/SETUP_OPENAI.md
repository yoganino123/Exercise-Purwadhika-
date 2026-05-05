# Tutorial Lengkap: Mendapatkan OpenAI API Key

Panduan ini menjelaskan langkah demi langkah cara membuat akun OpenAI, menambahkan kredit, dan mendapatkan API key untuk digunakan di Capstone Project Module 3.

---

## Daftar Isi

1. [Buat Akun OpenAI](#1-buat-akun-openai)
2. [Verifikasi Akun](#2-verifikasi-akun)
3. [Tambahkan Kredit (Billing)](#3-tambahkan-kredit-billing)
4. [Buat API Key](#4-buat-api-key)
5. [Cek Penggunaan & Batas](#5-cek-penggunaan--batas)
6. [Estimasi Biaya Capstone](#6-estimasi-biaya-capstone)
7. [Keamanan API Key](#7-keamanan-api-key)

---

## 1. Buat Akun OpenAI

1. Buka browser dan pergi ke **https://platform.openai.com/**

2. Klik tombol **"Sign up"** di pojok kanan atas

   ![Sign Up Page](https://platform.openai.com)

3. Pilih metode registrasi:
   - **Continue with Google** ← cara tercepat
   - **Continue with Microsoft**
   - Atau isi email + password manual

4. Jika daftar dengan email manual:
   - Masukkan email aktif kamu
   - Buat password yang kuat (minimal 12 karakter)
   - Klik **"Continue"**

5. Cek email kamu → klik link **"Verify email address"** yang dikirim OpenAI

6. Isi nama lengkap dan tanggal lahir, lalu klik **"Continue"**

7. Masukkan nomor telepon untuk verifikasi SMS, lalu klik **"Send code"**

8. Masukkan 6 digit kode OTP yang dikirim ke nomor HP kamu

> Setelah verifikasi, kamu akan diarahkan ke dashboard OpenAI Platform.

---

## 2. Verifikasi Akun

Setelah berhasil daftar, kamu akan berada di halaman **https://platform.openai.com/**.

Pastikan tampilan dashboard sudah muncul:

- Nama akun kamu di pojok kanan atas
- Menu navigasi di sebelah kiri: **Dashboard**, **API keys**, **Usage**, dll.

---

## 3. Tambahkan Kredit (Billing)

OpenAI menggunakan sistem **pay-as-you-go** — kamu membayar sesuai token yang digunakan. Untuk Capstone ini, **$5 USD sudah sangat cukup**.

### Langkah-langkah:

1. Di dashboard, klik nama akun / organisasi kamu di pojok kanan atas

2. Klik **"Billing"** di menu dropdown  
   Atau langsung buka: **https://platform.openai.com/settings/organization/billing**

3. Klik tombol **"Add payment method"**

4. Masukkan data kartu kredit/debit kamu:
   - Nomor kartu
   - Tanggal kedaluwarsa (MM/YY)
   - CVV (3 digit di belakang kartu)
   - Nama pemilik kartu
   - Alamat billing (bisa pakai alamat rumah)

   > **Catatan:** OpenAI menerima Visa, Mastercard, American Express. Untuk kartu Indonesia (BCA, BNI, BRI, Mandiri), pastikan kartu kamu sudah diaktifkan untuk transaksi internasional online.

5. Klik **"Add payment method"** untuk menyimpan

6. Setelah kartu terdaftar, klik **"Add to credit balance"**

7. Masukkan jumlah yang ingin di-top up (minimum **$5 USD**)

8. Klik **"Continue"** → konfirmasi → klik **"Confirm payment"**

9. Cek email — kamu akan mendapat konfirmasi pembayaran

> **Alternatif jika kartu Indonesia tidak bisa:** Gunakan virtual card seperti **Jenius e-Card**, **DANA Virtual Account**, atau minta tolong orang tua/teman yang memiliki kartu dengan akses transaksi internasional.

### Cek Saldo:

Setelah top-up, saldo bisa dicek di:
**https://platform.openai.com/settings/organization/billing** → bagian **"Credit balance"**

---

## 4. Buat API Key

API Key adalah "password" yang kamu gunakan agar aplikasi Python bisa mengakses OpenAI.

### Langkah-langkah:

1. Di menu kiri, klik **"API keys"**  
   Atau langsung buka: **https://platform.openai.com/api-keys**

2. Klik tombol **"+ Create new secret key"**

3. Isi detail key:
   - **Name:** Beri nama deskriptif, misal `capstone-3-project`
   - **Project:** Biarkan default atau pilih project yang sesuai
   - **Permissions:** Pilih **"All"** (untuk kemudahan development)

4. Klik **"Create secret key"**

5. **SANGAT PENTING:** Salin key yang muncul sekarang!  
   Key hanya ditampilkan **SATU KALI**. Setelah kamu tutup dialog ini, key tidak bisa dilihat lagi.

   Format key: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

6. Simpan key di tempat yang aman:
   - Paste ke file `.env` di project kamu (jangan di-commit ke GitHub!)
   - Simpan di password manager (misal: Bitwarden, 1Password)

7. Klik **"Done"** untuk menutup dialog

### Tampilan setelah berhasil:

Di halaman API keys, kamu akan melihat key baru dengan status **"Active"** dan nama yang tadi kamu beri.

> **Jika key terekspos / bocor:** Segera klik **"Revoke"** di sebelah key tersebut, lalu buat key baru. Key yang sudah di-revoke tidak bisa digunakan lagi.

---

## 5. Cek Penggunaan & Batas

### Melihat Usage:

Buka: **https://platform.openai.com/usage**

Di sini kamu bisa melihat:

- Total token yang digunakan hari ini / bulan ini
- Breakdown per model (gpt-4o-mini, text-embedding-3-small, dll)
- Grafik penggunaan harian

### Set Usage Limit (Penting!):

Untuk mencegah tagihan membengkak, set batas maksimal pengeluaran:

1. Buka **https://platform.openai.com/settings/organization/limits**
2. Di bagian **"Usage limits"**, set:
   - **Monthly budget:** misal $5
   - **Email notification threshold:** misal $3 (dapat peringatan sebelum habis)
3. Klik **"Save"**

Setelah batas tercapai, API akan menolak request dengan error `429 - Insufficient quota` sampai bulan berikutnya atau kamu top-up lagi.

---

## 6. Estimasi Biaya Capstone

Berikut estimasi biaya menggunakan model yang dipakai di project ini:

### Model yang Digunakan:

| Model                    | Kegunaan                       | Harga Input      | Harga Output     |
| ------------------------ | ------------------------------ | ---------------- | ---------------- |
| `text-embedding-3-small` | Membuat embedding data & query | $0.02 / 1M token | -                |
| `gpt-4o-mini`            | LLM untuk agent/chat           | $0.15 / 1M token | $0.60 / 1M token |

### Estimasi Biaya Upload Data:

**Dataset IMDB (1000 baris):**

- Rata-rata ~200 token per dokumen
- Total: 1.000 × 200 = 200.000 token
- Biaya embedding: 200.000 / 1.000.000 × $0.02 = **$0.004** (sangat murah!)

**Dataset Resume (2400 baris, dibatasi 500 token per dokumen):**

- Total: 2.400 × 500 = 1.200.000 token
- Biaya embedding: 1.200.000 / 1.000.000 × $0.02 = **$0.024**

### Estimasi Biaya Testing & Demo:

Setiap satu percakapan chatbot (1 pertanyaan + 1 jawaban) dengan GPT-4o-mini:

- Input: ~1.500 token (system prompt + history + dokumen RAG + pertanyaan)
- Output: ~300 token (jawaban)
- Biaya per pesan: (1.500 × $0.15 + 300 × $0.60) / 1.000.000 = **$0.0004**
- Dalam Rupiah (kurs Rp 17.000): **≈ Rp 6.8 per pesan**

**Estimasi total untuk development + testing + demo: $1–$3 USD**

> **Kesimpulan:** Saldo $5 USD lebih dari cukup untuk seluruh pengerjaan Capstone Project ini.

---

## 7. Keamanan API Key

Ini sangat penting untuk diperhatikan:

### JANGAN lakukan ini:

- ❌ Hardcode API key langsung di source code: `api_key = "sk-proj-xxxxx"`
- ❌ Commit file `.env` ke GitHub
- ❌ Share API key di WhatsApp, Discord, atau chat apapun
- ❌ Tampilkan API key di video presentasi
- ❌ Upload screenshot yang menampilkan API key

### LAKUKAN ini:

- ✅ Simpan di file `.env` (dan pastikan `.env` ada di `.gitignore`)
- ✅ Gunakan `st.secrets` untuk Streamlit Cloud
- ✅ Gunakan `os.getenv()` untuk membaca dari environment variable
- ✅ Set usage limit untuk mencegah tagihan tak terduga

### Cara Aman Menggunakan API Key:

**Lokal (development):**

```python
# Di file .env (TIDAK di-commit ke GitHub)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Di main.py
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

**Streamlit Cloud (production):**

```python
# Di Streamlit Cloud → App Settings → Secrets
# Tambahkan:
# OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxx"

# Di main.py
import streamlit as st
api_key = st.secrets["OPENAI_API_KEY"]
```

**Cara paling aman (works di lokal DAN Streamlit Cloud):**

```python
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()  # load .env untuk lokal

# st.secrets untuk production, os.getenv sebagai fallback untuk lokal
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
```

---

## Troubleshooting Umum

| Error                                             | Penyebab                                        | Solusi                                                                           |
| ------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------- |
| `AuthenticationError: Incorrect API key`          | API key salah atau sudah di-revoke              | Cek kembali key di `.env`, buat key baru jika perlu                              |
| `RateLimitError: You exceeded your current quota` | Saldo habis atau limit tercapai                 | Top-up kredit di billing page                                                    |
| `RateLimitError: Rate limit reached`              | Terlalu banyak request dalam waktu singkat      | Tambahkan `time.sleep(1)` antar request saat upload data                         |
| Kartu ditolak saat billing                        | Kartu tidak aktif untuk transaksi internasional | Aktifkan fitur transaksi internasional di aplikasi bank, atau gunakan kartu lain |

---

## Referensi

- [OpenAI Platform](https://platform.openai.com/)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [OpenAI Pricing](https://openai.com/api/pricing/)
- [OpenAI Usage Dashboard](https://platform.openai.com/usage)
- [OpenAI Docs - Quickstart](https://platform.openai.com/docs/quickstart)
