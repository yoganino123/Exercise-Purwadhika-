USE rental_mobil_db;

INSERT INTO rental_mobil (
    nama_pelanggan,
    jenis_mobil,
    harga_per_hari,
    lama_sewa,
    total_bayar,
    metode_pembayaran,
    tanggal_sewa
)
VALUES
('Andi', 'Toyota Avanza', 350000, 3, 1050000, 'Cash', '2026-02-01'),
('Budi', 'Honda Brio', 300000, 2, 600000, 'Transfer', '2026-02-02'),
('Citra', 'Daihatsu Xenia', 320000, 5, 1600000, 'QRIS', '2026-02-03'),
('Dimas', 'Toyota Innova', 500000, 4, 2000000, 'Cash', '2026-02-04'),
('Eka', 'Suzuki Ertiga', 330000, 1, 330000, 'Transfer', '2026-02-05'),
('Fajar', 'Mitsubishi Xpander', 420000, 2, 840000, 'Debit', '2026-02-06'),
('Gita', 'Honda Mobilio', 340000, 3, 1020000, 'Cash', '2026-02-07'),
('Hana', 'Toyota Agya', 280000, 2, 560000, 'QRIS', '2026-02-08'),
('Intan', 'Nissan Livina', 360000, 6, 2160000, 'Transfer', '2026-02-09'),
('Joko', 'Wuling Almaz', 550000, 2, 1100000, 'Kartu Kredit', '2026-02-10');
