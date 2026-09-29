"""
Pekerja Pengawas Layar & Pengalur OCR-TTS (ScreenWatcherWorker)
Versi Optimal: Menggunakan Windows Native OCR (15ms) dan pengaliran dialog gabungan.
"""

import time
from PyQt6.QtCore import QThread, pyqtSignal

from .screen_capture import ScreenCapturer
from .scroll_detector import ScrollDetector
from .ocr_engine import ComicOCREngine
from .deduplicator import TextDeduplicator
from .tts_player import ComicTTSPlayer
from ..models import ReadingZone

class ScreenWatcherWorker(QThread):
    text_detected = pyqtSignal(list)
    speaking_state_changed = pyqtSignal(bool)
    status_changed = pyqtSignal(str)

    def __init__(self, zone, tts_player: ComicTTSPlayer, debounce_ms=220):
        super().__init__()
        self.zone = ReadingZone.from_dict(zone)
        self.tts = tts_player
        self.running = True
        self.is_paused = False

        self.capturer = ScreenCapturer()
        self.detector = ScrollDetector(debounce_ms=debounce_ms, motion_threshold=3.5)
        self.ocr = ComicOCREngine()
        self.dedup = TextDeduplicator()

        self.tts.on_start_speech = self._on_tts_start
        self.tts.on_end_speech = self._on_tts_end

    def update_zone(self, new_zone):
        self.zone = ReadingZone.from_dict(new_zone)
        self.detector.reset()
        print(f"Area bidik diperbarui: {self.zone.to_dict()}")

    def trigger_instant_read(self):
        if self.is_paused:
            return
        frame = self.capturer.capture_zone(
            self.zone.x,
            self.zone.y,
            self.zone.width,
            self.zone.height
        )
        texts = self.ocr.extract_texts(frame)
        new_texts = self.dedup.filter_new_texts(texts)
        if new_texts:
            print(f"Dialog dibaca (manual): {new_texts}")
            self.text_detected.emit(new_texts)
            self.tts.enqueue_speech(new_texts)

    def clear_cache(self):
        self.dedup.clear()
        self.tts.clear_queue()
        print("Riwayat baca berhasil direset.")

    def set_paused(self, paused: bool):
        self.is_paused = paused
        if paused:
            self.tts.clear_queue()
            self.status_changed.emit("Dijeda")
        else:
            self.status_changed.emit("Memantau Gulir...")

    def _on_tts_start(self, text: str):
        self.speaking_state_changed.emit(True)

    def _on_tts_end(self):
        self.speaking_state_changed.emit(False)

    def run(self):
        while self.running:
            if self.is_paused:
                time.sleep(0.1)
                continue

            try:
                frame = self.capturer.capture_zone(
                    self.zone.x,
                    self.zone.y,
                    self.zone.width,
                    self.zone.height
                )

                # Deteksi apakah layar baru saja berhenti bergerak
                is_settled = self.detector.update_frame(frame)

                if is_settled:
                    texts = self.ocr.extract_texts(frame)
                    new_texts = self.dedup.filter_new_texts(texts)

                    if new_texts:
                        print(f"Dialog baru terbaca: {new_texts}")
                        self.text_detected.emit(new_texts)
                        # Kirim seluruh daftar dialog baru agar diucapkan sebagai satu alur cerita
                        self.tts.enqueue_speech(new_texts)

            except Exception as e:
                print(f"Kesalahan pada loop pengawas layar: {e}")
                self.status_changed.emit("Gangguan penangkap layar, memulihkan...")
                time.sleep(0.5)

            time.sleep(0.06)

    def stop(self):
        self.running = False
        self.capturer.close()
        self.tts.shutdown()
        self.wait(1000)
