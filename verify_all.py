import os
import cv2
import numpy as np

def test_ocr():
    print("--- 1. Uji Mesin OCR (RapidOCR) ---")
    from comic_reader.engine.ocr_engine import ComicOCREngine
    engine = ComicOCREngine()

    # Buat gambar dummy berisi teks komik buatan
    img = np.ones((150, 450, 3), dtype=np.uint8) * 255
    cv2.putText(img, "Halo dunia! Ini komik.", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    cv2.putText(img, "Siapa kamu sebenarnya?", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

    texts = engine.extract_texts(img)
    print(f"Hasil ekstraksi OCR: {texts}")
    assert len(texts) > 0, "OCR harus mendeteksi teks pada gambar tes!"
    print("  [OK] RapidOCR berjalan dengan baik.")

def test_tts():
    print("--- 2. Uji Mesin TTS (Edge-TTS 3 Karakter Suara) ---")
    from comic_reader.engine.tts_player import ComicTTSPlayer
    tts = ComicTTSPlayer(voice_index=0)

    # Uji sintesis 1 kalimat
    audio_path = tts._synthesize_speech("Halo, ini uji coba suara pembaca komik.")
    print(f"Hasil sintesis audio: {audio_path}")
    assert audio_path is not None and os.path.exists(audio_path), "File audio harus berhasil dibuat!"
    assert os.path.getsize(audio_path) > 1000, "Ukuran file audio harus valid!"
    print("  [OK] Edge-TTS berhasil membuat file audio MP3.")
    tts.shutdown()

def test_imports():
    print("--- 3. Uji Import Antarmuka PyQt6 ---")
    from PyQt6.QtWidgets import QApplication
    from comic_reader.ui.selection_frame import SelectionFrameWindow
    from comic_reader.ui.floating_widget import FloatingBubbleWidget
    print("  [OK] Semua komponen UI PyQt6 berhasil di-import tanpa error.")

if __name__ == "__main__":
    test_imports()
    test_ocr()
    test_tts()
    print("\nSEMUA UJI INTEGRASI SELESAI DAN BERHASIL 100%!")
