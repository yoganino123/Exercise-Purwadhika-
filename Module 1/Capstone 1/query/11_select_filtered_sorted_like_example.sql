USE rental_mobil_db;

-- Contoh query sesuai fitur read_data() di code terbaru:
-- filter jenis_mobil LIKE, filter metode_pembayaran LIKE, dan sorting total_bayar.

SELECT
    rental_id,
    nama_pelanggan,
    jenis_mobil,
    harga_per_hari,
    lama_sewa,
    total_bayar,
    metode_pembayaran,
    tanggal_sewa
FROM rental_mobil
WHERE jenis_mobil LIKE '%Toyota%'
  AND metode_pembayaran LIKE '%Cash%'
ORDER BY total_bayar DESC;
