from datetime import datetime

import requests

from core.config import settings


async def get_city_suggestions(city: str) -> list | None:
    '''Возвращает доступные города соответсвующие вводу'''
    params = {'name': city}
    try:
        response = requests.get(settings.app.geocoding_url, params=params)
        response.raise_for_status()
        data = response.json()
        return [
            f'{res["name"]}, {res.get("country")}'
            for res in data.get('results') if res.get("country")
        ] if data.get('results') else None
    except requests.RequestException:
        return
    

async def get_city_weather(city: str) -> dict | None:
    '''Получение текущей и почасововго прогноза погоды для города'''
    params = {'name': city}
    try:
        response = requests.get(settings.app.geocoding_url, params=params)
        data = response.json()
        if not data.get('results'):
            return None
            
        data_result = data['results'][0]
        lat, lon = data_result['latitude'], data_result['longitude']
        
        weather_params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': True,
            'hourly': 'temperature_2m,weather_code',
            'timezone': 'auto'
        }
        weather_response = requests.get(settings.app.weather_url, params=weather_params)
        weather_data = weather_response.json()
        hourly_data = weather_data['hourly']
        hourly_forecast = []
        t = weather_data['current_weather']['time'][:14] + '00'
        start_index = hourly_data['time'].index(t)
        for i in range(start_index, start_index+24):
            timestamp = datetime.fromisoformat(hourly_data['time'][i])
            hourly_forecast.append({
                'time': timestamp.strftime('%H:%M'),
                'temp': hourly_data['temperature_2m'][i],
                'code': hourly_data['weather_code'][i]
            })

        return {
            'city': f'{data_result["name"]}, {data_result.get("country")}',
            'current': weather_data.get('current_weather'),
            'hourly': hourly_forecast
        }
    except requests.RequestException:
        return None
