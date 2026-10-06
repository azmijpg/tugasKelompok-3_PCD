from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. MEMBACA GAMBAR
# ============================================================

gambar = Image.open(
    "images/Fig0334(a)(hubble-original).tif"
).convert("L")

citra = np.array(gambar)

tinggi, lebar = citra.shape

print("Ukuran gambar :", citra.shape)


# ============================================================
# 2. MEMBUAT ARRAY HASIL
# ============================================================

hasil = citra.copy()


# ============================================================
# 3. MEAN FILTER 3 x 3 SECARA MANUAL
# ============================================================

for y in range(1, tinggi - 1):

    for x in range(1, lebar - 1):

        jumlah = 0

        # Neighborhood 3 x 3
        for j in range(-1, 2):

            for i in range(-1, 2):

                jumlah += int(
                    citra[y + j, x + i]
                )

        # Rata-rata 9 piksel
        rata_rata = jumlah / 9

        hasil[y, x] = int(rata_rata + 0.5)


# ============================================================
# 4. MENYIMPAN HASIL
# ============================================================

Image.fromarray(hasil).save(
    "output/04_mean_filter_result.tif"
)


# ============================================================
# 5. MENAMPILKAN HASIL
# ============================================================

plt.figure(figsize=(10, 5))


plt.subplot(1, 2, 1)

plt.imshow(
    citra,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Original Image")
plt.axis("off")


plt.subplot(1, 2, 2)

plt.imshow(
    hasil,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Mean Filter 3x3")
plt.axis("off")


plt.tight_layout()
plt.show()