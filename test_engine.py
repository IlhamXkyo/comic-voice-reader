"""
Unit test dan verifikasi mandiri untuk komponen mesin ComicVoice:
- Deduplicator (Pencegahan baca ganda)
- Screen capturer
- Scroll detector
"""

import numpy as np
from comic_reader.engine.deduplicator import TextDeduplicator
from comic_reader.engine.scroll_detector import ScrollDetector

def test_deduplicator():
    print("Menguji Deduplicator...")
    dedup = TextDeduplicator(similarity_threshold=0.80)

    # Uji 1: Dialog pertama
    texts_1 = ["Hei, apa yang kamu lakukan di sini?!", "Aku sedang mencari buku sihir kuno."]
    filtered_1 = dedup.filter_new_texts(texts_1)
    assert len(filtered_1) == 2, f"Harusnya 2 teks baru, dapat {len(filtered_1)}"
    print("  [OK] Dialog baru berhasil lolos.")

    # Uji 2: Pengulangan saat layar berhenti di posisi yang sama
    texts_2 = ["Hei, apa yang kamu lakukan di sini?!", "Aku sedang mencari buku sihir kuno."]
    filtered_2 = dedup.filter_new_texts(texts_2)
    assert len(filtered_2) == 0, f"Harusnya 0 teks (duplikat), dapat {len(filtered_2)}"
    print("  [OK] Dialog yang sama berhasil disaring (tidak dibaca dua kali).")

    # Uji 3: Dialog baru masuk saat di-scroll
    texts_3 = ["Hei, apa yang kamu lakukan di sini?!", "Jangan mendekat, bahaya!"]
    filtered_3 = dedup.filter_new_texts(texts_3)
    assert len(filtered_3) == 1 and filtered_3[0] == "Jangan mendekat, bahaya!", f"Harusnya cuma teks baru, dapat {filtered_3}"
    print("  [OK] Hanya dialog baru yang lolos setelah gulir.")

def test_scroll_detector():
    print("Menguji Scroll Detector...")
    detector = ScrollDetector(debounce_ms=100, motion_threshold=2.0)

    # Frame statis 1 & 2
    f1 = np.zeros((200, 200, 3), dtype=np.uint8)
    res1 = detector.update_frame(f1)
    assert res1 is False

    # Frame bergerak (simulasi scroll)
    f2 = np.ones((200, 200, 3), dtype=np.uint8) * 100
    res2 = detector.update_frame(f2)
    assert res2 is False
    assert detector.is_moving is True
    print("  [OK] Gerakan gulir terdeteksi.")

if __name__ == "__main__":
    test_deduplicator()
    test_scroll_detector()
    print("Semua tes komponen logika berhasil 100%!")
