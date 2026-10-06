from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. MEMBACA GAMBAR
# ============================================================

gambar = Image.open(
    "images/Fig0338(a)(blurry_moon).tif"
).convert("L")

citra = np.array(
    gambar,
    dtype=np.int32
)

tinggi, lebar = citra.shape

print("Ukuran gambar :", citra.shape)


# ============================================================
# 2. MASK LAPLACIAN
# ============================================================

mask = [
    [0,  1, 0],
    [1, -4, 1],
    [0,  1, 0]
]


# ============================================================
# 3. ARRAY LAPLACIAN
# ============================================================

laplacian = np.zeros(
    (tinggi, lebar),
    dtype=np.int32
)


# ============================================================
# 4. LAPLACIAN FILTER SECARA MANUAL
# ============================================================

for y in range(1, tinggi - 1):

    for x in range(1, lebar - 1):

        jumlah = 0

        for j in range(-1, 2):

            for i in range(-1, 2):

                piksel = int(
                    citra[y + j, x + i]
                )

                koefisien = mask[j + 1][i + 1]

                jumlah += (
                    piksel * koefisien
                )

        laplacian[y, x] = jumlah


# ============================================================
# 5. IMAGE ENHANCEMENT
#
#    Karena center mask = -4:
#
#    g = f - Laplacian
# ============================================================

hasil = np.zeros(
    (tinggi, lebar),
    dtype=np.uint8
)


for y in range(tinggi):

    for x in range(lebar):

        nilai = (
            int(citra[y, x])
            - int(laplacian[y, x])
        )

        # Clipping manual

        if nilai < 0:
            nilai = 0

        if nilai > 255:
            nilai = 255

        hasil[y, x] = nilai


# ============================================================
# 6. RESCALING LAPLACIAN UNTUK DISPLAY
# ============================================================

nilai_min = laplacian[0, 0]
nilai_max = laplacian[0, 0]


for y in range(tinggi):

    for x in range(lebar):

        nilai = laplacian[y, x]

        if nilai < nilai_min:
            nilai_min = nilai

        if nilai > nilai_max:
            nilai_max = nilai


laplacian_display = np.zeros(
    (tinggi, lebar),
    dtype=np.uint8
)


for y in range(tinggi):

    for x in range(lebar):

        if nilai_max != nilai_min:

            nilai = (
                (laplacian[y, x] - nilai_min)
                / (nilai_max - nilai_min)
            ) * 255

        else:

            nilai = 0

        laplacian_display[y, x] = int(
            nilai + 0.5
        )


# ============================================================
# 7. MENYIMPAN HASIL
# ============================================================

Image.fromarray(
    laplacian_display
).save(
    "output/06_laplacian_filter_result.tif"
)

Image.fromarray(
    hasil
).save(
    "output/06_laplacian_enhancement_result.tif"
)


# ============================================================
# 8. MENAMPILKAN HASIL
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
    laplacian_display,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Laplacian Filter")
plt.axis("off")


plt.subplot(1, 3, 3)

plt.imshow(
    hasil,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Laplacian Enhancement")
plt.axis("off")


plt.tight_layout()
plt.show()