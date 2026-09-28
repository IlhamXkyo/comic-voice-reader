# Panduan Implementasi ComicVoice Android

Modul ini berisi arsitektur dan kode sumber dasar aplikasi Android ComicVoice Reader.

## Kebutuhan Sistem Android
- Android SDK 26 (Android 8.0 Oreo) ke atas.
- Izin Khusus:
  1. `SYSTEM_ALERT_WINDOW` ("Tampilkan di atas aplikasi lain" / Draw over other apps) untuk menampilkan balon suara mengambang di atas webtoon atau manga reader.
  2. `FOREGROUND_SERVICE_MEDIA_PROJECTION` untuk menangkap area baca layar secara aman melalui API resmi Android.

## Struktur Komponen Utama
1. **`FloatingBubbleService.kt`**: Foreground Service yang mengelola tampilan widget balon mengambang di `WindowManager`.
2. **`ScreenCaptureService.kt`**: Mengelola tangkapan layar area spesifik dengan `MediaProjection` dan `ImageReader`.
3. **`ComicMLKitOCR.kt`**: Mesin OCR offline berbasis Google ML Kit Text Recognition (cepat dan hemat baterai).
4. **`AndroidTTSPlayer.kt`**: Mesin pembaca dialog menggunakan `TextToSpeech` Android dengan pilihan suara pria, wanita, dan narator.

## Alur Penggunaan di Android
1. Pengguna membuka aplikasi ComicVoice Android dan memberikan izin jendela mengambang serta persetujuan rekam layar.
2. Muncul bingkai transparan di atas layar. Pengguna menggeser ukuran bingkai sesuai kolom komik.
3. Klik tombol "Mulai Baca". Bingkai menghilang, menyisakan balon suara mengambang.
4. Saat pengguna membuka Webtoon/Tachiyomi dan menggulir ke atas: begitu gulir berhenti sejenak, suara otomatis membaca dialog balon komik.
