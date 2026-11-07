import cv2
import matplotlib.pyplot as plt
import math

# Membaca gambar
img = cv2.imread("Bleach.jpg")

if img is None:
    raise FileNotFoundError(
        "Gambar 'kp.jpg' tidak ditemukan. Pastikan file gambar berada "
        "di folder yang sama dengan program ini."
    )

# Mengubah format warna BGR menjadi RGB untuk ditampilkan dengan Matplotlib
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

tinggi, lebar = img.shape[:2]


def lakukan_rotasi(gambar, sudut):
    """Memutar gambar sesuai sudut dan menjaga seluruh gambar tetap terlihat."""
    tinggi_asli, lebar_asli = gambar.shape[:2]
    pusat = (lebar_asli / 2, tinggi_asli / 2)

    # Membuat matriks rotasi
    M = cv2.getRotationMatrix2D(pusat, sudut, 1.0)

    # Menghitung ukuran kanvas baru agar gambar tidak terpotong
    cos_sudut = abs(M[0, 0])
    sin_sudut = abs(M[0, 1])
    lebar_baru = int((tinggi_asli * sin_sudut) + (lebar_asli * cos_sudut))
    tinggi_baru = int((tinggi_asli * cos_sudut) + (lebar_asli * sin_sudut))

    # Menggeser titik pusat ke tengah kanvas baru
    M[0, 2] += (lebar_baru / 2) - pusat[0]
    M[1, 2] += (tinggi_baru / 2) - pusat[1]

    hasil = cv2.warpAffine(gambar, M, (lebar_baru, tinggi_baru))
    return hasil


# Melakukan rotasi 45, 90, dan 180 derajat
sudut_rotasi = [45, 90, 180]
hasil_rotasi = {}

for sudut in sudut_rotasi:
    hasil = lakukan_rotasi(img, sudut)
    hasil_rotasi[sudut] = hasil

    # Menyimpan hasil rotasi
    nama_output = f"hasil_rotasi_{sudut}.jpg"
    hasil_bgr = cv2.cvtColor(hasil, cv2.COLOR_RGB2BGR)
    cv2.imwrite(nama_output, hasil_bgr)
    print(f"Hasil rotasi {sudut} derajat disimpan sebagai {nama_output}")

# Menampilkan citra asli dan seluruh hasil rotasi
plt.figure(figsize=(14, 9))

plt.subplot(2, 2, 1)
plt.imshow(img)
plt.title("Citra Asli")
plt.axis("off")

for nomor, sudut in enumerate(sudut_rotasi, start=2):
    plt.subplot(2, 2, nomor)
    plt.imshow(hasil_rotasi[sudut])
    plt.title(f"Rotasi {sudut} Derajat")
    plt.axis("off")

plt.tight_layout()
plt.show()
