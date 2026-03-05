import numpy as np
import matplotlib.pyplot as plt

from database import (
    get_distinct_jenis_mobil,
    get_distinct_metode_pembayaran,
    get_rental_dataframe,
    insert_dummy_data,
)
from queries import INSERT_RENTAL_MOBIL
from utils import (
    get_date_input,
    get_menu_choice,
    get_non_empty_input,
    get_non_negative_int,
    safe_input,
)

try:
    from mysql.connector import Error
except ImportError:
    Error = Exception


def format_console_table(df):
    headers = ["(index)", *[str(column) for column in df.columns]]
    rows = [
        [str(row_index), *["" if value is None else str(value) for value in row]]
        for row_index, row in enumerate(df.values.tolist())
    ]

    widths = []
    for index, header in enumerate(headers):
        cell_width = max((len(row[index]) for row in rows), default=0)
        widths.append(max(len(header), cell_width))

    def separator(char="-"):
        return "+" + "+".join(char * (width + 2) for width in widths) + "+"

    header_row = "| " + " | ".join(header.ljust(widths[i]) for i, header in enumerate(headers)) + " |"
    body_rows = [
        "| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(headers))) + " |"
        for row in rows
    ]

    return "\n".join([separator("-"), header_row, separator("="), *body_rows, separator("-")])


# Fungsi untuk menampilkan data rental dengan filter dan sorting dinamis
def read_data(connection):
    print("\n=== Lihat Data Rental ===")

    where_conditions = []
    params = []

    try:
        filter_jenis = safe_input("Filter jenis mobil (kosongkan jika tidak): ").strip()
        if filter_jenis:
            where_conditions.append("jenis_mobil LIKE %s")
            params.append(f"%{filter_jenis}%")

        filter_metode = safe_input("Filter metode pembayaran (kosongkan jika tidak): ").strip()
        if filter_metode:
            where_conditions.append("metode_pembayaran LIKE %s")
            params.append(f"%{filter_metode}%")

        sort_choice = safe_input("Sorting total_bayar? (asc/desc/kosongkan): ").strip().lower()
        order_clause = ""
        if sort_choice in ["asc", "desc"]:
            order_clause = f"total_bayar {sort_choice.upper()}"

        where_clause = " AND ".join(where_conditions)
        df = get_rental_dataframe(connection, where_clause, params, order_clause)

        if df.empty:
            print("Data tidak ditemukan.")
            return

        print("\nData Rental Mobil:")
        print(format_console_table(df))
    except Exception as err:
        print(f"Terjadi error saat menampilkan data: {err}")


# Fungsi untuk menambahkan 1 data rental baru dengan validasi lengkap
def add_data(connection):
    print("\n=== Tambah Data Rental ===")

    try:
        nama_pelanggan = get_non_empty_input("Nama pelanggan: ")
        jenis_mobil = get_non_empty_input("Jenis mobil: ")
        harga_per_hari = get_non_negative_int("Harga per hari: ")
        lama_sewa = get_non_negative_int("Lama sewa (hari): ")
        metode_pembayaran = get_non_empty_input("Metode pembayaran: ")
        tanggal_sewa = get_date_input("Tanggal sewa (YYYY-MM-DD): ")

        total_bayar = harga_per_hari * lama_sewa

        print("\n--- Konfirmasi Data ---")
        print(f"Nama Pelanggan    : {nama_pelanggan}")
        print(f"Jenis Mobil       : {jenis_mobil}")
        print(f"Harga per Hari    : {harga_per_hari}")
        print(f"Lama Sewa         : {lama_sewa}")
        print(f"Total Bayar       : {total_bayar}")
        print(f"Metode Pembayaran : {metode_pembayaran}")
        print(f"Tanggal Sewa      : {tanggal_sewa}")

        confirm = safe_input("Simpan data ini? (y/n): ").strip().lower()
        if confirm != "y":
            print("Insert dibatalkan.")
            return

        values = (
            nama_pelanggan,
            jenis_mobil,
            harga_per_hari,
            lama_sewa,
            total_bayar,
            metode_pembayaran,
            tanggal_sewa,
        )

        cursor = connection.cursor()
        cursor.execute(INSERT_RENTAL_MOBIL, values)
        connection.commit()
        print("Data rental berhasil ditambahkan.")
    except Error as err:
        print(f"Gagal menambah data ke database: {err}")
    except Exception as err:
        print(f"Terjadi error saat tambah data: {err}")


