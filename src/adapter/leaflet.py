import folium


def create_mission_map(
        points: list[dict[str, float]],
        date: str,
        time: str,
        drone: str,
) -> folium.Map:
    """
    Создает карту маршрута БПЛА с помощью Folium

    :param points: Список точек маршрута [{"lat": 55.75, "lng": 37.61}, ...]
    :param date: Дата полета в формате "YYYY-MM-DD"
    :param time: Время полета в формате "HH:MM:SS"
    :param drone: Модель дрона
    :param save_path: Путь для сохранения HTML файла (если не указан - файл не сохраняется)
    :return: Объект карты Folium
    """
    if not points:
        raise ValueError("Список точек маршрута не может быть пустым")

    # Рассчет среднего центра для карты
    avg_lat = sum(point['lat'] for point in points) / len(points)
    avg_lng = sum(point['lng'] for point in points) / len(points)

    # Создание карты с центром в средних координатах
    folium_map = folium.Map(
        location=[avg_lat, avg_lng],
        zoom_start=14,
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='OpenStreetMap'
    )

    # Добавление маркеров с номерами точек
    locations = []
    for i, point in enumerate(points):
        lat, lng = point['lat'], point['lng']
        locations.append([lat, lng])

        # Создание маркера с номером точки
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
    </div>
    """
    folium_map.get_root().html.add_child(folium.Element(mission_info))

    folium_map.save("maps.html")
    return folium_map.get_root().render()