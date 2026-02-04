def cek_ganjil_genap(angka):
    if angka % 2 == 0:
        return f"Angka {angka} tergolong bilangan GENAP!"
    else:
        return f"Angka {angka} tergolong bilangan GANJIL!"

angka = int(input("Masukkan angka: "))
print(cek_ganjil_genap(angka))
