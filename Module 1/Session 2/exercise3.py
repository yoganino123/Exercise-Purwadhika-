# Harga buah
harga_apel = 10000
harga_jeruk = 15000
harga_anggur = 20000

# Input jumlah buah
apel = int(input("Masukkan Jumlah Apel: "))
jeruk = int(input("Masukkan Jumlah Jeruk: "))
anggur = int(input("Masukkan Jumlah Anggur: "))

# Hitung detail belanja
total_apel = apel * harga_apel
total_jeruk = jeruk * harga_jeruk
total_anggur = anggur * harga_anggur

total = total_apel + total_jeruk + total_anggur

print("\nDetail Belanja")
print(f"Apel  : {apel} x {harga_apel} = {total_apel}")
print(f"Jeruk : {jeruk} x {harga_jeruk} = {total_jeruk}")
print(f"Anggur: {anggur} x {harga_anggur} = {total_anggur}")

print(f"\nTotal : {total}")

# Input uang pembayaran
uang = int(input("\nMasukkan jumlah uang: "))

# Kondisi pembayaran
if uang < total:
    kurang = total - uang
    print("Transaksi anda dibatalkan")
    print(f"Uang anda kurang sebesar {kurang}")

elif uang == total:
    print("Terima kasih")

else:
    kembali = uang - total
    print("Terima kasih")
    print(f"Uang kembali anda : {kembali}")
