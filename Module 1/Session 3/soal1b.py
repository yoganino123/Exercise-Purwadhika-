n = 5

# Bagian atas
for i in range(1, n + 1):
    print("  " * (n - i) + "* " * (2 * i - 1))

# Bagian bawah
for i in range(n - 1, 0, -1):
    print("  " * (n - i) + "* " * (2 * i - 1))
