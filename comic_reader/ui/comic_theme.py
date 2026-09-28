"""
Tema Antarmuka Bergaya Komik (Pop Comic Art Style)
Menghadirkan gaya visual buku komik:
- Garis tepi tebal tinta hitam (bold solid ink borders)
- Bayangan pekat tanpa blur (hard offset drop shadow)
- Palet warna: Comic Yellow (#FFE135), Ink Black (#111111), Action Red (#FF4747), Panel White (#FFFFFF)
- Tipografi tegas bergaya buku komik
"""

COMIC_YELLOW = "#FFE135"
COMIC_YELLOW_HOVER = "#FFF066"
COMIC_INK = "#18181B"
COMIC_WHITE = "#FFFFFF"
COMIC_RED = "#FF4747"
COMIC_RED_HOVER = "#FF6B6B"
COMIC_GREEN = "#10B981"
COMIC_GREEN_HOVER = "#34D399"
COMIC_GRAY = "#E4E4E7"
COMIC_DARK_GRAY = "#27272A"

QSS_COMIC_THEME = f"""
QWidget {{
    font-family: 'Segoe UI', 'Impact', 'Arial Black', sans-serif;
    color: {COMIC_INK};
}}

/* Tombol Gaya Komik */
QPushButton {{
    background-color: {COMIC_YELLOW};
    color: {COMIC_INK};
    border: 3px solid {COMIC_INK};
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 900;
    font-size: 13px;
    margin-right: 3px;
    margin-bottom: 3px;
}}

QPushButton:hover {{
    background-color: {COMIC_YELLOW_HOVER};
}}

QPushButton:pressed {{
    background-color: #E5C720;
    margin-top: 3px;
    margin-left: 3px;
    margin-right: 0px;
    margin-bottom: 0px;
}}

QPushButton#btnDanger {{
    background-color: {COMIC_RED};
    color: {COMIC_WHITE};
}}

QPushButton#btnDanger:hover {{
    background-color: {COMIC_RED_HOVER};
}}

QPushButton#btnAction {{
    background-color: {COMIC_GREEN};
    color: {COMIC_WHITE};
    font-size: 14px;
}}

QPushButton#btnAction:hover {{
    background-color: {COMIC_GREEN_HOVER};
}}

/* Slider Gaya Komik */
QSlider::groove:horizontal {{
    border: 2px solid {COMIC_INK};
    height: 10px;
    background: {COMIC_WHITE};
    border-radius: 5px;
}}

QSlider::sub-page:horizontal {{
    background: {COMIC_YELLOW};
    border: 2px solid {COMIC_INK};
    border-radius: 5px;
}}

QSlider::handle:horizontal {{
    background: {COMIC_RED};
    border: 2px solid {COMIC_INK};
    width: 22px;
    margin-top: -7px;
    margin-bottom: -7px;
    border-radius: 11px;
}}

QSlider::handle:horizontal:hover {{
    background: {COMIC_RED_HOVER};
}}

/* ComboBox Gaya Komik */
QComboBox {{
    background-color: {COMIC_WHITE};
    border: 3px solid {COMIC_INK};
    border-radius: 8px;
    padding: 6px 12px;
    font-weight: 800;
    font-size: 12px;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 2px solid {COMIC_INK};
    background-color: {COMIC_YELLOW};
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}}

QComboBox QAbstractItemView {{
    background-color: {COMIC_WHITE};
    border: 3px solid {COMIC_INK};
    selection-background-color: {COMIC_YELLOW};
    selection-color: {COMIC_INK};
    font-weight: 700;
    padding: 4px;
}}

/* Label Gaya Komik */
QLabel {{
    font-weight: 800;
    font-size: 12px;
}}

QLabel#titleLabel {{
    font-size: 15px;
    font-weight: 900;
    color: {COMIC_INK};
}}

QLabel#badgeLabel {{
    background-color: {COMIC_YELLOW};
    border: 2px solid {COMIC_INK};
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 900;
}}
"""
