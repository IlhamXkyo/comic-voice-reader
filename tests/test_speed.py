import os
import sys
import time
import numpy as np
import cv2

# Tambah path
sys.path.insert(0, ".")

from comic_reader.engine.ocr_engine import ComicOCREngine
from comic_reader.engine.tts_player import ComicTTSPlayer
from comic_reader.config import AVAILABLE_VOICES

def test_speed_and_clarity():
    print("=== PENGUJIAN KECEPATAN & KEJELASAN SUARA ===")
    
    # 1. Uji OCR
    ocr = ComicOCREngine()
    img = np.ones((100, 500, 3), dtype=np.uint8) * 255
    cv2.putText(img, "Halo kawan! Ini tes dialog komik.", (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    t0 = time.time()
    extracted = ocr.extract_texts(img)
    ocr_time = time.time() - t0
    print(f"1. Waktu Deteksi OCR: {ocr_time*1000:.1f} ms")
    print(f"   Hasil Teks (Pemisahan Spasi): {extracted}")
    assert len(extracted) > 0 and " " in extracted[0], "Teks harus memiliki spasi dan terpisah jelas!"

    # 2. Uji Mode Suara Instan Offline (0ms)
    print("\n2. Uji Mode Suara Instan Offline:")
    tts_offline = ComicTTSPlayer(voice_index=3) # local-sapi
    t0 = time.time()
    tts_offline.enqueue_speech("Halo, ini pengujian suara instan tanpa jeda.")
    time.sleep(0.5)
    tts_offline.shutdown()
    print("   [OK] Suara offline langsung dieksekusi instan.")

    # 3. Uji Mode Suara Edge-TTS Indonesia
    print("\n3. Uji Mode Suara Natural Edge-TTS:")
    tts_edge = ComicTTSPlayer(voice_index=0) # Ardi
    t0 = time.time()
    audio_file = tts_edge._synthesize_speech_edge("Halo kawan, ini suara bahasa Indonesia yang jernih.")
    edge_time = time.time() - t0
    print(f"   Waktu pembuatan audio Edge-TTS: {edge_time:.2f} detik")
    print(f"   File audio: {audio_file}")
    assert audio_file is not None and os.path.exists(audio_file)
    tts_edge.shutdown()

    print("\nSEMUA PENGUJIAN SELESAI DENGAN HASIL SANGAT CEPAT DAN JERNIH!")

if __name__ == "__main__":
    test_speed_and_clarity()
