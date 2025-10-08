import base64
import re
import tempfile

import folium
# from weasyprint import HTML


def create_mission_map(
        points: list[dict[str, float]],
        date: str,
        time: str,
        drone: str,
        owner: str
) -> str:
    if not points:
        raise ValueError("Список точек маршрута не может быть пустым")

    avg_lat = sum(point['lat'] for point in points) / len(points)
    avg_lng = sum(point['lng'] for point in points) / len(points)

    folium_map = folium.Map(
        location=[avg_lat, avg_lng],
        zoom_start=14
    )

    locations = []
    for i, point in enumerate(points):
        lat, lng = point['lat'], point['lng']
        locations.append([lat, lng])

        folium.Marker(
            [lat, lng],
            popup=f"Точка {i + 1}",
            icon=folium.DivIcon(
                html=f'<div style="font-size: 14pt; font-weight: bold; color: #1a73e8;">{i + 1}</div>'
            )
        ).add_to(folium_map)

    mission_info = f"""
    <div style="position: fixed; bottom: 20px; left: 50px; z-index: 1000; 
                background: white; padding: 10px; border-radius: 5px;
                box-shadow: 0 0 5px rgba(0,0,0,0.2);">
        <b>Дрон:</b> {drone}<br>
        <b>Дата:</b> {date}<br>
        <b>Время:</b> {time}<br>
        <b>Владелец:</b> {owner}<br>
    </div>
    """
    folium_map.get_root().html.add_child(folium.Element(mission_info))

    safe_date = re.sub(r'[^\w]', '_', date)
    safe_time = re.sub(r'[^\w]', '_', time)
    safe_drone = re.sub(r'[^\w]', '_', drone)
    safe_owner = re.sub(r'[^\w]', '_', owner)
    pdf_filename = f"mission_map_{safe_owner}_{safe_drone}_{safe_date}_{safe_time}.pdf"

    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmpfile:
        html_path = tmpfile.name
        folium_map.save(html_path)

    # HTML(html_path).write_pdf(pdf_filename)

    import os
    os.unlink(html_path)

    with open(pdf_filename, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    return pdf_base64