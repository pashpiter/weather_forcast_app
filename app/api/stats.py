from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from crud.query import count_cities_query

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/stats', response_class=HTMLResponse)
async def show_stats(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    '''Эндпоинт для статистики'''
    db_stats = await count_cities_query(session)
    stats = db_stats.model_dump()['stats']

    return templates.TemplateResponse(
        'stats.html',
        {
            'request': request,
            'stats': stats
        }
    )