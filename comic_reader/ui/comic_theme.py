"""
Sistem Desain & Tema Semantik untuk ComicVoice Reader (Pro-UI Standard)
Menerapkan Semantic Token Matrix yang mendukung tema visual:
1. Pop Comic / Neobrutalism (Default): Border tebal tinta komik, aksen kuning cerah, dan umpan balik taktil.
2. Dark Obsidian: Antarmuka gelap minimalis produktif dengan aksen indigo tenang.
3. Light Precision: Tampilan monokrom bersih dengan kontras tinggi.
"""

from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class ThemeTokens:
    surface_canvas: str
    surface_panel: str
    surface_card: str
    border_color: str
    border_width: str
    accent_primary: str
    accent_hover: str
    accent_pressed: str
    action_color: str
    action_hover: str
    danger_color: str
    danger_hover: str
    text_primary: str
    text_secondary: str
    radius_base: str
    radius_pill: str
    font_family: str

# 1. Preset Tema: Pop Comic (Neobrutalism)
POP_COMIC_THEME = ThemeTokens(
    surface_canvas="transparent",
    surface_panel="#FFFFFF",
    surface_card="#FFE135",
    border_color="#18181B",
    border_width="3px",
    accent_primary="#FFE135",
    accent_hover="#FFF066",
    accent_pressed="#E5C720",
    action_color="#10B981",
    action_hover="#34D399",
    danger_color="#FF4747",
    danger_hover="#FF6B6B",
    text_primary="#18181B",
    text_secondary="#52525B",
    radius_base="8px",
    radius_pill="9999px",
    font_family="'Segoe UI', 'Impact', 'Arial Black', sans-serif"
)

# 2. Preset Tema: Dark Obsidian (Minimalist Pro)
DARK_OBSIDIAN_THEME = ThemeTokens(
    surface_canvas="transparent",
    surface_panel="#121316",
    surface_card="#18191E",
    border_color="#2E3039",
    border_width="1px",
    accent_primary="#5E6AD2",
    accent_hover="#707CE6",
    accent_pressed="#4E58B2",
    action_color="#10B981",
    action_hover="#059669",
    danger_color="#EF4444",
    danger_hover="#DC2626",
    text_primary="#F3F4F6",
    text_secondary="#9CA3AF",
    radius_base="6px",
    radius_pill="9999px",
    font_family="'Segoe UI', -apple-system, sans-serif"
)

# 3. Preset Tema: Light Precision (Editorial Clean)
LIGHT_PRECISION_THEME = ThemeTokens(
    surface_canvas="transparent",
    surface_panel="#FFFFFF",
    surface_card="#FAFAFA",
    border_color="#E5E7EB",
    border_width="1px",
    accent_primary="#18181B",
    accent_hover="#27272A",
    accent_pressed="#09090B",
    action_color="#059669",
    action_hover="#047857",
    danger_color="#DC2626",
    danger_hover="#B91C1C",
    text_primary="#18181B",
    text_secondary="#6B7280",
    radius_base="6px",
    radius_pill="9999px",
    font_family="'Segoe UI', -apple-system, sans-serif"
)

