import re
import difflib
from collections import deque

class TextDeduplicator:
    """
    Penyaring teks untuk mencegah pembacaan berulang (duplikat).
    Menyimpan riwayat teks yang baru saja dibaca dalam buffer memori geser (ring buffer).
    """
    def __init__(self, max_history=60, similarity_threshold=0.80):
        self.max_history = max_history
        self.similarity_threshold = similarity_threshold
        self.history = deque(maxlen=max_history)
        self.normalized_history = deque(maxlen=max_history)

    def normalize(self, text: str) -> str:
        """
        Membersihkan teks dari tanda baca ganda, spasi berlebih, dan mengubah ke huruf kecil
        agar pencocokan lebih akurat.
        """
        # Hapus karakter non-alfanumerik umum untuk komik, pertahankan huruf dan angka
        cleaned = re.sub(r'[^\w\s]', '', text.lower())
        # Gabungkan spasi berlebih
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def is_duplicate(self, text: str) -> bool:
        """
        Memeriksa apakah teks sudah pernah dibaca sebelumnya.
        """
        norm_text = self.normalize(text)
        if not norm_text or len(norm_text) < 2:
            return True  # Abaikan teks kosong atau terlalu pendek (noise OCR)

        # Cek kesamaan persis terlebih dahulu
        if norm_text in self.normalized_history:
            return True

        # Cek kesamaan string menggunakan SequenceMatcher
        for prev in self.normalized_history:
            # Jika teks saat ini adalah substring signifikan dari teks sebelumnya atau sebaliknya
            if len(norm_text) > 8 and len(prev) > 8:
                if norm_text in prev or prev in norm_text:
                    return True

            similarity = difflib.SequenceMatcher(None, norm_text, prev).ratio()
            if similarity >= self.similarity_threshold:
                return True

        return False

    def mark_as_read(self, text: str):
        """
        Menandai teks sebagai telah dibaca.
        """
        norm = self.normalize(text)
        if norm:
            self.history.append(text)
            self.normalized_history.append(norm)

    def filter_new_texts(self, text_list: list[str]) -> list[str]:
        """
        Memfilter daftar teks dari OCR dan hanya mengembalikan teks yang benar-benar baru.
        """
        new_texts = []
        for text in text_list:
            clean = text.strip()
            if not self.is_duplicate(clean):
                new_texts.append(clean)
                self.mark_as_read(clean)
        return new_texts

    def clear(self):
        """
        Membersihkan riwayat memori baca.
        """
        self.history.clear()
        self.normalized_history.clear()
