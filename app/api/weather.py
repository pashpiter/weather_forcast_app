from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils import get_city_weather
from core.database import get_session
from crud.query import create_query

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/weather')
async def show_weather(
        request: Request,
        city: str,
        session: AsyncSession = Depends(get_session)
):
    '''Эндпоинт для показа погогды конкретного города'''
    weather_data = await get_city_weather(city)
    if not weather_data:
        return RedirectResponse('/?error=City+not+found', status_code=302)
    await create_query(session, city, request.cookies['csrftoken'])

    return templates.TemplateResponse(
        'weather.html',
        {
            'request': request,
            'city': weather_data['city'],
            'current': weather_data['current'],
            'hourly_forecast': weather_data['hourly'],
            'history': []
        }
    )