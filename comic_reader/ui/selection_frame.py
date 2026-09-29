"""
Jendela Pemilihan Bingkai Baca Komik (SelectionFrameWindow)
Mendukung pengaturan ukuran panjang (tinggi) dan lebar secara leluasa:
1. Menarik 4 tepi bingkai (Kiri, Kanan, Atas, Bawah) dan 4 sudut.
2. Tombol cepat pengatur panjang & lebar (+/- 50px) serta preset Webtoon/Komik di bilah atas.
"""

from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QCursor
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QFrame
)

from .comic_theme import (
    COMIC_YELLOW, COMIC_INK, COMIC_WHITE,
    COMIC_GREEN, COMIC_RED, QSS_COMIC_THEME
)
from ..models import ReadingZone

class SelectionFrameWindow(QWidget):
    started = pyqtSignal(dict)

    def __init__(self, initial_zone=None):
        super().__init__()
        self.zone = ReadingZone.from_dict(initial_zone)
        self.resizing = False
        self.moving = False
        self.resize_mode = None  # 'left', 'right', 'top', 'bottom', 'top_left', dst.
        self.drag_start_pos = QPoint()
        self.drag_start_geom = QRect()

        self.border_margin = 14  # Area tangkap kursor untuk resize di setiap tepi
        self.header_height = 52

        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet(QSS_COMIC_THEME)
        self.setMouseTracking(True)

        x = self.zone.x
        y = self.zone.y
        w = self.zone.width
        h = self.zone.height
        self.setGeometry(x, y, w, h)

        # Bilah kontrol atas
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.top_bar = QWidget(self)
        self.top_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {COMIC_YELLOW};
                border: 3px solid {COMIC_INK};
                border-radius: 8px;
            }}
        """)
        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(8, 6, 8, 6)
        top_layout.setSpacing(6)

        title = QLabel("ATUR BINGKAI")
        title.setFont(QFont("Arial Black", 10, QFont.Weight.Bold))
        title.setStyleSheet("border: none; color: #18181B;")
        top_layout.addWidget(title)

        # Indikator Ukuran Aktif
        self.lbl_size = QLabel(f"{w} x {h}")
        self.lbl_size.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.lbl_size.setStyleSheet(f"""
            background-color: {COMIC_WHITE};
            border: 2px solid {COMIC_INK};
            border-radius: 4px;
            padding: 2px 6px;
        """)
        top_layout.addWidget(self.lbl_size)

        # Tombol Atur Lebar
        btn_w_minus = QPushButton("-L")
        btn_w_minus.setToolTip("Kurangi Lebar (-50px)")
        btn_w_minus.setFixedSize(32, 28)
        btn_w_minus.clicked.connect(lambda: self.adjust_size(dw=-50, dh=0))
        top_layout.addWidget(btn_w_minus)

        btn_w_plus = QPushButton("+L")
        btn_w_plus.setToolTip("Tambah Lebar (+50px)")
        btn_w_plus.setFixedSize(32, 28)
        btn_w_plus.clicked.connect(lambda: self.adjust_size(dw=50, dh=0))
        top_layout.addWidget(btn_w_plus)

        # Tombol Atur Panjang/Tinggi
        btn_h_minus = QPushButton("-P")
        btn_h_minus.setToolTip("Kurangi Panjang/Tinggi (-50px)")
        btn_h_minus.setFixedSize(32, 28)
        btn_h_minus.clicked.connect(lambda: self.adjust_size(dw=0, dh=-50))
        top_layout.addWidget(btn_h_minus)

        btn_h_plus = QPushButton("+P")
        btn_h_plus.setToolTip("Tambah Panjang/Tinggi (+50px)")
        btn_h_plus.setFixedSize(32, 28)
        btn_h_plus.clicked.connect(lambda: self.adjust_size(dw=0, dh=50))
        top_layout.addWidget(btn_h_plus)

        top_layout.addStretch()

        # Tombol Mulai Baca
        self.btn_start = QPushButton("MULAI BACA")
        self.btn_start.setObjectName("btnAction")
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.clicked.connect(self.on_start_clicked)
        top_layout.addWidget(self.btn_start)

        layout.addWidget(self.top_bar)
        layout.addStretch()

    def adjust_size(self, dw: int, dh: int):
        """Menambah atau mengurangi ukuran lebar dan tinggi secara langsung"""
        geom = self.geometry()
        new_w = max(250, geom.width() + dw)
        new_h = max(250, geom.height() + dh)
        self.resize(new_w, new_h)
        self.lbl_size.setText(f"{new_w} x {new_h}")

    def on_start_clicked(self):
        geom = self.geometry()
        current_zone = {
            "x": geom.x() + 8,
            "y": geom.y() + self.header_height + 8,
            "width": max(150, geom.width() - 16),
            "height": max(150, geom.height() - self.header_height - 16)
        }
        self.zone = current_zone
        self.hide()
        self.started.emit(current_zone)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        # Garis batas luar tinta hitam tebal
        painter.setPen(QPen(QColor(COMIC_INK), 4))
        painter.setBrush(QBrush(QColor(0, 0, 0, 10))) # Sangat bening di dalam
        painter.drawRect(rect.adjusted(2, 2, -2, -2))

        # Garis strip komik kuning putus-putus
        painter.setPen(QPen(QColor(COMIC_YELLOW), 2, Qt.PenStyle.DashLine))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(rect.adjusted(6, 6, -6, -6))

        # Handle di 4 sudut dan tengah tepi untuk menandakan area bisa ditarik
        painter.setPen(QPen(QColor(COMIC_INK), 2))
        painter.setBrush(QBrush(QColor(COMIC_YELLOW)))

        m = 16
        # Sudut
        painter.drawRect(0, 0, m, m)
        painter.drawRect(rect.width() - m, 0, m, m)
        painter.drawRect(0, rect.height() - m, m, m)
        painter.drawRect(rect.width() - m, rect.height() - m, m, m)

        # Handle tengah tepi (menandakan bisa tarik panjang/lebar)
        mid_x = rect.width() // 2 - m // 2
        mid_y = rect.height() // 2 - m // 2
        painter.drawRect(mid_x, 0, m, 8)  # Tengah atas
        painter.drawRect(mid_x, rect.height() - 8, m, 8)  # Tengah bawah
        painter.drawRect(0, mid_y, 8, m)  # Tengah kiri
        painter.drawRect(rect.width() - 8, mid_y, 8, m)  # Tengah kanan

    def _determine_resize_mode(self, pos: QPoint) -> str:
        """Menentukan apakah kursor berada di tepi kiri, kanan, atas, bawah, atau sudut"""
        w = self.width()
        h = self.height()
        m = self.border_margin

        on_left = pos.x() <= m
        on_right = pos.x() >= w - m
        on_top = pos.y() <= m
        on_bottom = pos.y() >= h - m

        if on_top and on_left:
            return "top_left"
        if on_top and on_right:
            return "top_right"
        if on_bottom and on_left:
            return "bottom_left"
        if on_bottom and on_right:
            return "bottom_right"
        if on_left:
            return "left"
        if on_right:
            return "right"
        if on_top:
            return "top"
        if on_bottom:
            return "bottom"
        return "none"

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mode = self._determine_resize_mode(event.pos())
            self.drag_start_pos = event.globalPosition().toPoint()
            self.drag_start_geom = self.geometry()

            if mode != "none":
                self.resizing = True
                self.resize_mode = mode
            else:
                self.moving = True
            event.accept()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        global_pos = event.globalPosition().toPoint()

        if self.resizing:
            delta = global_pos - self.drag_start_pos
            orig = self.drag_start_geom
            new_x = orig.x()
            new_y = orig.y()
            new_w = orig.width()
            new_h = orig.height()

            # Atur Lebar (Kiri atau Kanan)
            if "right" in self.resize_mode:
                new_w = max(250, orig.width() + delta.x())
            elif "left" in self.resize_mode:
                diff = delta.x()
                if orig.width() - diff >= 250:
                    new_x = orig.x() + diff
                    new_w = orig.width() - diff

            # Atur Panjang / Tinggi (Atas atau Bawah)
            if "bottom" in self.resize_mode:
                new_h = max(250, orig.height() + delta.y())
            elif "top" in self.resize_mode:
                diff = delta.y()
                if orig.height() - diff >= 250:
                    new_y = orig.y() + diff
                    new_h = orig.height() - diff

            self.setGeometry(new_x, new_y, new_w, new_h)
            self.lbl_size.setText(f"{new_w} x {new_h}")
            event.accept()

        elif self.moving:
            delta = global_pos - self.drag_start_pos
            self.move(self.drag_start_geom.topLeft() + delta)
            event.accept()

        else:
            # Perbarui ikon kursor mouse sesuai posisi tepi yang disentuh
            mode = self._determine_resize_mode(pos)
            if mode in ("left", "right"):
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            elif mode in ("top", "bottom"):
                self.setCursor(Qt.CursorShape.SizeVerCursor)
            elif mode in ("top_left", "bottom_right"):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif mode in ("top_right", "bottom_left"):
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.SizeAllCursor)

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.moving = False
        self.resize_mode = "none"
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def reposition_to_zone(self, zone):
        """Memposisikan ulang bingkai seleksi secara terenkapsulasi."""
        if hasattr(zone, "to_dict"):
            zone = zone.to_dict()
        zone_dict = zone or {}
        new_x = max(0, zone_dict.get("x", 350) - 8)
        new_y = max(0, zone_dict.get("y", 100) - self.header_height - 8)
        new_w = zone_dict.get("width", 650) + 16
        new_h = zone_dict.get("height", 850) + self.header_height + 16

        self.setGeometry(new_x, new_y, new_w, new_h)
        if hasattr(self, "lbl_size"):
            self.lbl_size.setText(f"{new_w} x {new_h}")
        self.show()
        self.raise_()

    def keyPressEvent(self, event):
        """Dukungan shortcut keyboard untuk resize cepat dan konfirmasi."""
        key = event.key()
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            self.on_start_clicked()
            event.accept()
        elif key == Qt.Key.Key_Escape:
            self.hide()
            event.accept()
        elif key == Qt.Key.Key_Left:
            self.adjust_size(dw=-20, dh=0)
            event.accept()
        elif key == Qt.Key.Key_Right:
            self.adjust_size(dw=20, dh=0)
            event.accept()
        elif key == Qt.Key.Key_Up:
            self.adjust_size(dw=0, dh=-20)
            event.accept()
        elif key == Qt.Key.Key_Down:
            self.adjust_size(dw=0, dh=20)
            event.accept()
        else:
            super().keyPressEvent(event)