def build_qss(tokens: ThemeTokens) -> str:
    """Menghasilkan stylesheet Qt (QSS) berbasis token semantik."""
    return f"""
QWidget {{
    font-family: {tokens.font_family};
    color: {tokens.text_primary};
}}

/* Tombol Komponen Utama dengan 5 Status Lengkap */
QPushButton {{
    background-color: {tokens.accent_primary};
    color: {tokens.text_primary};
    border: {tokens.border_width} solid {tokens.border_color};
    border-radius: {tokens.radius_base};
    padding: 8px 14px;
    font-weight: 800;
    font-size: 13px;
    margin-right: 2px;
    margin-bottom: 2px;
}}

QPushButton:hover {{
    background-color: {tokens.accent_hover};
}}

QPushButton:pressed {{
    background-color: {tokens.accent_pressed};
    margin-top: 2px;
    margin-left: 2px;
    margin-right: 0px;
    margin-bottom: 0px;
}}

QPushButton:focus-visible {{
    outline: 2px solid {tokens.accent_primary};
    outline-offset: 2px;
}}

QPushButton:disabled {{
    background-color: #E4E4E7;
    color: #A1A1AA;
    border-color: #D4D4D8;
}}

/* Variasi Tombol Danger (Merah) */
QPushButton#btnDanger {{
    background-color: {tokens.danger_color};
    color: #FFFFFF;
}}

QPushButton#btnDanger:hover {{
    background-color: {tokens.danger_hover};
}}

/* Variasi Tombol Action Utama (Hijau) */
QPushButton#btnAction {{
    background-color: {tokens.action_color};
    color: #FFFFFF;
    font-size: 14px;
}}

QPushButton#btnAction:hover {{
    background-color: {tokens.action_hover};
}}

/* Slider Kontrol Presisi */
QSlider::groove:horizontal {{
    border: 2px solid {tokens.border_color};
    height: 8px;
    background: {tokens.surface_panel};
    border-radius: 4px;
}}

QSlider::sub-page:horizontal {{
    background: {tokens.accent_primary};
    border: 2px solid {tokens.border_color};
    border-radius: 4px;
}}

QSlider::handle:horizontal {{
    background: {tokens.danger_color};
    border: 2px solid {tokens.border_color};
    width: 20px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: 10px;
}}

QSlider::handle:horizontal:hover {{
    background: {tokens.danger_hover};
}}

/* Dropdown Menu (QComboBox) */
QComboBox {{
    background-color: {tokens.surface_panel};
    color: {tokens.text_primary};
    border: {tokens.border_width} solid {tokens.border_color};
    border-radius: {tokens.radius_base};
    padding: 6px 12px;
    font-weight: 700;
    font-size: 12px;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 26px;
    border-left: 2px solid {tokens.border_color};
    background-color: {tokens.accent_primary};
    border-top-right-radius: {tokens.radius_base};
    border-bottom-right-radius: {tokens.radius_base};
}}

QComboBox QAbstractItemView {{
    background-color: {tokens.surface_panel};
    color: {tokens.text_primary};
    border: {tokens.border_width} solid {tokens.border_color};
    selection-background-color: {tokens.accent_primary};
    selection-color: {tokens.text_primary};
    font-weight: 700;
    padding: 4px;
}}

/* Label Tipografi Semantik */
QLabel {{
    font-weight: 700;
    font-size: 12px;
    color: {tokens.text_primary};
}}

QLabel#titleLabel {{
    font-size: 14px;
    font-weight: 900;
    color: {tokens.text_primary};
}}

QLabel#badgeLabel {{
    background-color: {tokens.accent_primary};
    color: {tokens.text_primary};
    border: 2px solid {tokens.border_color};
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 800;
}}
"""

# Kompatibilitas konstanta lama untuk kode yang mengimpor langsung
COMIC_YELLOW = POP_COMIC_THEME.accent_primary
COMIC_YELLOW_HOVER = POP_COMIC_THEME.accent_hover
COMIC_INK = POP_COMIC_THEME.border_color
COMIC_WHITE = POP_COMIC_THEME.surface_panel
COMIC_RED = POP_COMIC_THEME.danger_color
COMIC_RED_HOVER = POP_COMIC_THEME.danger_hover
COMIC_GREEN = POP_COMIC_THEME.action_color
COMIC_GREEN_HOVER = POP_COMIC_THEME.action_hover
COMIC_GRAY = "#E4E4E7"
COMIC_DARK_GRAY = "#27272A"

QSS_COMIC_THEME = build_qss(POP_COMIC_THEME)
QSS_DARK_OBSIDIAN = build_qss(DARK_OBSIDIAN_THEME)
QSS_LIGHT_PRECISION = build_qss(LIGHT_PRECISION_THEME)
