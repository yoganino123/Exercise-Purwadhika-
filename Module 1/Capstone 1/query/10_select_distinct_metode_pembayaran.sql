USE rental_mobil_db;

SELECT DISTINCT
    metode_pembayaran
FROM rental_mobil
WHERE metode_pembayaran IS NOT NULL
  AND metode_pembayaran <> ''
ORDER BY metode_pembayaran ASC;
