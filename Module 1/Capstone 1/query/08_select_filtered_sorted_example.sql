USE rental_mobil_db;

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
WHERE jenis_mobil = 'Toyota Avanza'
  AND metode_pembayaran = 'Cash'
ORDER BY total_bayar DESC;