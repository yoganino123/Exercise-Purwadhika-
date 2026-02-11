def cek_ganjil_genap(angka):
    if angka % 2 == 0:
        return "Genap"
    else:
        return "Ganjil"

# Contoh data
data1 = [1, 3, 4, 5]
data2 = [22, 17, 19, 20, 14]
data3 = [1, 3, 5]
data4 = [2, 4, 6]

# Menggunakan map
hasil1 = list(map(cek_ganjil_genap, data1))
hasil2 = list(map(cek_ganjil_genap, data2))
hasil3 = list(map(cek_ganjil_genap, data3))
hasil4 = list(map(cek_ganjil_genap, data4))

print(hasil1)
print(hasil2)
print(hasil3)
print(hasil4)
