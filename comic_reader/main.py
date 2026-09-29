"""
Titik Masuk Utama Aplikasi ComicVoice Reader (Desktop Windows)
Mengintegrasikan jendela bingkai seleksi bebas panjang/lebar,
balon suara mengambang always-on-top, deteksi gulir cepat (100ms),
dan pemutar audio instan 0ms.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from .config import load_config, save_config
from .ui.selection_frame import SelectionFrameWindow
from .ui.floating_widget import FloatingBubbleWidget
from .engine.tts_player import ComicTTSPlayer
from .engine.watcher import ScreenWatcherWorker

class ComicVoiceApp:
    def __init__(self):
        self.config = load_config()

        # Inisialisasi pemutar suara TTS (Default: Instan 0ms)
        self.tts = ComicTTSPlayer(
            voice_index=self.config.get("voice_index", 0),
            speed=self.config.get("speed", 1.1),
            volume=self.config.get("volume", 1.0)
        )

        # Inisialisasi jendela pengatur bingkai awal
        self.frame_window = SelectionFrameWindow(self.config.get("reading_zone", {}))
        self.frame_window.started.connect(self.on_frame_confirmed)

        # Inisialisasi balon suara mengambang
        self.bubble_widget = FloatingBubbleWidget(self.config)
        self._connect_bubble_signals()

        # Thread pekerja pengawas layar
        self.watcher = None

        # Tampilkan bingkai awal agar pengguna dapat mengatur area baca
        self.frame_window.show()

    def _connect_bubble_signals(self):
        panel = self.bubble_widget.control_panel
        panel.frame_reset_requested.connect(self.on_request_frame_reset)
        panel.voice_changed.connect(self.on_voice_changed)
        panel.speed_changed.connect(self.on_speed_changed)
        panel.volume_changed.connect(self.on_volume_changed)
        panel.pause_toggled.connect(self.on_pause_toggled)
        panel.cache_clear_requested.connect(self.on_cache_cleared)
        panel.instant_read_requested.connect(self.on_instant_read)
        panel.quit_requested.connect(self.quit_app)

    def on_frame_confirmed(self, zone: dict):
        """Dipanggil saat tombol MULAI BACA pada bingkai diklik"""
        self.config["reading_zone"] = zone
        save_config(self.config)

        # Tampilkan balon mengambang
        self.bubble_widget.show()
        self.bubble_widget.raise_()

        # Mulai pekerja pengawas layar jika belum ada
        if self.watcher is None:
            self.watcher = ScreenWatcherWorker(
                zone=zone,
                tts_player=self.tts,
                debounce_ms=self.config.get("scroll_debounce_ms", 100)
            )
            self.watcher.speaking_state_changed.connect(self.bubble_widget.set_speaking_state)
            self.watcher.status_changed.connect(self.bubble_widget.control_panel.set_status_text)
            self.watcher.start()
        else:
            self.watcher.update_zone(zone)
            self.watcher.set_paused(False)

        print(f"ComicVoice aktif pada area: {zone}")

    def on_request_frame_reset(self):
        """Menampilkan kembali bingkai untuk mengatur ulang area baca"""
        if self.watcher:
            self.watcher.set_paused(True)
        current_zone = self.config.get("reading_zone", {})
        self.frame_window.reposition_to_zone(current_zone)

    def on_voice_changed(self, idx: int):
        self.tts.set_voice(idx)
        self.config["voice_index"] = idx
        save_config(self.config)

    def on_speed_changed(self, speed: float):
        self.tts.set_speed(speed)
        self.config["speed"] = speed
        save_config(self.config)

    def on_volume_changed(self, volume: float):
        self.tts.set_volume(volume)
        self.config["volume"] = volume
        save_config(self.config)

    def on_pause_toggled(self):
        if self.watcher:
            is_paused = self.tts.toggle_pause()
            self.watcher.set_paused(is_paused)

    def on_cache_cleared(self):
        if self.watcher:
            self.watcher.clear_cache()

    def on_instant_read(self):
        if self.watcher:
            self.watcher.trigger_instant_read()

    def quit_app(self):
        print("Menutup ComicVoice Reader...")
        if self.watcher:
            self.watcher.stop()
        self.tts.shutdown()
        self.bubble_widget.close()
        self.frame_window.close()
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ComicVoice Reader")
    comic_app = ComicVoiceApp()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
