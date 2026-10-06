from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. MEMBACA GAMBAR
# ============================================================

gambar = Image.open(
     "images/Fig0340(a)(dipxe_text).tif"
).convert("L")

citra = np.array(
    gambar,
    dtype=np.int32
)

tinggi, lebar = citra.shape

print("Ukuran gambar :", citra.shape)


# ============================================================
# 2. MEMBUAT BLURRED IMAGE
#
#    Mean Filter 3 x 3 secara manual
# ============================================================

blur = citra.copy()


for y in range(1, tinggi - 1):

    for x in range(1, lebar - 1):

        jumlah = 0

        for j in range(-1, 2):

            for i in range(-1, 2):

                jumlah += int(
                    citra[y + j, x + i]
                )

        blur[y, x] = int(
            jumlah / 9 + 0.5
        )


# ============================================================
# 3. MEMBUAT UNSHARP MASK
#
#    mask = original - blurred
# ============================================================

mask = np.zeros(
    (tinggi, lebar),
    dtype=np.int32
)


for y in range(tinggi):

    for x in range(lebar):

        mask[y, x] = (
            citra[y, x]
            - blur[y, x]
        )


# ============================================================
# 4. MENAMBAHKAN MASK KE ORIGINAL
#
#    sharpened = original + mask
# ============================================================

hasil = np.zeros(
    (tinggi, lebar),
    dtype=np.uint8
)


for y in range(tinggi):

    for x in range(lebar):

        nilai = (
            citra[y, x]
            + mask[y, x]
        )

        # Clipping manual

        if nilai < 0:
            nilai = 0

        if nilai > 255:
            nilai = 255

        hasil[y, x] = nilai


# ============================================================
# 5. RESCALING MASK UNTUK DISPLAY
# ============================================================

nilai_min = mask[0, 0]
nilai_max = mask[0, 0]


for y in range(tinggi):

    for x in range(lebar):

        if mask[y, x] < nilai_min:
            nilai_min = mask[y, x]

        if mask[y, x] > nilai_max:
            nilai_max = mask[y, x]


mask_display = np.zeros(
    (tinggi, lebar),
    dtype=np.uint8
)


for y in range(tinggi):

    for x in range(lebar):

        if nilai_max != nilai_min:

            nilai = (
                (mask[y, x] - nilai_min)
                / (nilai_max - nilai_min)
            ) * 255

        else:

            nilai = 0

        mask_display[y, x] = int(
            nilai + 0.5
        )


# ============================================================
# 6. MENYIMPAN HASIL
# ============================================================

Image.fromarray(
    blur.astype(np.uint8)
).save(
    "output/07_unsharp_blurred_result.tif"
)

Image.fromarray(
    mask_display
).save(
    "output/07_unsharp_mask_result.tif"
)

Image.fromarray(
    hasil
).save(
    "output/07_unsharp_sharpened_result.tif"
)


# ============================================================
# 7. MENAMPILKAN HASIL
# ============================================================

plt.figure(figsize=(15, 8))


plt.subplot(2, 2, 1)

plt.imshow(
    citra,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Original Image")
plt.axis("off")


plt.subplot(2, 2, 2)

plt.imshow(
    blur,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Blurred Image")
plt.axis("off")


plt.subplot(2, 2, 3)

plt.imshow(
    mask_display,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Unsharp Mask")
plt.axis("off")


plt.subplot(2, 2, 4)

plt.imshow(
    hasil,
    cmap="gray",
    vmin=0,
    vmax=255
)

plt.title("Sharpened Image")
plt.axis("off")


plt.tight_layout()
plt.show()