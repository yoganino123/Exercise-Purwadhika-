def input_film(pesan):
    while True:
        data = input(pesan)
        film = data.split(",")
        # Eror handling
        if len(film) < 5:
            print("❌ Error: Jumlah film kurang dari 5. Silakan masukkan tepat 5 film.\n")
        elif len(film) > 5:
            print("❌ Error: Jumlah film lebih dari 5. Silakan masukkan tepat 5 film.\n")
        else:
            return [f.strip().lower() for f in film]


# Input dengan function validasi
film_kamu = input_film(
    "Masukkan 5 Film Kesukaan anda dipisahkan dengan koma : "
)

film_teman = input_film(
    "Masukkan 5 Film Kesukaan teman anda dipisahkan dengan koma : "
)

# Cari film yang sama
film_sama = set(film_kamu) & set(film_teman)

# Hitung persentase
persentase = (len(film_sama) / 5) * 100

# Output
print(f"\nKesukaan Film kalian yang sama sebesar {persentase:.1f}%")
