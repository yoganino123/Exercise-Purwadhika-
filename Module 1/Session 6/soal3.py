# Data buah
buah = {
    "Apel": {
        "stok": 5,
        "harga": 10000
        },
    "Jeruk": {
        "stok": 7,
        "harga": 15000
        },
    "Anggur": {
        "stok": 6,
        "harga": 20000
        }
}


def input_belanja(data_buah):
    belanja = {}
    print("=== Proses Menentukan Jumlah Buah ===")

    for nama, data in data_buah.items():
        while True:
            try:
                jumlah = int(input(f"Masukkan Jumlah {nama} : "))

                if jumlah > data["stok"]:
                    print("Jumlah yang dimasukkan terlalu banyak")
                    print(f"Stock {nama} tinggal : {data['stok']}")
                elif jumlah < 0:
                    print("Jumlah tidak boleh negatif")
                else:
                    belanja[nama] = jumlah
                    break

            except ValueError:
                print("Input harus berupa angka!")

    return belanja


def hitung_total(data_buah, belanja):
    print("\nDetail Belanja")
    total = 0

    for nama, jumlah in belanja.items():
        harga = data_buah[nama]["harga"]
        subtotal = jumlah * harga
        total += subtotal
        print(f"{nama} : {jumlah} x {harga} = {subtotal}")

    print(f"Total : {total}")
    return total


def proses_bayar(total):
    print("\n=== Proses Bayar ===")

    while True:
        try:
            uang = int(input("Masukkan jumlah uang : "))

            if uang < total:
                print(f"Uang anda kurang sebesar {total - uang}")
            else:
                print("Terima kasih")
                print(f"Uang kembali anda : {uang - total}")
                break

        except ValueError:
            print("Input harus berupa angka!")


def main():
    belanja = input_belanja(buah)
    total = hitung_total(buah, belanja)
    proses_bayar(total)


# Jalankan program
main()
