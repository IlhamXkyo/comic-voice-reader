# ComicVoice Reader 🎙️📖

Aplikasi pembaca layar komik otomatis (Webtoon, Manhwa, Manga) dengan gaya visual buku komik pop art, pengawas gulir layar pintar, dan pemutar suara non-blocking.

---

## Fitur Utama

- **Bingkai Seleksi Bebas Panjang & Lebar (8-Way Resize)**:
  Tarik sisi tepi (kiri, kanan, atas, bawah) atau sudut mana pun untuk menyesuaikan kolom komik. Tersedia juga tombol pintas ukuran (+/- 50px).
- **Balon Suara Mengambang (Always on Top)**:
  Widget bergaya komik klasik (bebas dari tampilan AI generik) yang selalu berada di atas jendela komik dan bisa digeser bebas.
- **Deteksi Gulir Layar Pintar (100ms Debounce)**:
  Mendeteksi pergerakan gulir layar secara real-time. Aplikasi menahan proses OCR saat layar bergerak dan langsung membaca begitu gulir berhenti sejenak.
- **Penyaring Teks Anti Duplikat**:
  Mencegah pembacaan berulang pada dialog yang sama saat kamu berhenti membaca di satu halaman.
- **Pilihan Suara**:
  1. `⚡ Instan 0ms (Lokal Offline)`: Berbunyi instan tanpa koneksi internet dan tanpa jeda buffering.
  2. `🌐 Pria Natural (Ardi - Cloud Edge-TTS)`: Suara pria natural bahasa Indonesia.
  3. `🌐 Wanita Natural (Gadis - Cloud Edge-TTS)`: Suara wanita jernih bahasa Indonesia.
  4. `🌐 Narator Komik (Brian - Cloud Edge-TTS)`: Suara narator ekspresif untuk dialog Inggris/dwibahasa.
- **Pondasi Android**:
  Dilengkapi modul latar belakang Android (`SYSTEM_ALERT_WINDOW` & Foreground Service) di folder `android/`.

---

## Instalasi & Cara Menjalankan (Windows)

### 1. Kloning Repositori
```bash
git clone https://github.com/IlhamXkyo/comic-voice-reader.git
cd comic-voice-reader
```

### 2. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
python run.py
```
Atau klik dua kali `Buka_ComicVoice_Reader.bat`.

---

## Lisensi
MIT License
