import numpy as np
from PIL import Image

try:
    import mss
    HAS_MSS = True
except ImportError:
    HAS_MSS = False

from PIL import ImageGrab

class ScreenCapturer:
    """
    Penangkap area layar berkecepatan tinggi menggunakan pustaka mss
    dengan fallback otomatis ke Pillow ImageGrab.
    """
    def __init__(self):
        self._sct = mss.mss() if HAS_MSS else None

    def capture_zone(self, x: int, y: int, width: int, height: int) -> np.ndarray:
        """
        Menangkap area layar pada koordinat tertentu dan mengembalikannya
        dalam format numpy array BGR (siap untuk OCR / OpenCV).
        """
        # Validasi ukuran minimal
        width = max(50, int(width))
        height = max(50, int(height))
        x = max(0, int(x))
        y = max(0, int(y))

        if self._sct:
            monitor = {"top": y, "left": x, "width": width, "height": height}
            sct_img = self._sct.grab(monitor)
            # mss menghasilkan BGRA, ubah ke format numpy BGR
            img_np = np.array(sct_img)
            # Hapus channel alpha jika ada
            if img_np.shape[2] == 4:
                img_np = img_np[:, :, :3]
            return img_np
        else:
            bbox = (x, y, x + width, y + height)
            pil_img = ImageGrab.grab(bbox=bbox)
            img_np = np.array(pil_img)
            # Konversi RGB Pillow ke BGR numpy
            img_bgr = img_np[:, :, ::-1]
            return img_bgr

    def close(self):
        if self._sct:
            self._sct.close()
