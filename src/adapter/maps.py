import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.io as pio
import base64
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader


def create_mission_map_plotly(
        points: list[dict[str, float]],
        date: str,
        time: str,
        drone: str,
        owner: str,
        id_number: str
) -> go.Figure:
    if not points:
        raise ValueError("Список точек маршрута не может быть пустым")

    padding_ratio = 0.1

    df = pd.DataFrame(points)
    df['point_number'] = [i+1 for i in range(len(points))]
    df['sequence'] = range(len(points))

    center_lat = np.mean([point['lat'] for point in points])
    center_lng = np.mean([point['lng'] for point in points])

    lats = [point['lat'] for point in points]
    lngs = [point['lng'] for point in points]

    min_lat, max_lat = min(lats), max(lats)
    min_lng, max_lng = min(lngs), max(lngs)

    lat_padding = (max_lat - min_lat) * padding_ratio
    lng_padding = (max_lng - min_lng) * padding_ratio

    df['hover_text'] = [f'Точка {i+1}<br>Широта: {p["lat"]:.6f}<br>Долгота: {p["lng"]:.6f}'
                        for i, p in enumerate(points)]

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lng",
        hover_name="hover_text",
        zoom=12,
        height=700
    )

    fig.add_trace(go.Scattermapbox(
        lat=df['lat'],
        lon=df['lng'],
        mode='lines',
        line=dict(width=4, color='#1a73e8'),
        name='Маршрут полета',
        hoverinfo='skip'
    ))

    for i, row in df.iterrows():
        fig.add_trace(go.Scattermapbox(
            lat=[row['lat']],
            lon=[row['lng']],
            mode='markers+text',
            marker=dict(
                size=20,
                color='white',
                opacity=1,
                symbol='circle'
            ),
            text=str(row['point_number']),
            textposition="middle center",
            textfont=dict(
                size=12,
                color='#1a73e8',
                weight='bold'
            ),
            name=f'Точка {row["point_number"]}',
            hoverinfo='text',
            hovertext=row['hover_text'],
            showlegend=False
        ))

    info_text = (
        f"<b>МИССИЯ ДРОНА</b><br>"
        f"<b>Дрон:</b> {drone}<br>"
        f"<b>Дата:</b> {date}<br>"
        f"<b>Время:</b> {time}<br>"
        f"<b>Владелец:</b> {owner}<br>"
        f"<b>Документ:</b> ****{id_number}<br>"
        f"<b>Точек маршрута:</b> {len(points)}"

    )
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(lat=center_lat, lon=center_lng),
            zoom=10
        ),
        title=dict(
            text="Карта миссии дрона",
            x=0.5,
            font=dict(size=20)
        ),
        margin={"r": 0, "t": 80, "l": 0, "b": 0},
        annotations=[
            dict(
                x=0.02,
                y=0.98,
                xref='paper',
                yref='paper',
                text=info_text,
                showarrow=False,
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#1a73e8",
                borderwidth=2,
                borderpad=10,
                font=dict(size=12, color='black'),
                align='left'
            )
        ],
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    lat_range = max_lat - min_lat
    lng_range = max_lng - min_lng
    max_range = max(lat_range, lng_range)

    if max_range < 0.001:
        zoom_level = 16
    elif max_range < 0.005:
        zoom_level = 14
    elif max_range < 0.01:
        zoom_level = 13
    elif max_range < 0.02:
        zoom_level = 12
    elif max_range < 0.05:
        zoom_level = 11
    elif max_range < 0.1:
        zoom_level = 10
    elif max_range < 0.2:
        zoom_level = 9
    elif max_range < 0.5:
        zoom_level = 8
    else:
        zoom_level = 7

    fig.update_layout(
        mapbox=dict(
            center=dict(lat=center_lat, lon=center_lng),
            zoom=zoom_level
        )
    )
    return fig

def create_mission_pdf_plotly(
        points: list[dict[str, float]],
        date: str,
        time: str,
        drone: str,
        owner: str,
        id_number: str
) -> str:
    fig = create_mission_map_plotly(points, date, time, drone, owner, id_number)

    img_bytes = pio.to_image(fig, format='png', width=1200, height=800)


    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))

    img_buffer = BytesIO(img_bytes)
    img = ImageReader(img_buffer)

    pdf_width, pdf_height = landscape(A4)

    img_width = pdf_width - 80
    img_height = (img_width * 800) / 1200

    if img_height > pdf_height - 80:
        img_height = pdf_height - 80
        img_width = (img_height * 1200) / 800

    x = (pdf_width - img_width) / 2
    y = (pdf_height - img_height) / 2

    pdf.drawImage(img, x, y, width=img_width, height=img_height)
    pdf.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

    return pdf_base64