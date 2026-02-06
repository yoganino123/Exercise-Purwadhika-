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

belanja = {}

print("=== Proses Menentukan Jumlah Buah ===")

# Input jumlah buah dengan validasi stok
for nama, data in buah.items():
    while True:
        jumlah = int(input(f"Masukkan Jumlah {nama} : "))

        if jumlah > data["stok"]:
            print("Jumlah yang dimasukkan terlalu banyak")
            print(f"Stock {nama} tinggal : {data['stok']}")
        else:
            belanja[nama] = jumlah
            break

# Detail belanja
print("\nDetail Belanja")
total = 0

for nama, jumlah in belanja.items():
    harga = buah[nama]["harga"]
    subtotal = jumlah * harga
    total += subtotal
    print(f"{nama} : {jumlah} x {harga} = {subtotal}")

print(f"Total : {total}")

# Proses bayar
print("\n=== Proses Bayar ===")
while True:
    uang = int(input("Masukkan jumlah uang : "))

    if uang < total:
        print(f"Uang anda kurang sebesar {total - uang}")
    else:
        print("Terima kasih")
        print(f"Uang kembali anda : {uang - total}")
        break
