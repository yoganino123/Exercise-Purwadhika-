import os
from datetime import datetime

from config import ensure_env_file


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


# Fungsi untuk memperbarui credential MySQL dari input user
def input_db_credentials(config):
    print("\n=== Input Credential MySQL ===")
    host = get_non_empty_input("Host (contoh: localhost): ")
    user = get_non_empty_input("User: ")
    password = safe_input("Password (boleh kosong): ")

    config["host"] = host
    config["user"] = user
    config["password"] = password

    if save_db_config_to_env(config):
        print("Credential berhasil diperbarui dan disimpan ke .env.")
    else:
        print("Credential berhasil diperbarui (runtime), tapi gagal disimpan ke .env.")


# Fungsi untuk menyimpan DB_CONFIG terbaru ke file .env
def save_db_config_to_env(config, env_file_path=None):
    try:
        if env_file_path is None:
            env_file_path = os.path.join(os.path.dirname(__file__), ".env")

        ensure_env_file(env_file_path)

        host = str(config.get("host", ""))
        user = str(config.get("user", ""))
        password = str(config.get("password", ""))
        database = str(config.get("database", "rental_mobil_db"))

        content = (
            "# Konfigurasi database (auto-generated)\n"
            f"DB_HOST={host}\n"
            f"DB_USER={user}\n"
            f"DB_PASSWORD={password}\n"
            f"DB_DATABASE={database}\n"
        )

        with open(env_file_path, "w", encoding="utf-8") as file:
            file.write(content)

        return True
    except Exception as err:
        print(f"Gagal menyimpan credential ke file .env: {err}")
        return False
