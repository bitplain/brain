from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "Инструкция_по_удаленному_рабочему_столу.pdf"
ICON_FILE = BASE_DIR / "rdp-icon.png"
LOGIN_FILE = BASE_DIR / "rdp-login.png"
FONT_PATH = Path("/Library/Fonts/Arial Unicode.ttf")
FONT_NAME = "ArialUnicode"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 42
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN


def register_font() -> None:
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"Font not found: {FONT_PATH}")
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))


def draw_wrapped_text(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y_top: float,
    max_width: float,
    font_size: int = 11,
    color=colors.HexColor("#1E293B"),
    leading: float | None = None,
):
    leading = leading or (font_size + 4)
    pdf.setFont(FONT_NAME, font_size)
    pdf.setFillColor(color)
    lines = simpleSplit(text, FONT_NAME, font_size, max_width)
    for index, line in enumerate(lines):
        pdf.drawString(x, y_top - index * leading, line)
    return y_top - len(lines) * leading


def draw_panel(
    pdf: canvas.Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    fill_color,
    title: str,
    body_lines: list[str],
):
    pdf.setFillColor(fill_color)
    pdf.setStrokeColor(fill_color)
    pdf.roundRect(x, y, width, height, 12, fill=1, stroke=0)

    pdf.setFillColor(colors.HexColor("#0F172A"))
    pdf.setFont(FONT_NAME, 14)
    pdf.drawString(x + 16, y + height - 24, title)

    cursor = y + height - 50
    for line in body_lines:
        cursor = draw_wrapped_text(
            pdf,
            f"• {line}",
            x + 16,
            cursor,
            width - 32,
            font_size=10,
            color=colors.HexColor("#334155"),
            leading=14,
        ) - 4


