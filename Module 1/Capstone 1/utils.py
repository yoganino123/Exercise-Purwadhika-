import os
from datetime import datetime


# Fungsi untuk membersihkan layar terminal (opsional)
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Fungsi wrapper input agar tidak crash saat terjadi error input dari user
def safe_input(prompt):
    while True:
        try:
            return input(prompt)
        except Exception as err:
            print(f"Input error: {err}. Silakan coba lagi.")


# Fungsi untuk membaca pilihan menu integer dengan validasi rentang nilai
def get_menu_choice(prompt, valid_choices):
    while True:
        try:
            raw = safe_input(prompt).strip()
            choice = int(raw)
            if choice in valid_choices:
                return choice
            print(f"Pilihan harus salah satu dari: {sorted(valid_choices)}")
        except ValueError:
            print("Input harus berupa angka yang valid.")
        except Exception as err:
            print(f"Terjadi kesalahan input: {err}")


# Fungsi untuk input teks yang tidak boleh kosong
def get_non_empty_input(prompt):
    while True:
        try:
            value = safe_input(prompt).strip()
            if value:
                return value
            print("Input tidak boleh kosong.")
        except Exception as err:
            print(f"Terjadi kesalahan input: {err}")


# Fungsi untuk input angka integer non-negatif
def get_non_negative_int(prompt):
    while True:
        try:
            raw = safe_input(prompt).strip()
            value = int(raw)
            if value < 0:
                print("Nilai tidak boleh negatif.")
                continue
            return value
        except ValueError:
            print("Input harus angka bulat.")
        except Exception as err:
            print(f"Terjadi kesalahan input: {err}")


# Fungsi untuk input tanggal format YYYY-MM-DD
def get_date_input(prompt):
    while True:
        try:
            raw = safe_input(prompt).strip()
            parsed = datetime.strptime(raw, "%Y-%m-%d")
            return parsed.date()
        except ValueError:
            print("Format tanggal salah. Gunakan format YYYY-MM-DD.")
        except Exception as err:
            print(f"Terjadi kesalahan input: {err}")


# Fungsi untuk memperbarui credential MySQL dari input user
def input_db_credentials(config):
    print("\n=== Input Credential MySQL ===")
    host = get_non_empty_input("Host (contoh: localhost): ")
    user = get_non_empty_input("User: ")
    password = safe_input("Password (boleh kosong): ")

    config["host"] = host
    config["user"] = user
    config["password"] = password

    if save_db_config_to_file(config):
        print("Credential berhasil diperbarui dan disimpan ke config.py.")
    else:
        print("Credential berhasil diperbarui (runtime), tapi gagal disimpan ke file.")


# Fungsi untuk menyimpan DB_CONFIG terbaru ke file config.py
def save_db_config_to_file(config, config_file_path=None):
    try:
        if config_file_path is None:
            config_file_path = os.path.join(os.path.dirname(__file__), "config.py")

        host = str(config.get("host", ""))
        user = str(config.get("user", ""))
        password = str(config.get("password", ""))
        database = str(config.get("database", ""))

        content = (
            "# Konfigurasi default database MySQL (bisa diubah lewat menu input credential)\n"
            "DB_CONFIG = {\n"
            f"    \"host\": {host!r},\n"
            f"    \"user\": {user!r},\n"
            f"    \"password\": {password!r},\n"
            f"    \"database\": {database!r},\n"
            "}\n"
        )

        with open(config_file_path, "w", encoding="utf-8") as file:
            file.write(content)

        return True
    except Exception as err:
        print(f"Gagal menyimpan credential ke file config.py: {err}")
        return False
