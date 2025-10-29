import base64
from io import BytesIO
from datetime import datetime
from weasyprint import HTML
import os


def generate_drone_cert_base64(image_path, hull_number, owner, drone_title, model_title=None):
    """Generate a drone certificate in PDF format and return as base64 string."""
    
    # Validate input
    if not image_path or not hull_number or not owner:
        raise ValueError("Image path, hull number, and owner are required")
    
    # Read and encode the image to base64 for embedding in HTML
    with open(image_path, 'rb') as img_file:
        img_data = base64.b64encode(img_file.read()).decode('utf-8')
    
    # Determine MIME type
    ext = os.path.splitext(image_path)[1].lower()
    mime_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    mime_type = mime_type_map.get(ext, 'image/jpeg')
    
    # Current date
    issue_date = datetime.now().strftime("%d.%m.%Y")
    
    # Create HTML template for the certificate
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4 landscape;
                margin: 0;
            }}
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
            }}
            .certificate {{
                background: white;
                padding: 60px;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                text-align: center;
                position: relative;
                min-height: 500px;
            }}
            .header {{
                border-bottom: 4px solid #667eea;
                padding-bottom: 20px;
                margin-bottom: 40px;
            }}
            h1 {{
                color: #667eea;
                font-size: 48px;
                margin: 0;
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            .subtitle {{
                color: #666;
                font-size: 18px;
                margin-top: 10px;
            }}
            .content {{
                margin: 40px 0;
            }}
            .drone-image {{
                max-width: 300px;
                max-height: 300px;
                margin: 20px auto;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            .info-section {{
                background: #f8f9fa;
                padding: 30px;
                border-radius: 10px;
                margin: 30px 0;
                text-align: left;
            }}
            .info-row {{
                margin: 15px 0;
                font-size: 18px;
            }}
            .info-label {{
                font-weight: bold;
                color: #667eea;
                display: inline-block;
                width: 200px;
            }}
            .info-value {{
                color: #333;
            }}
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #e0e0e0;
                color: #666;
                font-size: 14px;
            }}
            .seal {{
                position: absolute;
                bottom: 60px;
                right: 60px;
                width: 120px;
                height: 120px;
                border: 3px solid #667eea;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                background: white;
                font-weight: bold;
                color: #667eea;
                font-size: 12px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="certificate">
            <div class="header">
                <h1>Сертификат регистрации БПЛА</h1>
                <div class="subtitle">Удостоверение регистрации беспилотного летательного аппарата</div>
            </div>
            
            <div class="content">
                <img src="data:{mime_type};base64,{img_data}" class="drone-image" alt="Drone Image">
                
                <div class="info-section">
                    <div class="info-row">
                        <span class="info-label">Бортовой номер:</span>
                        <span class="info-value">{hull_number}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Название:</span>
                        <span class="info-value">{drone_title}</span>
                    </div>
                    {f'<div class="info-row"><span class="info-label">Модель:</span><span class="info-value">{model_title}</span></div>' if model_title else ''}
                    <div class="info-row">
                        <span class="info-label">Владелец:</span>
                        <span class="info-value">{owner}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Дата выдачи:</span>
                        <span class="info-value">{issue_date}</span>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                Данный сертификат подтверждает регистрацию беспилотного летательного аппарата<br>
                в системе учета и управления дронами
            </div>
            
            <div class="seal">
                ОФИЦИАЛЬНАЯ<br>ПЕЧАТЬ
            </div>
        </div>
    </body>
    </html>
    """
    
    # Generate PDF from HTML
    pdf_buffer = BytesIO()
    HTML(string=html_content).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    
    # Encode PDF to base64
    pdf_base64 = base64.b64encode(pdf_buffer.read()).decode('utf-8')
    
    return pdf_base64
