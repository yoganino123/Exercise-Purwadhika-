data = [9100000, 9800000, 9500000, 10300000, 9300000]

# Input batas minimum
value_lebih_dari = 9500000

def filter_lebih_dari(x):
    return x >= value_lebih_dari

hasil = list(filter(filter_lebih_dari, data))

print("Hasil filter:", hasil)
