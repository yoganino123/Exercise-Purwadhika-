USE rental_mobil_db;

CREATE TABLE IF NOT EXISTS rental_mobil (
    rental_id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pelanggan VARCHAR(100) NOT NULL,
    jenis_mobil VARCHAR(100) NOT NULL,
    harga_per_hari INT NOT NULL,
    lama_sewa INT NOT NULL,
    total_bayar INT NOT NULL,
    metode_pembayaran VARCHAR(50) NOT NULL,
    tanggal_sewa DATE NOT NULL
);
