import pandas as pd
from queries import (
    CREATE_TABLE_RENTAL_MOBIL,
    DUMMY_RENTAL_DATA,
    INSERT_RENTAL_MOBIL,
    SELECT_RENTAL_MOBIL_BASE,
    SHOW_DATABASES_LIKE,
    SHOW_TABLES_LIKE,
    build_create_database_query,
)

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    mysql = None
    Error = Exception


# Fungsi untuk membuat koneksi ke MySQL (dengan/ tanpa memilih database)
def connect_database(config, use_database=True):
    if mysql is None:
        print("mysql-connector-python belum terpasang. Install dulu: pip install mysql-connector-python")
        return None

    try:
        host = str(config.get("host", "")).strip()
        user = str(config.get("user", "")).strip()
        password = config.get("password", "")
        database_name = str(config.get("database", "")).strip()

        if not host or not user:
            print("Koneksi database gagal: host dan user MySQL tidak boleh kosong.")
            return None

        if use_database and not database_name:
            print("Koneksi database gagal: nama database tidak boleh kosong.")
            return None

        connection_params = {
            "host": host,
            "user": user,
            "password": password,
        }

        if use_database:
            connection_params["database"] = database_name

        connection = mysql.connector.connect(**connection_params)
        if connection.is_connected():
            return connection
        return None
    except Error as err:
        print(f"Koneksi database gagal: {err}")
        return None
    except Exception as err:
        print(f"Terjadi error saat koneksi: {err}")
        return None


# Fungsi untuk mengetes koneksi MySQL tanpa memilih database
def test_connection(config):
    connection = connect_database(config, use_database=False)
    if connection is None:
        print("Test connection gagal.")
        return False

    try:
        print("Test connection berhasil ke MySQL server.")
        return True
    except Exception as err:
        print(f"Terjadi error saat test connection: {err}")
        return False
    finally:
        try:
            if connection.is_connected():
                connection.close()
        except Exception:
            pass


# Fungsi untuk mengecek apakah database ada di MySQL server
def is_database_exists(config):
    database_name = str(config.get("database", "")).strip()
    if not database_name:
        print("Nama database kosong, tidak bisa cek database.")
        return False

    connection = connect_database(config, use_database=False)
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute(SHOW_DATABASES_LIKE, (database_name,))
        result = cursor.fetchone()
        return result is not None
    except Error as err:
        print(f"Gagal mengecek database: {err}")
        return False
    except Exception as err:
        print(f"Terjadi error saat mengecek database: {err}")
        return False
    finally:
        try:
            if connection.is_connected():
                connection.close()
        except Exception:
            pass


# Fungsi untuk membuat database rental_mobil_db jika belum ada
def create_database(config):
    database_name = str(config.get("database", "")).strip()
    if not database_name:
        print("Gagal membuat database: nama database tidak boleh kosong.")
        return False

    connection = connect_database(config, use_database=False)
    if connection is None:
        print("Gagal terhubung ke MySQL server. Database belum dibuat.")
        return False

    try:
        cursor = connection.cursor()
        query = build_create_database_query(database_name)
        cursor.execute(query)
        connection.commit()
        print(f"Database '{database_name}' siap digunakan.")
        return True
    except Error as err:
        print(f"Gagal membuat database: {err}")
        return False
    except Exception as err:
        print(f"Terjadi error saat membuat database: {err}")
        return False
    finally:
        try:
            if connection.is_connected():
                connection.close()
        except Exception:
            pass


# Fungsi untuk membuat tabel rental_mobil sesuai requirement
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_TABLE_RENTAL_MOBIL)
        connection.commit()
        print("Table 'rental_mobil' berhasil dibuat / sudah tersedia.")
        return True
    except Error as err:
        print(f"Gagal membuat table: {err}")
        return False
    except Exception as err:
        print(f"Terjadi error saat membuat table: {err}")
        return False


# Fungsi untuk mengecek apakah tabel rental_mobil sudah ada di database
def is_table_exists(connection, table_name="rental_mobil"):
    try:
        cursor = connection.cursor()
        cursor.execute(SHOW_TABLES_LIKE, (table_name,))
        result = cursor.fetchone()
        return result is not None
    except Error as err:
        print(f"Gagal mengecek table: {err}")
        return False
    except Exception as err:
        print(f"Terjadi error saat mengecek table: {err}")
        return False


# Fungsi untuk mengisi data dummy minimal 10 record ke tabel rental_mobil
def insert_dummy_data(connection):
    try:
        cursor = connection.cursor()
        cursor.executemany(INSERT_RENTAL_MOBIL, DUMMY_RENTAL_DATA)
        connection.commit()
        print(f"Berhasil insert {cursor.rowcount} data dummy.")
        return True
    except Error as err:
        print(f"Gagal insert dummy data: {err}")
        return False
    except Exception as err:
        print(f"Terjadi error saat insert dummy data: {err}")
        return False


# Fungsi untuk mengambil data rental_mobil ke dalam DataFrame pandas
def get_rental_dataframe(connection, where_clause="", params=None, order_clause=""):
    if params is None:
        params = []

    query = SELECT_RENTAL_MOBIL_BASE

    if where_clause:
        query += f" WHERE {where_clause}"

    if order_clause:
        query += f" ORDER BY {order_clause}"

    try:
        df = pd.read_sql(query, connection, params=params)
        return df
    except Exception as err:
        print(f"Gagal membaca data: {err}")
        return pd.DataFrame()
