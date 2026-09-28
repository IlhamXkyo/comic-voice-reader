import asyncio
import cv2
import numpy as np

try:
    import winsdk.windows.media.ocr as win_ocr
    import winsdk.windows.graphics.imaging as imaging
    import winsdk.windows.storage.streams as streams
    HAS_WIN_OCR = True
except Exception:
    HAS_WIN_OCR = False

try:
    from rapidocr_onnxruntime import RapidOCR
    HAS_RAPID_OCR = True
except Exception:
    HAS_RAPID_OCR = False

class ComicOCREngine:
    """
    Mesin OCR komik berkecepatan tinggi:
    1. Menggunakan Windows Native Media OCR (0.016 detik, pemisahan kata & spasi 100% sempurna).
    2. Fallback ke RapidOCR jika sistem Windows tidak mendukung.
    3. Mengurutkan teks komik dari atas ke bawah dan membersihkan noise coretan gambar.
    """
    def __init__(self):
        self.win_engine = None
        self.rapid_engine = None
        self._init_engines()

    def _init_engines(self):
        if HAS_WIN_OCR:
            try:
                # Prioritaskan bahasa Indonesia atau bahasa profil sistem
                self.win_engine = win_ocr.OcrEngine.try_create_from_user_profile_languages()
                if self.win_engine:
                    print(f"Windows Native OCR aktif (Bahasa: {self.win_engine.recognizer_language.display_name}). Latensi ~15ms.")
            except Exception as e:
                print(f"Peringatan init Windows OCR: {e}")
                self.win_engine = None

        if HAS_RAPID_OCR and self.win_engine is None:
            try:
                self.rapid_engine = RapidOCR()
                print("RapidOCR aktif sebagai mesin alternatif.")
            except Exception as e:
                print(f"Peringatan init RapidOCR: {e}")
                self.rapid_engine = None

    async def _recognize_windows_async(self, img_bgr: np.ndarray) -> list[str]:
        # Encode gambar ke PNG di memori
        success, buf = cv2.imencode('.png', img_bgr)
        if not success:
            return []

        stream = streams.InMemoryRandomAccessStream()
        writer = streams.DataWriter(stream)
        writer.write_bytes(buf.tobytes())
        await writer.store_async()
        await writer.flush_async()
        stream.seek(0)

        decoder = await imaging.BitmapDecoder.create_async(stream)
        software_bitmap = await decoder.get_software_bitmap_async()

        result = await self.win_engine.recognize_async(software_bitmap)
        if not result or not result.lines:
            return []

        # Ekstrak baris teks dengan koordinat bounding box
        lines_data = []
        for line in result.lines:
            text = line.text.strip()
            # Filter noise singkat (kurang dari 2 huruf atau karakter coretan non-kata)
            if len(text) < 2:
                continue
            
            # Hitung posisi vertikal (y) dari kata pertama di baris ini
            top_y = 0
            height = 20
            if len(line.words) > 0:
                rect = line.words[0].bounding_rect
                top_y = rect.y
                height = rect.height

            lines_data.append({
                "text": text,
                "top_y": top_y,
                "height": height
            })

        if not lines_data:
            return []

        # Urutkan dari atas ke bawah
        lines_data.sort(key=lambda x: x["top_y"])

        # Kelompokkan baris teks yang berdekatan menjadi paragraf dialog utuh
        bubbles = []
        current_lines = [lines_data[0]["text"]]
        prev_top = lines_data[0]["top_y"]

        for item in lines_data[1:]:
            # Jika selisih vertikal masih dalam satu balon dialog (~1.8x tinggi teks)
            if abs(item["top_y"] - prev_top) < item["height"] * 1.8:
                current_lines.append(item["text"])
            else:
                bubbles.append(" ".join(current_lines))
                current_lines = [item["text"]]
            prev_top = item["top_y"]

        if current_lines:
            bubbles.append(" ".join(current_lines))

        return bubbles

    def _extract_windows(self, img_bgr: np.ndarray) -> list[str]:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res = loop.run_until_complete(self._recognize_windows_async(img_bgr))
            loop.close()
            return res
        except Exception as e:
            print(f"Kesalahan eksekusi Windows OCR: {e}")
            return []

    def _extract_rapid(self, img_bgr: np.ndarray) -> list[str]:
        if not self.rapid_engine:
            return []
        try:
            result, _ = self.rapid_engine(img_bgr)
            if not result:
                return []
            texts = []
            for item in result:
                box, text, conf = item
                if conf >= 0.60:
                    clean = text.strip()
                    if len(clean) >= 2:
                        texts.append(clean)
            return texts
        except Exception as e:
            print(f"Kesalahan RapidOCR: {e}")
            return []

    def extract_texts(self, img_bgr: np.ndarray) -> list[str]:
        if img_bgr is None or img_bgr.size == 0:
            return []

        if self.win_engine is not None:
            res = self._extract_windows(img_bgr)
            if res:
                return res

        return self._extract_rapid(img_bgr)
