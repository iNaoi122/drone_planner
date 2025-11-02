from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime
import base64
from io import BytesIO


def register_cyrillic_fonts():
    try:
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
        return 'Arial'
    except:
        try:
            pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
            return 'DejaVuSans'
        except:
            return 'Helvetica'


def generate_drone_cert_simple(image_path, hull_number, owner, drone_title, model_title=None):
    if not image_path or not hull_number or not owner:
        raise ValueError("Image path, hull number, and owner are required")

    font_name = register_cyrillic_fonts()
    buffer = BytesIO()

    page_size = landscape(A4)
    width, height = page_size

    c = canvas.Canvas(buffer, pagesize=page_size)

    c.setFillColor(HexColor('#667eea'))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    cert_margin = 20 * mm
    cert_width = width - 2 * cert_margin
    cert_height = height - 2 * cert_margin

    c.setFillColor(colors.white)
    c.roundRect(cert_margin, cert_margin, cert_width, cert_height, 10 * mm, fill=1, stroke=0)

    c.setFont(f"{font_name}-Bold", 28)
    c.setFillColor(HexColor('#667eea'))
    c.drawCentredString(width / 2, height - 80, "СЕРТИФИКАТ РЕГИСТРАЦИИ БПЛА")

    c.setFont(font_name, 14)
    c.setFillColor(HexColor('#666666'))
    c.drawCentredString(width / 2, height - 110,
                        "Удостоверение регистрации беспилотного летательного аппарата")

    content_start_y = height - 150
    content_end_y = 100

    try:
        img = ImageReader(image_path)

        img_width_orig, img_height_orig = img.getSize()
        img_ratio = img_width_orig / img_height_orig

        max_img_height = 60 * mm
        max_img_width = 80 * mm

        img_height = min(max_img_height, max_img_width / img_ratio)
        img_width = img_height * img_ratio

        if img_width > max_img_width:
            img_width = max_img_width
            img_height = img_width / img_ratio

        img_x = width / 2 - img_width / 2
        img_y = content_start_y - 30 * mm - img_height

        c.drawImage(img, img_x, img_y, width=img_width, height=img_height, mask='auto')
        img_y_position = img_y

    except Exception as e:
        print(f"Error loading image: {e}")
        img_y_position = content_start_y - 30 * mm

    fields = [
        ("Бортовой номер:", hull_number),
        ("Название:", drone_title),
        ("Владелец:", owner),
        ("Дата выдачи:", datetime.now().strftime("%d.%m.%Y"))
    ]

    if model_title:
        fields.insert(2, ("Модель:", model_title))

    if img_y_position:
        info_start_y = img_y_position - 30 * mm  # Space below image
    else:
        info_start_y = content_start_y - 100 * mm

    min_info_y = content_end_y + len(fields) * 25 + 20
    info_start_y = max(info_start_y, min_info_y)

    for i, (label, value) in enumerate(fields):
        y_pos = info_start_y - (i * 25)

        c.setFillColor(HexColor('#667eea'))
        c.setFont(f"{font_name}-Bold", 12)
        c.drawString(80 * mm, y_pos, label)

        c.setFillColor(colors.black)
        c.setFont(font_name, 12)

        value_x = 200 * mm
        c.drawString(value_x, y_pos, value)

    c.setFillColor(HexColor('#666666'))
    c.setFont(font_name, 10)

    footer_y1 = 60
    footer_y2 = 45

    last_field_y = info_start_y - (len(fields) * 25)
    if last_field_y < footer_y1 + 20:
        footer_y1 = max(30, last_field_y - 20)
        footer_y2 = footer_y1 - 15

    c.drawCentredString(width / 2, footer_y1,
                        "Данный сертификат подтверждает регистрацию беспилотного летательного аппарата")
    c.drawCentredString(width / 2, footer_y2,
                        "в системе учета и управления дронами")

    c.showPage()
    c.save()

    buffer.seek(0)
    pdf_bytes = buffer.getvalue()
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    return pdf_base64


# Пример использования
if __name__ == "__main__":
    try:
        pdf_base64_simple = generate_drone_cert_simple(
            image_path="../../fpv2.jpg",
            hull_number="RU-DRN-2024-002",
            owner="Петров Алексей Сергеевич",
            drone_title="Квадрокоптер AirExplorer",
            model_title="Autel Evo Nano+"
        )

        with open("drone_certificate_simple.pdf", "wb") as f:
            f.write(base64.b64decode(pdf_base64_simple))

        print("Simple PDF saved as drone_certificate_simple.pdf")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()