# Fungsi untuk menampilkan statistik rental menggunakan pandas dan numpy
def show_statistics(connection):
    print("\n=== Statistik Rental ===")
    try:
        df = get_rental_dataframe(connection)
        if df.empty:
            print("Belum ada data untuk dihitung statistik.")
            return

        total_transaksi = len(df)
        total_pendapatan = df["total_bayar"].sum()
        rata_rata_total = df["total_bayar"].mean()
        median_total = np.median(df["total_bayar"])
        mobil_tersering = df["jenis_mobil"].mode().iloc[0] if not df["jenis_mobil"].mode().empty else "-"
        rata_lama_sewa = df["lama_sewa"].mean()

        print(f"Total transaksi               : {total_transaksi}")
        print(f"Total pendapatan             : {total_pendapatan}")
        print(f"Rata-rata total bayar (mean) : {rata_rata_total:.2f}")
        print(f"Median total bayar (numpy)   : {median_total:.2f}")
        print(f"Mobil paling sering disewa   : {mobil_tersering}")
        print(f"Rata-rata lama sewa          : {rata_lama_sewa:.2f} hari")
    except Exception as err:
        print(f"Terjadi error saat hitung statistik: {err}")


# Fungsi untuk menampilkan visualisasi data rental dengan matplotlib
def show_visualization(connection):
    print("\n=== Visualisasi Data ===")
    try:
        df = get_rental_dataframe(connection)
        if df.empty:
            print("Belum ada data untuk divisualisasikan.")
            return
        #
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        # Pie chart untuk proporsi jenis mobil
        jenis_counts = df["jenis_mobil"].value_counts()
        axes[0].pie(jenis_counts.values, labels=jenis_counts.index, autopct="%1.1f%%", startangle=90)
        axes[0].set_title("Proporsi Jenis Mobil")

        # Bar chart untuk metode pembayaran
        metode_counts = df["metode_pembayaran"].value_counts()
        axes[1].bar(metode_counts.index, metode_counts.values)
        axes[1].set_title("Jumlah Transaksi per Metode Pembayaran")
        axes[1].set_xlabel("Metode Pembayaran")
        axes[1].set_ylabel("Jumlah Transaksi")
        axes[1].tick_params(axis="x", rotation=30)

        # Histogram untuk distribusi total bayar
        axes[2].hist(df["total_bayar"], bins=8)
        axes[2].set_title("Distribusi Total Bayar")
        axes[2].set_xlabel("Total Bayar")
        axes[2].set_ylabel("Frekuensi")

        plt.tight_layout()
        plt.show()
    except Exception as err:
        print(f"Terjadi error saat visualisasi: {err}")


def show_jenis_mobil(connection):
    print("\n=== Data Jenis Mobil ===")
    try:
        jenis_mobil_list = get_distinct_jenis_mobil(connection)
        if not jenis_mobil_list:
            print("Belum ada data jenis mobil.")
            return

        for index, jenis_mobil in enumerate(jenis_mobil_list, start=1):
            print(f"{index}. {jenis_mobil}")
    except Exception as err:
        print(f"Terjadi error saat menampilkan jenis mobil: {err}")


def show_metode_pembayaran(connection):
    print("\n=== Data Metode Pembayaran ===")
    try:
        metode_list = get_distinct_metode_pembayaran(connection)
        if not metode_list:
            print("Belum ada data metode pembayaran.")
            return

        for index, metode in enumerate(metode_list, start=1):
            print(f"{index}. {metode}")
    except Exception as err:
        print(f"Terjadi error saat menampilkan metode pembayaran: {err}")


# Fungsi untuk menampilkan menu utama dan menjalankan fitur-fitur utama
def show_main_menu(connection):
    while True:
        print("\n=== MENU UTAMA RENTAL MOBIL ===")
        print("1. Lihat Data Rental")
        print("2. Tambah Data Rental")
        print("3. Statistik Rental")
        print("4. Visualisasi Data")
        print("5. Lihat Data Jenis Mobil")
        print("6. Lihat Data Metode Pembayaran")
        print("7. Tambah Dummy Data (10)")
        print("8. Exit")

        choice = get_menu_choice("Pilih menu (1-8): ", {1, 2, 3, 4, 5, 6, 7, 8})

        if choice == 1:
            read_data(connection)
        elif choice == 2:
            add_data(connection)
        elif choice == 3:
            show_statistics(connection)
        elif choice == 4:
            show_visualization(connection)
        elif choice == 5:
            show_jenis_mobil(connection)
        elif choice == 6:
            show_metode_pembayaran(connection)
        elif choice == 7:
            confirm = safe_input("Tambahkan 10 data dummy sekarang? (y/n): ").strip().lower()
            if confirm == "y":
                insert_dummy_data(connection)
            else:
                print("Tambah dummy data dibatalkan.")
        elif choice == 8:
            print("Keluar dari menu utama.")
            break
