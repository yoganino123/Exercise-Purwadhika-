from config import DB_CONFIG
from database import (
    connect_database,
    create_database,
    create_table,
    insert_dummy_data,
    is_database_exists,
    is_table_exists,
    test_connection,
)
from features import show_main_menu
from utils import get_menu_choice, input_db_credentials


# Fungsi untuk alur startup sesuai requirement (koneksi, setup DB/table, lalu masuk menu utama)
def start_application():
    while True:
        server_connection = connect_database(DB_CONFIG, use_database=False)

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

        connection = connect_database(DB_CONFIG, use_database=True)
        if connection is None:
            print("\n=== Koneksi Database Gagal ===")
            continue

        try:
            print("\n=== Aplikasi Rental Mobil ===")
            if not is_table_exists(connection, "rental_mobil"):
                print("\n=== Table rental_mobil belum ada ===")
                print("1. Create Table")
                print("2. Insert Dummy Data")
                print("3. Exit")

                choice = get_menu_choice("Pilih menu (1-3): ", {1, 2, 3})

                if choice == 1:
                    create_table(connection)
                elif choice == 2:
                    created = create_table(connection)
                    if created:
                        insert_dummy_data(connection)
                elif choice == 3:
                    print("Program selesai.")
                    break
            else:
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


# Blok utama program
if __name__ == "__main__":
    start_application()
