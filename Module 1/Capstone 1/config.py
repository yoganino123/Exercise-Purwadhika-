import os


ENV_FILE_PATH = os.path.join(os.path.dirname(__file__), ".env")

DEFAULT_DB_CONFIG = {
    "host": "",
    "user": "",
    "password": "",
    "database": "rental_mobil_db",
}


def _parse_env_file(file_path):
    data = {}
    if not os.path.exists(file_path):
        return data

    with open(file_path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]

            data[key] = value

    return data


def _write_env_file(file_path, config):
    content = (
        "# Konfigurasi database (auto-generated)\n"
        f"DB_HOST={config.get('host', '')}\n"
        f"DB_USER={config.get('user', '')}\n"
        f"DB_PASSWORD={config.get('password', '')}\n"
        f"DB_DATABASE={config.get('database', '')}\n"
    )

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def ensure_env_file(file_path=ENV_FILE_PATH):
    if os.path.exists(file_path):
        return
    _write_env_file(file_path, DEFAULT_DB_CONFIG)


def load_db_config(file_path=ENV_FILE_PATH):
    ensure_env_file(file_path)
    env_values = _parse_env_file(file_path)

    return {
        "host": os.getenv("DB_HOST", env_values.get("DB_HOST", DEFAULT_DB_CONFIG["host"])),
        "user": os.getenv("DB_USER", env_values.get("DB_USER", DEFAULT_DB_CONFIG["user"])),
        "password": os.getenv("DB_PASSWORD", env_values.get("DB_PASSWORD", DEFAULT_DB_CONFIG["password"])),
        "database": os.getenv("DB_DATABASE", env_values.get("DB_DATABASE", DEFAULT_DB_CONFIG["database"])),
    }


DB_CONFIG = load_db_config()
