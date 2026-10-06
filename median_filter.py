from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# FUNGSI PENGURUTAN MANUAL
# ============================================================

def urutkan_manual(data):

    hasil_urut = data.copy()

    panjang = len(hasil_urut)

    # Insertion Sort
    for i in range(1, panjang):

        nilai = hasil_urut[i]

        j = i - 1

        while j >= 0 and hasil_urut[j] > nilai:

            hasil_urut[j + 1] = hasil_urut[j]

            j -= 1

        hasil_urut[j + 1] = nilai

    return hasil_urut


# ============================================================
# MEDIAN FILTER MANUAL
# ============================================================

def median_filter_manual(citra, ukuran_mask):

    tinggi, lebar = citra.shape

    hasil = citra.copy()

    radius = ukuran_mask // 2

    for y in range(radius, tinggi - radius):

        for x in range(radius, lebar - radius):

            neighborhood = []

            # Mengambil piksel neighborhood
            for j in range(-radius, radius + 1):

                for i in range(-radius, radius + 1):

                    neighborhood.append(
                        int(citra[y + j, x + i])
                    )

            # Mengurutkan secara manual
            neighborhood = urutkan_manual(
                neighborhood
            )

            # Mengambil nilai tengah
            posisi_tengah = len(neighborhood) // 2

            hasil[y, x] = neighborhood[posisi_tengah]

    return hasil


# ============================================================
# 1. MEMBACA GAMBAR
# ============================================================

gambar = Image.open(
     "images/Fig0335(a)(ckt_board_saltpep_prob_pt05).tif"
).convert("L")

citra = np.array(gambar)

print("Ukuran gambar :", citra.shape)


# ============================================================
# 2. MEDIAN FILTER 3 x 3
# ============================================================

hasil_3x3 = median_filter_manual(
    citra,
    3
)


# ============================================================
# 3. MEDIAN FILTER 5 x 5
# ============================================================

hasil_5x5 = median_filter_manual(
    citra,
    5
)


# ============================================================
# 4. MENYIMPAN HASIL
# ============================================================

Image.fromarray(hasil_3x3).save(
    "output/05_median_filter_3x3_result.tif"
)

Image.fromarray(hasil_5x5).save(
    "output/05_median_filter_5x5_result.tif"
)


# ============================================================
# 5. MENAMPILKAN HASIL
# ============================================================

plt.figure(figsize=(15, 5))


plt.subplot(1, 3, 1)

plt.imshow(
    citra,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Original Image")
plt.axis("off")


plt.subplot(1, 3, 2)

plt.imshow(
    hasil_3x3,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Median Filter 3x3")
plt.axis("off")


plt.subplot(1, 3, 3)

plt.imshow(
    hasil_5x5,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Median Filter 5x5")
plt.axis("off")


plt.tight_layout()
plt.show()