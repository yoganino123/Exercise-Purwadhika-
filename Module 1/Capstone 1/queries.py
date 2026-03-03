# Kumpulan query SQL untuk aplikasi rental mobil

CREATE_TABLE_RENTAL_MOBIL = """
CREATE TABLE IF NOT EXISTS rental_mobil (
    rental_id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pelanggan VARCHAR(100) NOT NULL,
    jenis_mobil VARCHAR(100) NOT NULL,
    harga_per_hari INT NOT NULL,
    lama_sewa INT NOT NULL,
    total_bayar INT NOT NULL,
    metode_pembayaran VARCHAR(50) NOT NULL,
    tanggal_sewa DATE NOT NULL
)
"""

INSERT_RENTAL_MOBIL = """
INSERT INTO rental_mobil (
    nama_pelanggan,
    jenis_mobil,
    harga_per_hari,
    lama_sewa,
    total_bayar,
    metode_pembayaran,
    tanggal_sewa
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

SELECT_RENTAL_MOBIL_BASE = (
    "SELECT rental_id, nama_pelanggan, jenis_mobil, harga_per_hari, lama_sewa, "
    "total_bayar, metode_pembayaran, tanggal_sewa FROM rental_mobil"
)

SHOW_DATABASES_LIKE = "SHOW DATABASES LIKE %s"
SHOW_TABLES_LIKE = "SHOW TABLES LIKE %s"

DUMMY_RENTAL_DATA = [
    ("Andi", "Toyota Avanza", 350000, 3, 1050000, "Cash", "2026-02-01"),
    ("Budi", "Honda Brio", 300000, 2, 600000, "Transfer", "2026-02-02"),
    ("Citra", "Daihatsu Xenia", 320000, 5, 1600000, "QRIS", "2026-02-03"),
    ("Dimas", "Toyota Innova", 500000, 4, 2000000, "Cash", "2026-02-04"),
    ("Eka", "Suzuki Ertiga", 330000, 1, 330000, "Transfer", "2026-02-05"),
    ("Fajar", "Mitsubishi Xpander", 420000, 2, 840000, "Debit", "2026-02-06"),
    ("Gita", "Honda Mobilio", 340000, 3, 1020000, "Cash", "2026-02-07"),
    ("Hana", "Toyota Agya", 280000, 2, 560000, "QRIS", "2026-02-08"),
    ("Intan", "Nissan Livina", 360000, 6, 2160000, "Transfer", "2026-02-09"),
    ("Joko", "Wuling Almaz", 550000, 2, 1100000, "Kartu Kredit", "2026-02-10"),
]


def build_create_database_query(database_name):
    return f"CREATE DATABASE IF NOT EXISTS {database_name}"
