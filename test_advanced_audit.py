import os
import sys
import unittest
import numpy as np
import cv2

# Pastikan path modul terbaca
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comic_reader.engine.deduplicator import TextDeduplicator
from comic_reader.engine.ocr_engine import ComicOCREngine
from comic_reader.engine.tts_player import ComicTTSPlayer
from comic_reader.models import ReadingZone

class TestComicVoiceReaderAudit(unittest.TestCase):
    def test_deduplicator_substring_edge_cases(self):
        dedup = TextDeduplicator(similarity_threshold=0.80)
        
        # Kalimat panjang pertama
        long_sentence = "Aku tidak percaya ini bisa terjadi pada kita semua di sini"
        filtered1 = dedup.filter_new_texts([long_sentence])
        self.assertEqual(filtered1, [long_sentence])
        
        # Substring dengan panjang jauh berbeda (dialog baru yang sah)
        # Seharusnya TIDAK dibuang sebagai duplikat
        short_new_sentence = "ini bisa terjadi"
        filtered2 = dedup.filter_new_texts([short_new_sentence])
        self.assertEqual(filtered2, [short_new_sentence], "Dialog pendek tidak boleh terhapus hanya karena kata-katanya termuat di kalimat panjang sebelumnya!")
        
        # Kalimat duplikat dengan typo kecil OCR (harus tersaring)
        typo_sentence = "Aku tidak percaya ini bisa terjadi pada kita semua di sini."
        filtered3 = dedup.filter_new_texts([typo_sentence])
        self.assertEqual(filtered3, [], "Kalimat yang hampir identik harus disaring sebagai duplikat!")

    def test_deduplicator_clear_and_filter(self):
        dedup = TextDeduplicator()
        texts = ["Halo dunia", "Selamat pagi kawan"]
        res = dedup.filter_new_texts(texts)
        self.assertEqual(len(res), 2)
        
        # Coba filter ulang (harus kosong)
        res_dup = dedup.filter_new_texts(texts)
        self.assertEqual(len(res_dup), 0)
        
        # Reset cache
        dedup.clear()
        res_after_clear = dedup.filter_new_texts(texts)
        self.assertEqual(len(res_after_clear), 2)

    def test_reading_zone_model(self):
        zone = ReadingZone(x=10, y=20, width=500, height=800)
        z_dict = zone.to_dict()
        zone_restored = ReadingZone.from_dict(z_dict)
        self.assertEqual(zone.x, zone_restored.x)
        self.assertEqual(zone.width, zone_restored.width)

    def test_ocr_bmp_streaming(self):
        ocr = ComicOCREngine()
        # Buat frame sintetis
        frame = np.ones((120, 400, 3), dtype=np.uint8) * 255
        cv2.putText(frame, "Audit Verifikasi OCR", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        texts = ocr.extract_texts(frame)
        self.assertTrue(len(texts) > 0, "OCR harus berhasil mengekstrak teks dari frame sintetis!")
        self.assertIn("Audit", texts[0])

    def test_tts_player_bounds_and_safety(self):
        tts = ComicTTSPlayer(voice_index=0)
        
        # Uji clamping kecepatan
        tts.set_speed(0.1) # di bawah min
        self.assertEqual(tts.speed, 0.5)
        tts.set_speed(10.0) # di atas max
        self.assertEqual(tts.speed, 2.5)
        
        # Uji clamping volume
        tts.set_volume(-1.0)
        self.assertEqual(tts.volume, 0.0)
        tts.set_volume(5.0)
        self.assertEqual(tts.volume, 1.0)
        
        # Uji antrean teks kosong/noise
        tts.enqueue_speech("")
        tts.enqueue_speech(" ")
        self.assertTrue(tts.audio_queue.empty())
        
        tts.shutdown()

if __name__ == "__main__":
    unittest.main()
