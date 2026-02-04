# IMT = massa (kg) / tinggi (m)^2
massa = float(input("Masukkan Massa (kg): "))
tinggi_cm = float(input("Masukkan Tinggi (cm): "))

# Konversi cm ke meter
tinggi_m = tinggi_cm / 100

# Hitung IMT
imt = massa / (tinggi_m ** 2)

# Kategori IMT
if imt < 18.5:
    kategori = "BERAT BADAN KURANG!"
elif 18.5 <= imt <= 24.9:
    kategori = "BERAT BADAN IDEAL!"
elif 25.0 <= imt <= 29.9:
    kategori = "BERAT BADAN BERLEBIH!"
elif 30.0 <= imt <= 39.9:
    kategori = "BERAT BADAN SANGAT BERLEBIH!"
else:
    kategori = "OBESITAS!"

print(f"Massa {massa} kg dan tinggi {tinggi_m} m")
print(f"IMT = {imt}, {kategori}")
