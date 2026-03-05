USE rental_mobil_db;

SELECT DISTINCT
    jenis_mobil
FROM rental_mobil
WHERE jenis_mobil IS NOT NULL
  AND jenis_mobil <> ''
ORDER BY jenis_mobil ASC;
