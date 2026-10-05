import os
import sys
import time
import queue
import asyncio
import tempfile
import shutil
import threading
from typing import Callable, Optional

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False

try:
    import win32com.client
    HAS_WIN32COM = True
except ImportError:
    HAS_WIN32COM = False

from ..config import AVAILABLE_VOICES

class ComicTTSPlayer:
    """
    Pemutar suara pembaca komik dengan:
    1. Mesin lokal instan 0ms (SAPI.SpVoice Async) sebagai default tanpa jeda internet.
    2. Edge-TTS neural online (Ardi, Gadis, Brian).
    3. Pengaliran dialog gabungan (batching) dan pembatalan otomatis (purge) saat bergulir.
    """
    def __init__(self, voice_index=0, speed=1.1, volume=1.0):
        self.voice_index = voice_index
        self.speed = speed
        self.volume = volume
        self.is_paused = False
        self.is_stopped = False

        self.audio_queue = queue.Queue()
        self.temp_dir = tempfile.mkdtemp(prefix="comic_tts_")

        self.on_start_speech: Optional[Callable[[str], None]] = None
        self.on_end_speech: Optional[Callable[[], None]] = None

        self._active_sapi_voice = None
        self._init_audio_system()

        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def _init_audio_system(self):
        if HAS_PYGAME:
            try:
                pygame.mixer.init()
            except Exception as e:
                print(f"Peringatan init pygame mixer: {e}")

    def set_voice(self, index: int):
        if 0 <= index < len(AVAILABLE_VOICES):
            self.voice_index = index
            self.stop_current_audio()

    def set_speed(self, speed: float):
        self.speed = max(0.5, min(2.5, float(speed)))

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, float(volume)))
        if HAS_PYGAME and pygame.mixer.get_init():
            try:
                pygame.mixer.music.set_volume(self.volume)
            except Exception:
                pass

    def enqueue_speech(self, text_or_list):
        if self.is_paused:
            return

        if isinstance(text_or_list, list):
            clean_items = [t.strip() for t in text_or_list if t.strip() and len(t.strip()) > 1]
            if not clean_items:
                return
            combined = ". ".join(clean_items) + "."
        else:
            combined = str(text_or_list).strip()
            if not combined or len(combined) < 2:
                return

        # Segera bersihkan antrean lama agar suara baru langsung diproses
        self.clear_queue()
        self.audio_queue.put(combined)

    def clear_queue(self):
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
        self.stop_current_audio()

    def stop_current_audio(self):
        if HAS_PYGAME and pygame.mixer.get_init():
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        if self._active_sapi_voice:
            try:
                if HAS_WIN32COM:
                    import pythoncom
                    try:
                        pythoncom.CoInitialize()
                    except Exception:
                        pass
                # SVSFPurgeBeforeSpeak = 2
                self._active_sapi_voice.Speak("", 2)
            except Exception:
                pass

    def toggle_pause(self) -> bool:
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.stop_current_audio()
        return self.is_paused

    def _format_rate_str(self) -> str:
        percentage = int(round((self.speed - 1.0) * 100))
        if percentage >= 0:
            return f"+{percentage}%"
        return f"{percentage}%"

    def _format_volume_str(self) -> str:
        percentage = int(round((self.volume - 1.0) * 100))
        if percentage >= 0:
            return f"+{percentage}%"
        return f"{percentage}%"

    async def _generate_audio_edge(self, text: str, output_path: str):
        voice_info = AVAILABLE_VOICES[self.voice_index]
        if voice_info.get("type") == "edge":
            voice_id = voice_info["id"]
        else:
            voice_id = "id-ID-ArdiNeural"
        rate_str = self._format_rate_str()
        vol_str = self._format_volume_str()

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice_id,
            rate=rate_str,
            volume=vol_str
        )
        await communicate.save(output_path)

    def _speak_local_sapi(self, text: str):
        """Memutar suara lokal Windows secara instan (0.005 detik, non-blocking)"""
        if not HAS_WIN32COM:
            return False
        try:
            import pythoncom
            pythoncom.CoInitialize()
            if self._active_sapi_voice is None:
                self._active_sapi_voice = win32com.client.Dispatch("SAPI.SpVoice")

            voice = self._active_sapi_voice
            rate_val = int((self.speed - 1.0) * 6)
            voice.Rate = max(-10, min(10, rate_val))
            voice.Volume = int(self.volume * 100)

            if self.on_start_speech:
                self.on_start_speech(text)

            # SVSFlagsAsync = 1 (langsung berbunyi dalam milidetik tanpa membekukan loop)
            # SVSFPurgeBeforeSpeak = 2 (batalkan jika ada kalimat lama)
            voice.Speak(text, 1 | 2)

            # Tunggu pembacaan selesai sambil tetap merespons pembatalan
            while not self.is_stopped and not self.is_paused and self.audio_queue.empty():
                # Status 0 = done
                if voice.Status.RunningState == 1: # 1 = SRSEDone
                    break
                time.sleep(0.04)

            if self.on_end_speech:
                self.on_end_speech()

            pythoncom.CoUninitialize()
            return True
        except Exception as e:
            print(f"SAPI error: {e}")
            return False

    def _synthesize_speech_edge(self, text: str) -> Optional[str]:
        filename = f"speech_{int(time.time() * 1000)}.mp3"
        output_path = os.path.join(self.temp_dir, filename)

        if HAS_EDGE_TTS:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._generate_audio_edge(text, output_path))
                loop.close()
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    return output_path
            except Exception as e:
                print(f"Edge-TTS gagal ({e}), menggunakan suara lokal instan.")

        return None

    def _synthesize_speech(self, text: str) -> Optional[str]:
        """Alias untuk sintesis audio edge (kompatibilitas backward)"""
        return self._synthesize_speech_edge(text)

    def _worker_loop(self):
        while not self.is_stopped:
            try:
                text = self.audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if self.is_paused or self.is_stopped:
                continue

            voice_type = AVAILABLE_VOICES[self.voice_index].get("type", "sapi")

            # 1. Mode Instan Lokal 0ms (Default)
            if voice_type == "sapi":
                self._speak_local_sapi(text)
                continue

            # 2. Mode Edge-TTS (Cloud)
            audio_file = self._synthesize_speech_edge(text)
            if not audio_file:
                self._speak_local_sapi(text)
                continue

            if self.on_start_speech:
                try:
                    self.on_start_speech(text)
                except Exception:
                    pass

            if HAS_PYGAME and pygame.mixer.get_init():
                try:
                    pygame.mixer.music.load(audio_file)
                    pygame.mixer.music.set_volume(self.volume)
                    pygame.mixer.music.play()

                    while pygame.mixer.music.get_busy() and not self.is_paused and not self.is_stopped and self.audio_queue.empty():
                        time.sleep(0.03)

                    pygame.mixer.music.unload()
                except Exception as e:
                    print(f"Kesalahan pemutaran audio: {e}")

            if self.on_end_speech:
                try:
                    self.on_end_speech()
                except Exception:
                    pass

            try:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            except Exception:
                pass

    def shutdown(self):
        self.is_stopped = True
        self.clear_queue()
        if hasattr(self, "temp_dir") and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except Exception:
                pass
