"""
Widget Balon Suara Mengambang (FloatingBubbleWidget)
Always on top, dapat digeser ke mana saja di layar.
Klik balon akan membuka/menutup panel kontrol komik popout.
"""

from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QPolygon
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSlider, QComboBox, QFrame, QApplication
)

from .comic_theme import (
    COMIC_YELLOW, COMIC_INK, COMIC_WHITE,
    COMIC_RED, COMIC_GREEN, QSS_COMIC_THEME
)
from ..config import AVAILABLE_VOICES

class ComicControlPanel(QWidget):
    """
    Panel pengaturan popout bergaya komik yang muncul saat balon suara diklik.
    """
    frame_reset_requested = pyqtSignal()
    voice_changed = pyqtSignal(int)
    speed_changed = pyqtSignal(float)
    volume_changed = pyqtSignal(float)
    pause_toggled = pyqtSignal()
    cache_clear_requested = pyqtSignal()
    instant_read_requested = pyqtSignal()
    quit_requested = pyqtSignal()

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.is_paused = False
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet(QSS_COMIC_THEME)
        self.setFixedWidth(320)

        # Container berlatar komik putih dengan border hitam
        container = QWidget(self)
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {COMIC_WHITE};
                border: 3px solid {COMIC_INK};
                border-radius: 12px;
            }}
        """)
        panel_layout = QVBoxLayout(container)
        panel_layout.setContentsMargins(14, 14, 14, 14)
        panel_layout.setSpacing(10)

        # Header Komik
        header = QHBoxLayout()
        title_badge = QLabel("KONTROL SUARA KOMIK")
        title_badge.setFont(QFont("Arial Black", 11, QFont.Weight.Bold))
        title_badge.setStyleSheet(f"""
            background-color: {COMIC_YELLOW};
            border: 2px solid {COMIC_INK};
            border-radius: 6px;
            padding: 3px 8px;
            color: {COMIC_INK};
        """)

        btn_close = QPushButton("X")
        btn_close.setFixedSize(28, 28)
        btn_close.setObjectName("btnDanger")
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.hide)

        header.addWidget(title_badge)
        header.addStretch()
        header.addWidget(btn_close)
        panel_layout.addLayout(header)

        # Label status pembacaan
        self.lbl_status = QLabel("Status: Memantau Gulir...")
        self.lbl_status.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.lbl_status.setStyleSheet(f"color: {COMIC_INK}; border: none; padding: 2px;")
        panel_layout.addWidget(self.lbl_status)

        # Garis pemisah komik
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"background-color: {COMIC_INK}; max-height: 2px; border: none;")
        panel_layout.addWidget(line)

        # 1. Pilihan Suara
        voice_label = QLabel("PILIHAN SUARA (3 KARAKTER):")
        voice_label.setFont(QFont("Arial Black", 9))
        voice_label.setStyleSheet("border: none;")
        panel_layout.addWidget(voice_label)

        self.cb_voices = QComboBox()
        for v in AVAILABLE_VOICES:
            self.cb_voices.addItem(f"{v['name']}")
        current_v = self.config.get("voice_index", 0)
        self.cb_voices.setCurrentIndex(current_v)
        self.cb_voices.currentIndexChanged.connect(self.on_voice_changed)
        panel_layout.addWidget(self.cb_voices)

        # 2. Pengatur Kecepatan Baca
        speed_header = QHBoxLayout()
        lbl_speed = QLabel("KECEPATAN BACA:")
        lbl_speed.setFont(QFont("Arial Black", 9))
        lbl_speed.setStyleSheet("border: none;")
        self.lbl_speed_val = QLabel(f"{self.config.get('speed', 1.0):.1f}x")
        self.lbl_speed_val.setFont(QFont("Arial Black", 9))
        self.lbl_speed_val.setStyleSheet("border: none; color: #D97706;")
        speed_header.addWidget(lbl_speed)
        speed_header.addStretch()
        speed_header.addWidget(self.lbl_speed_val)
        panel_layout.addLayout(speed_header)

        self.slider_speed = QSlider(Qt.Orientation.Horizontal)
        self.slider_speed.setRange(5, 20)  # 0.5x sampai 2.0x
        current_spd = int(round(self.config.get("speed", 1.0) * 10))
        self.slider_speed.setValue(current_spd)
        self.slider_speed.valueChanged.connect(self.on_speed_changed)
        panel_layout.addWidget(self.slider_speed)

        # 3. Pengatur Volume
        vol_header = QHBoxLayout()
        lbl_vol = QLabel("VOLUME SUARA:")
        lbl_vol.setFont(QFont("Arial Black", 9))
        lbl_vol.setStyleSheet("border: none;")
        self.lbl_vol_val = QLabel(f"{int(self.config.get('volume', 1.0) * 100)}%")
        self.lbl_vol_val.setFont(QFont("Arial Black", 9))
        self.lbl_vol_val.setStyleSheet("border: none; color: #2563EB;")
        vol_header.addWidget(lbl_vol)
        vol_header.addStretch()
        vol_header.addWidget(self.lbl_vol_val)
        panel_layout.addLayout(vol_header)

        self.slider_vol = QSlider(Qt.Orientation.Horizontal)
        self.slider_vol.setRange(0, 100)
        current_vol = int(round(self.config.get("volume", 1.0) * 100))
        self.slider_vol.setValue(current_vol)
        self.slider_vol.valueChanged.connect(self.on_volume_changed)
        panel_layout.addWidget(self.slider_vol)

        # Garis pemisah
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet(f"background-color: {COMIC_INK}; max-height: 2px; border: none;")
        panel_layout.addWidget(line2)

        # 4. Tombol Aksi Komik
        self.btn_reset_frame = QPushButton("ATUR ULANG BINGKAI")
        self.btn_reset_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reset_frame.clicked.connect(self.on_reset_frame_clicked)
        panel_layout.addWidget(self.btn_reset_frame)

        btn_row = QHBoxLayout()
        self.btn_pause = QPushButton("JEDA")
        self.btn_pause.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_pause.clicked.connect(self.on_pause_clicked)

        self.btn_read_now = QPushButton("BACA SEKARANG")
        self.btn_read_now.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_read_now.clicked.connect(self.instant_read_requested.emit)

        btn_row.addWidget(self.btn_pause)
        btn_row.addWidget(self.btn_read_now)
        panel_layout.addLayout(btn_row)

        btn_row2 = QHBoxLayout()
        self.btn_clear = QPushButton("RESET RIWAYAT")
        self.btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear.clicked.connect(self.cache_clear_requested.emit)

        self.btn_quit = QPushButton("KELUAR")
        self.btn_quit.setObjectName("btnDanger")
        self.btn_quit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_quit.clicked.connect(self.quit_requested.emit)

        btn_row2.addWidget(self.btn_clear)
        btn_row2.addWidget(self.btn_quit)
        panel_layout.addLayout(btn_row2)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(container)

    def on_voice_changed(self, idx):
        self.voice_changed.emit(idx)

    def on_speed_changed(self, val):
        speed_float = val / 10.0
        self.lbl_speed_val.setText(f"{speed_float:.1f}x")
        self.speed_changed.emit(speed_float)

    def on_volume_changed(self, val):
        vol_float = val / 100.0
        self.lbl_vol_val.setText(f"{val}%")
        self.volume_changed.emit(vol_float)

    def on_reset_frame_clicked(self):
        self.hide()
        self.frame_reset_requested.emit()

    def on_pause_clicked(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.btn_pause.setText("LANJUT")
            self.lbl_status.setText("Status: Dijeda Sementara")
        else:
            self.btn_pause.setText("JEDA")
            self.lbl_status.setText("Status: Memantau Gulir...")
        self.pause_toggled.emit()

    def set_status_text(self, text: str):
        clean_text = text.strip()
        if "Membaca" in clean_text:
            bg_color = COMIC_GREEN
            txt_color = "#FFFFFF"
        elif "Dijeda" in clean_text:
            bg_color = "#F59E0B"
            txt_color = "#FFFFFF"
        elif "Gangguan" in clean_text or "Error" in clean_text:
            bg_color = COMIC_RED
            txt_color = "#FFFFFF"
        else:
            bg_color = COMIC_YELLOW
            txt_color = COMIC_INK

        self.lbl_status.setText(f"Status: {clean_text}")
        self.lbl_status.setStyleSheet(f"""
            background-color: {bg_color};
            color: {txt_color};
            border: 2px solid {COMIC_INK};
            border-radius: 6px;
            padding: 4px 8px;
            font-weight: 800;
        """)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
            event.accept()
        elif event.key() == Qt.Key.Key_Space:
            self.on_pause_clicked()
            event.accept()
        else:
            super().keyPressEvent(event)


class FloatingBubbleWidget(QWidget):
    """
    Balon suara mengambang bergaya buku komik (Always on Top).
    Dapat digeser bebas di layar desktop.
    Klik kiri membuka panel kontrol.
    """
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.drag_position = QPoint()
        self.is_speaking = False

        self.init_ui()

        # Panel kontrol
        self.control_panel = ComicControlPanel(self.config)

        # Timer animasi efek suara bergetar saat berbicara
        self.pulse_timer = QTimer(self)
        self.pulse_timer.timeout.connect(self._on_pulse)
        self.pulse_step = 0

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(74, 74)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Posisi awal di kanan atas layar
        self.move(1100, 150)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Gambar Bayangan Keras (Comic Drop Shadow)
        shadow_brush = QBrush(QColor(COMIC_INK))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(shadow_brush)
        painter.drawEllipse(7, 7, 56, 56)

        # Warna isi balon (kuning saat santai, hijau aksi saat membaca dialog)
        fill_color = COMIC_GREEN if self.is_speaking else COMIC_YELLOW
        painter.setBrush(QBrush(QColor(fill_color)))
        painter.setPen(QPen(QColor(COMIC_INK), 3))
        painter.drawEllipse(3, 3, 56, 56)

        # Ekor balon dialog komik kecil di sisi kiri bawah
        triangle = QPolygon([
            QPoint(12, 48),
            QPoint(2, 64),
            QPoint(24, 54)
        ])
        painter.setBrush(QBrush(QColor(fill_color)))
        painter.setPen(QPen(QColor(COMIC_INK), 2.5))
        painter.drawPolygon(triangle)

        # Ikon Pengeras Suara Komik
        painter.setPen(QPen(QColor(COMIC_INK), 2.5))
        painter.setBrush(QBrush(QColor(COMIC_INK)))

        # Badan speaker
        speaker_rect = QPolygon([
            QPoint(20, 27),
            QPoint(27, 27),
            QPoint(36, 19),
            QPoint(36, 43),
            QPoint(27, 35),
            QPoint(20, 35)
        ])
        painter.drawPolygon(speaker_rect)

        # Gelombang suara (arcs)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawArc(35, 23, 12, 16, -60 * 16, 120 * 16)
        if self.is_speaking:
            # Gelombang luar tambahan saat aktif bersuara
            painter.setPen(QPen(QColor(COMIC_RED), 3))
            painter.drawArc(38, 17, 18, 28, -60 * 16, 120 * 16)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            screen = self.screen() or QApplication.primaryScreen()
            if screen:
                geom = screen.availableGeometry()
                safe_x = max(geom.left(), min(new_pos.x(), geom.right() - self.width()))
                safe_y = max(geom.top(), min(new_pos.y(), geom.bottom() - self.height()))
                self.move(safe_x, safe_y)
            else:
                self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        # Jika perpindahan sangat kecil (klik), toggle panel kontrol
        if (event.globalPosition().toPoint() - self.frameGeometry().topLeft() - self.drag_position).manhattanLength() < 5:
            self.toggle_control_panel()
        event.accept()

    def toggle_control_panel(self):
        if self.control_panel.isVisible():
            self.control_panel.hide()
        else:
            # Posisikan panel di samping kiri atau kanan balon
            bubble_pos = self.pos()
            panel_x = max(10, bubble_pos.x() - 330)
            panel_y = max(10, bubble_pos.y())
            self.control_panel.move(panel_x, panel_y)
            self.control_panel.show()
            self.control_panel.raise_()

    def set_speaking_state(self, speaking: bool):
        self.is_speaking = speaking
        if speaking:
            self.pulse_timer.start(150)
            self.control_panel.set_status_text("Sedang Membaca Dialog...")
        else:
            self.pulse_timer.stop()
            self.control_panel.set_status_text("Memantau Gulir...")
        self.update()

    def _on_pulse(self):
        self.pulse_step = (self.pulse_step + 1) % 2
        self.update()

    def closeEvent(self, event):
        self.control_panel.close()
        super().closeEvent(event)
