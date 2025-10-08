# import base64
# from io import BytesIO
# # from PIL import Image, ImageDraw, ImageFont
# from pathlib import Path
#
#
# def generate_drone_cert_base64(image, hull_number, owner):
#     # Validate input
#     if not image or not hull_number or not owner:
#         raise ValueError("Image, hull number, and owner are required")
#
#     # Load the image
#     drone_image = Image.open(image)
#
#     cert_width, cert_height = 800, 600
#     certificate = Image.new("RGB", (cert_width, cert_height), "white")
#     draw = ImageDraw.Draw(certificate)
#
#     font_path = Path("fonts/arial.ttf")  # Ensure the font file exists
#     font = ImageFont.truetype(str(font_path), size=24)
#     draw.text((50, 50), "Drone Certificate", font=font, fill="black")
#     draw.text((50, 100), f"Hull Number: {hull_number}", font=font,
#               fill="black")
#     draw.text((50, 150), f"Owner: {owner}", font=font, fill="black")
#
#     # Resize and paste the drone image onto the certificate
#     drone_image = drone_image.resize((300, 300))
#     certificate.paste(drone_image, (50, 200))
#
#     # Save the certificate to a BytesIO object as a PDF
#     pdf_buffer = BytesIO()
#     certificate.save(pdf_buffer, format="PDF")
#     pdf_buffer.seek(0)
#
#     # Encode the PDF as base64
#     pdf_base64 = base64.b64encode(pdf_buffer.read()).decode("utf-8")
#
#     return pdf_base64
