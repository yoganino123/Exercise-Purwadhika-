from config import DB_CONFIG
from database import (
    connect_database,
    create_database,
    create_table,
    is_database_exists,
    is_table_exists,
    test_connection,
)
from features import show_main_menu
from utils import get_menu_choice, input_db_credentials


# Fungsi untuk cek database  (koneksi, setup DB/table, lalu masuk menu utama)
def start_application():
    while True:
        # Cek koneksi database
        try:
            server_connection = connect_database(DB_CONFIG, use_database=False)
        except Exception as err:
            print(f"Koneksi database gagal: {err}")
            server_connection = None

        if server_connection is None:
            print("\n=== Koneksi Database Gagal ===")
            print("1. Masukkan Credential MySQL")
            print("2. Test Connection")
            print("3. Kembali ke Menu Utama")
            print("4. Exit")
            choice = get_menu_choice("Pilih menu (1-4): ", {1, 2, 3, 4})

            if choice == 1:
                input_db_credentials(DB_CONFIG)
            elif choice == 2:
                test_connection(DB_CONFIG)
            elif choice == 3:
                continue
            elif choice == 4:
                print("Program selesai.")
                break
            continue
        # Jika koneksi server berhasil, lanjut cek database dan table
        try:
            if server_connection.is_connected():
                server_connection.close()
        except Exception:
            pass

        database_name = str(DB_CONFIG.get("database", "")).strip()
        if not is_database_exists(DB_CONFIG):
            print("\n=== Database Tidak Ada ===")
            print(f"1. Create Database {database_name}")
            print(f"2. Test Apakah ada Database {database_name}")
            print("3. Kembali ke Menu Utama")
            print("4. Exit")
            choice = get_menu_choice("Pilih menu (1-4): ", {1, 2, 3, 4})

            if choice == 1:
                create_database(DB_CONFIG)
            elif choice == 2:
                if is_database_exists(DB_CONFIG):
                    print(f"Database {database_name} ditemukan.")
                else:
                    print(f"Database {database_name} belum ada.")
            elif choice == 3:
                continue
            elif choice == 4:
                print("Program selesai.")
                break
            continue

        try:
            connection = connect_database(DB_CONFIG, use_database=True)
        except Exception as err:
            print(f"Koneksi database gagal: {err}")
            connection = None

        if connection is None:
            print("\n=== Koneksi Database Gagal ===")
            continue
        # Jika koneksi database berhasil, lanjut cek table rental_mobil
        try:
            print("\n=== Aplikasi Rental Mobil ===")
            if not is_table_exists(connection, "rental_mobil"):
                print("\n=== Table rental_mobil belum ada ===")
                print("1. Create Table")
                print("2. Exit")

                choice = get_menu_choice("Pilih menu (1-2): ", {1, 2})

                if choice == 1:
                    create_table(connection)
                elif choice == 2:
                    print("Program selesai.")
                    break
            else:
                # Jika table sudah ada, langsung masuk menu utama
                show_main_menu(connection)
                print("Program selesai.")
                break
        finally:
            try:
                if connection.is_connected():
                    connection.close()
                    print("Koneksi database ditutup.")
            except Exception:
                pass


# main
# fungsi if __name__ == "__main__" untuk memastikan start_application() hanya dijalankan saat app.py dieksekusi langsung, bukan saat diimport sebagai modul
if __name__ == "__main__":
    start_application()
