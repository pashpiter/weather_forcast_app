from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils import get_city_suggestions
from core.database import get_session
from crud.query import get_latest_city_for_user

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/', response_class=HTMLResponse)
async def home(
        request: Request,
        city: str = '',
        session: AsyncSession = Depends(get_session)
):
    '''Главная страница'''
    suggestions = await get_city_suggestions(city) if city else None
    city_query = await get_latest_city_for_user(
        session, request.cookies.get('csrftoken')
    ) if request.cookies.get('csrftoken') else None
    previous_city = city_query.city if city_query else None
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'search_query': city,
            'suggestions': suggestions,
            'previous_city': previous_city
        }
    )


@router.post('/search')
async def search_city(city: str = Form(...)):
    '''Поиск города'''
    return RedirectResponse(f'/?city={city}', status_code=302)