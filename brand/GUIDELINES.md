# Helmcheck K3 — Panduan Logo

## 1. Logo

**Ide:** palang huruf H menjadi pinggiran helm, dan kubahnya duduk di rongga atas. Hasilnya huruf H yang memakai helm: inisial produk sekaligus pekerja yang patuh K3.

| Versi | File master | Kapan dipakai |
|---|---|---|
| Horizontal (utama) | `logo/helmcheck-horizontal.svg` | Header website, dokumen, presentasi |
| Bertumpuk | `logo/helmcheck-stacked.svg` | Papan area, stiker, sampul, ruang yang sempit melebar |
| Simbol | `logo/helmcheck-symbol.svg` | Avatar, ikon, bila nama sudah tertulis di dekatnya |
| Simbol kecil | `logo/helmcheck-symbol-small.svg` | **Wajib** di ukuran 32 px ke bawah (favicon, tab) |
| Wordmark | `logo/helmcheck-wordmark.svg` | Bila simbol sudah tampil terpisah di halaman yang sama |
| Latar gelap | `logo/*-reversed.svg` | Putih, geometri sedikit ditipiskan agar tidak tampak lebih tebal |

Varian siap pakai ada di `export/`: hitam, putih, biru satu warna, PNG 1200 px, ikon aplikasi, dan set ikon web (`export/symbol/favicon.ico`, `favicon.svg`, `apple-touch-icon.png`, `icon-192/512.png`, `site.webmanifest`, `head-snippet.html`).

## 2. Ruang kosong

Sisakan ruang kosong minimal **1 × lebar tiang H** di semua sisi logo. Lebar tiang = 17 % dari tinggi simbol. Ruang ini ikut membesar dan mengecil bersama logo.

## 3. Ukuran minimum

| Versi | Layar | Cetak |
|---|---|---|
| Horizontal | lebar 120 px | lebar 30 mm |
| Bertumpuk | lebar 96 px | lebar 22 mm |
| Simbol | 16 px (pakai file simbol kecil di ≤ 32 px) | 6 mm |

## 4. Warna

| Nama | HEX | RGB | CMYK (perkiraan) | Pantone (terdekat) | Kontras di atas putih |
|---|---|---|---|---|---|
| Biru rambu (utama) | `#0B5CAD` | 11 92 173 | 94 47 0 32 | 300 C | 6,7 : 1 |
| Tinta | `#141B22` | 20 27 34 | 41 21 0 87 | Black 6 C | 17,4 : 1 |

Konversi CMYK dan Pantone di atas masih perkiraan. Cocokkan dengan buku warna Pantone sebelum mencetak.

**Pasangan logo dan latar yang disetujui:**
- logo berwarna di atas putih;
- logo putih (`-reversed`) di atas biru rambu;
- logo putih di atas tinta atau foto gelap yang tenang;
- logo hitam di atas putih untuk cetak satu warna.

Merah `#C4122F` dan hijau `#1C7A47` adalah warna **status deteksi** di aplikasi (tanpa helm / pakai helm). Jangan pakai keduanya untuk logo.

## 5. Tipografi

- Logo dan judul memakai **Archivo** (variabel), tebal 700, lebar 112 %. Teks isi memakai Archivo 400.
- Lisensinya SIL Open Font License, bebas dipakai untuk logo. Salinan font ada di `fonts/`.
- Wordmark sudah berupa path. Jangan mengetik ulang "Helmcheck K3" sebagai pengganti logo.
- Kalau wordmark perlu dibuat ulang: `python brand/build_lockups.py`.

## 6. Yang tidak boleh

- Meregangkan, memampatkan, atau memutar logo.
- Mewarnai di luar palet, atau memberi bayangan, garis tepi, gradien, dan efek lain.
- Mengubah jarak atau perbandingan simbol dan teks dalam lockup.
- Memakai simbol ukuran normal di bawah 32 px. Gunakan versi kecil.
- Meletakkan logo berwarna di atas latar biru, hitam, atau foto ramai.
- Memakai logo dengan cara yang menyerupai rambu K3 resmi (lingkaran biru ISO 7010). Logo ini identitas produk, bukan rambu.

## 7. Catatan serah terima

- **Uji yang sudah dijalankan:** audit SVG (100/100 untuk simbol), tangga ukuran 16–256 px, uji piksel 16/32/48, satu warna, versi terbalik, greyscale, blur, cermin, rotasi 180°, serta konteks favicon, ikon aplikasi, dan header.
- **Batasan yang diketahui:**
  - Di 16 px, kubah helm melebur dengan palang. Versi kecil membantu, tetapi bentuk H yang paling dikenali.
  - Bila diputar 180°, H tetap terbaca, hanya kubahnya jadi menggantung.
- **Merek dagang:** belum ada penelusuran. Lakukan pencarian di PDKI (pdki-indonesia.dgip.go.id) dan pencarian gambar terbalik sebelum dipakai komersial.
- **Belum tersedia:** file PDF/EPS untuk percetakan. Ekspor dari SVG di Inkscape atau Illustrator bila diperlukan.
