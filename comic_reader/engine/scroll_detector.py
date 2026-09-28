import cv2
import time
import numpy as np

class ScrollDetector:
    """
    Pendeteksi gerakan gulir layar ultra-responsif (debounce 100ms).
    Memastikan pembacaan langsung terpicu seketika saat gulir berhenti
    tanpa jeda tunggu yang lama.
    """
    def __init__(self, debounce_ms=100, motion_threshold=4.0):
        self.debounce_sec = debounce_ms / 1000.0
        self.motion_threshold = motion_threshold
        self.prev_small_gray = None
        self.last_motion_time = time.time()
        self.is_moving = False
        self.already_triggered_for_current_still = False

    def update_frame(self, frame_bgr: np.ndarray) -> bool:
        now = time.time()

        h, w = frame_bgr.shape[:2]
        small_w = 100
        small_h = max(20, int(h * (small_w / max(1, w))))
        small = cv2.resize(frame_bgr, (small_w, small_h), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        if self.prev_small_gray is None:
            self.prev_small_gray = gray
            self.last_motion_time = now
            return False

        diff = cv2.absdiff(gray, self.prev_small_gray)
        mean_diff = float(np.mean(diff))
        self.prev_small_gray = gray

        if mean_diff > self.motion_threshold:
            self.is_moving = True
            self.last_motion_time = now
            self.already_triggered_for_current_still = False
            return False
        else:
            if self.is_moving:
                self.is_moving = False
                self.last_motion_time = now

            time_since_motion = now - self.last_motion_time

            # Jika gerakan telah stabil selama 100ms dan belum dibaca
            if time_since_motion >= self.debounce_sec and not self.already_triggered_for_current_still:
                self.already_triggered_for_current_still = True
                return True

        return False

    def reset(self):
        self.prev_small_gray = None
        self.is_moving = False
        self.already_triggered_for_current_still = False
        self.last_motion_time = time.time()