def draw_banner(pdf: canvas.Canvas) -> None:
    pdf.setFillColor(colors.HexColor("#0F4C81"))
    pdf.roundRect(MARGIN, PAGE_HEIGHT - 140, CONTENT_WIDTH, 98, 18, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont(FONT_NAME, 18)
    pdf.drawString(MARGIN + 24, PAGE_HEIGHT - 84, "Памятка по подключению")
    pdf.drawString(MARGIN + 24, PAGE_HEIGHT - 108, "к удаленному рабочему столу")

    draw_wrapped_text(
        pdf,
        "Эта инструкция поможет понять, где искать ярлык и что вводить при первом входе.",
        MARGIN + 24,
        PAGE_HEIGHT - 126,
        CONTENT_WIDTH - 48,
        font_size=9,
        color=colors.white,
        leading=11,
    )


def draw_notice(pdf: canvas.Canvas, y: float, text: str) -> None:
    pdf.setFillColor(colors.HexColor("#FFF7ED"))
    pdf.setStrokeColor(colors.HexColor("#FDBA74"))
    pdf.roundRect(MARGIN, y, CONTENT_WIDTH, 54, 14, fill=1, stroke=1)

    pdf.setFillColor(colors.HexColor("#9A3412"))
    pdf.setFont(FONT_NAME, 12)
    pdf.drawString(MARGIN + 16, y + 33, "Важно")
    draw_wrapped_text(
        pdf,
        text,
        MARGIN + 76,
        y + 33,
        CONTENT_WIDTH - 92,
        font_size=11,
        color=colors.HexColor("#7C2D12"),
        leading=13,
    )


def draw_page_one(pdf: canvas.Canvas) -> None:
    draw_banner(pdf)

    draw_notice(
        pdf,
        PAGE_HEIGHT - 198,
        "Ярлык удаленного подключения нужно искать на локальном рабочем столе вашего компьютера, "
        "а не внутри уже открытой удаленной сессии.",
    )

    pdf.setFillColor(colors.HexColor("#0F172A"))
    pdf.setFont(FONT_NAME, 16)
    pdf.drawString(MARGIN, PAGE_HEIGHT - 236, "Локальный и удаленный рабочий стол: в чем разница")

    panel_y = PAGE_HEIGHT - 426
    panel_width = (CONTENT_WIDTH - 20) / 2
    panel_height = 156

    draw_panel(
        pdf,
        MARGIN,
        panel_y,
        panel_width,
        panel_height,
        colors.HexColor("#ECFDF5"),
        "Локальный рабочий стол",
        [
            "Это экран вашего компьютера сразу после входа в Windows.",
            "Именно здесь находятся обычные ярлыки и файлы вашего ПК.",
            "Ярлык удаленного рабочего стола нужно запускать отсюда.",
        ],
    )
    draw_panel(
        pdf,
        MARGIN + panel_width + 20,
        panel_y,
        panel_width,
        panel_height,
        colors.HexColor("#EFF6FF"),
        "Удаленный рабочий стол",
        [
            "Это подключение к другому рабочему компьютеру или серверу.",
            "Он открывается после запуска ярлыка и ввода учетных данных.",
            "Если вы уже внутри него, вы смотрите не на локальный экран.",
        ],
    )

    pdf.setFillColor(colors.HexColor("#0F4C81"))
    pdf.setFont(FONT_NAME, 16)
    pdf.drawString(MARGIN, 350, "Шаг 1. Найдите нужный ярлык")

    pdf.setFillColor(colors.HexColor("#F8FAFC"))
    pdf.setStrokeColor(colors.HexColor("#CBD5E1"))
    pdf.roundRect(MARGIN, 160, CONTENT_WIDTH, 170, 14, fill=1, stroke=1)

    icon = ImageReader(str(ICON_FILE))
    pdf.drawImage(icon, MARGIN + 18, 184, width=110, height=90, preserveAspectRatio=True, mask="auto")

    pdf.setStrokeColor(colors.HexColor("#0F4C81"))
    pdf.setLineWidth(2)
    pdf.roundRect(MARGIN + 10, 176, 126, 106, 14, fill=0, stroke=1)

    pdf.setFillColor(colors.HexColor("#0F172A"))
    draw_wrapped_text(
        pdf,
        "Ищите на локальном рабочем столе значок удаленного рабочего стола, похожий на изображение слева.",
        MARGIN + 160,
        292,
        300,
        font_size=11,
        color=colors.HexColor("#0F172A"),
        leading=15,
    )

    draw_wrapped_text(
        pdf,
        "После нажатия на этот ярлык откроется окно ввода учетных данных для подключения.",
        MARGIN + 160,
        244,
        CONTENT_WIDTH - 188,
        font_size=11,
        color=colors.HexColor("#334155"),
        leading=14,
    )

    pdf.setFillColor(colors.HexColor("#E2E8F0"))
    pdf.roundRect(MARGIN + 160, 178, CONTENT_WIDTH - 186, 48, 10, fill=1, stroke=0)
    draw_wrapped_text(
        pdf,
        "Если такого ярлыка не видно, сначала проверьте, что вы на локальном рабочем столе.",
        MARGIN + 176,
        206,
        CONTENT_WIDTH - 220,
        font_size=11,
        color=colors.HexColor("#0F172A"),
        leading=14,
    )


def draw_page_two(pdf: canvas.Canvas) -> None:
    pdf.setFillColor(colors.HexColor("#0F4C81"))
    pdf.roundRect(MARGIN, PAGE_HEIGHT - 102, CONTENT_WIDTH, 58, 18, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont(FONT_NAME, 20)
    pdf.drawString(MARGIN + 22, PAGE_HEIGHT - 72, "Шаг 2. Введите учетные данные")

    draw_wrapped_text(
        pdf,
        "После запуска ярлыка откроется окно, как на примере ниже.",
        MARGIN,
        PAGE_HEIGHT - 126,
        CONTENT_WIDTH,
        font_size=12,
        color=colors.HexColor("#334155"),
        leading=14,
    )

    login = ImageReader(str(LOGIN_FILE))
    image_width = CONTENT_WIDTH
    image_height = image_width * (817 / 925)
    image_y = 250
    pdf.drawImage(login, MARGIN, image_y, width=image_width, height=image_height, preserveAspectRatio=True, mask="auto")

    pdf.setStrokeColor(colors.HexColor("#CBD5E1"))
    pdf.roundRect(MARGIN, image_y, image_width, image_height, 10, fill=0, stroke=1)

    bottom_y = 182
    pdf.setFillColor(colors.HexColor("#EEF2FF"))
    pdf.setStrokeColor(colors.HexColor("#C7D2FE"))
    pdf.roundRect(MARGIN, bottom_y, CONTENT_WIDTH, 120, 14, fill=1, stroke=1)

    pdf.setFillColor(colors.HexColor("#312E81"))
    pdf.setFont(FONT_NAME, 13)
    pdf.drawString(MARGIN + 16, bottom_y + 92, "Если вы запускаете удаленный рабочий стол впервые")
    draw_wrapped_text(
        pdf,
        "В поле имени пользователя введите учетную запись в формате: inf.co.fi\\пользователь",
        MARGIN + 16,
        bottom_y + 70,
        CONTENT_WIDTH - 32,
        font_size=12,
        color=colors.HexColor("#312E81"),
        leading=15,
    )

    pdf.setFillColor(colors.HexColor("#DCFCE7"))
    pdf.setStrokeColor(colors.HexColor("#86EFAC"))
    pdf.roundRect(MARGIN, 72, CONTENT_WIDTH, 86, 14, fill=1, stroke=1)

    pdf.setFillColor(colors.HexColor("#166534"))
    pdf.setFont(FONT_NAME, 13)
    pdf.drawString(MARGIN + 16, 130, "Если вы уже раньше подключались")
    draw_wrapped_text(
        pdf,
        "Имя пользователя обычно подставляется автоматически. Проверьте его, введите пароль и нажмите OK.",
        MARGIN + 16,
        108,
        CONTENT_WIDTH - 32,
        font_size=12,
        color=colors.HexColor("#166534"),
        leading=15,
    )


def build_pdf() -> None:
    register_font()

    if not ICON_FILE.exists():
        raise FileNotFoundError(f"Missing icon file: {ICON_FILE}")
    if not LOGIN_FILE.exists():
        raise FileNotFoundError(f"Missing login file: {LOGIN_FILE}")

    pdf = canvas.Canvas(str(OUTPUT_FILE), pagesize=A4)
    pdf.setTitle("Инструкция по удаленному рабочему столу")
    pdf.setAuthor("Codex")

    draw_page_one(pdf)
    pdf.showPage()
    draw_page_two(pdf)
    pdf.save()


if __name__ == "__main__":
    build_pdf()
