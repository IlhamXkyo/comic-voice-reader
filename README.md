# ComicVoice Reader 🎙️📖

[![Stars](https://img.shields.io/badge/GitHub-Stars_Welcome-gold?style=flat-square&logo=github)](https://github.com/IlhamXkyo/comic-voice-reader)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows_10%2F11-0078D6?style=flat-square&logo=windows)](https://microsoft.com)
[![Tests: Passing](https://img.shields.io/badge/Tests-5%2F5_Passing-brightgreen?style=flat-square)]()

Aplikasi pembaca layar komik otomatis real-time (Webtoon, Manhwa, Manga) dengan tema visual komik retro pop art, pengawas gulir layar pintar, dan pemutar suara multi-mesin (Windows SAPI 0ms & Edge-TTS Neural).

---

## ⚡ Tolok Ukur Kinerja (Latency Benchmark)

| Komponen Mesin | Latensi Eksekusi | Keterangan & Keunggulan |
| :--- | :--- | :--- |
| **Windows Native Media OCR** | **~15 - 18 ms** | Ekstraksi teks in-memory via stream BMP tanpa kompresi, spasi kata 100% presisi |
| **RapidOCR Fallback** | **~120 - 160 ms** | Deteksi alternatif lintas platform berbasis ONNX Runtime |
| **SAPI SpVoice (Lokal)** | **~5 ms (Instan)** | Suara lokal Windows tanpa koneksi internet & tanpa buffering |
| **Edge-TTS Neural (Cloud)** | **~1.5 - 2.0 s** | Kualitas suara natural mirip manusia (Ardi, Gadis, Brian) |

---

## 🚀 Fitur Utama

- **Bingkai Seleksi Bebas 8-Arah (8-Way Resize Frame)**:
  Ubah ukuran area baca dari setiap sisi dan sudut layar secara presisi. Tersedia tombol cepat penyesuaian resolusi (+/- 50px).
- **Balon Suara Mengambang (Always on Top)**:
  Widget pop art interaktif yang selalu melayang di atas komik, dapat digeser bebas, dan menampilkan status baca.
- **Deteksi Gulir Layar Responsif (100ms Debounce)**:
  Mendeteksi pergerakan halaman secara real-time. Proses OCR ditahan saat layar bergerak dan otomatis memicu pembacaan ketika posisi gulir berhenti.
- **Penyaring Teks Anti-Duplikat Cerdas (Ratio-Bound Deduplicator)**:
  Mencegah pembacaan ulang pada dialog yang telah diucapkan tanpa memotong dialog pendek baru yang sah.
- **Pipeline Aliran Gambar BMP In-Memory**:
  Mengeliminasi overhead kompresi PNG saat pengaliran frame ke Windows Media Imaging.
- **Multi-Pilihan Karakter Suara**:
  1. `⚡ Instan 0ms (Lokal Offline)`: Bersuara langsung tanpa koneksi internet.
  2. `🌐 Pria Natural (Ardi - Cloud Edge-TTS)`: Suara pria natural bahasa Indonesia.
  3. `🌐 Wanita Natural (Gadis - Cloud Edge-TTS)`: Suara wanita jernih bahasa Indonesia.
  4. `🌐 Narator Komik (Brian - Cloud Edge-TTS)`: Narasi ekspresif untuk dialog Inggris/dwibahasa.

---

## 💻 Instalasi & Menjalankan (Windows)

### 1. Kloning Repositori
```bash
git clone https://github.com/IlhamXkyo/comic-voice-reader.git
cd comic-voice-reader
```

### 2. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 3. Jalankan Pengujian
```bash
python test_advanced_audit.py
```

### 4. Mulai Aplikasi
```bash
python run.py
```
Atau klik dua kali pada berkas `Buka_ComicVoice_Reader.bat`.

---

## 🏷️ GitHub Topics & SEO
`webtoon-reader` • `manhwa-reader` • `manga-ocr` • `edge-tts` • `screen-reader` • `comic-reader` • `python-gui` • `pyqt6` • `rapidocr` • `assistive-technology`

---

## 📄 Lisensi
Didistribusikan di bawah lisensi [MIT License](LICENSE).
