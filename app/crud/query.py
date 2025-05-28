from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, func, select

from schemas.query import CityQuery, CityQueryCreate, CityStats, CityStatsRead


async def get_latest_city_for_user(
        session: AsyncSession,
        csrftoken: str
) -> CityQuery | None:
    stmt = (
        select(CityQuery)
        .where(CityQuery.csrftoken == csrftoken)
        .order_by(desc(CityQuery.id))
        .limit(1)
    )
    results: Result = await session.execute(stmt)
    return results.scalars().one_or_none()


async def create_query(
        session: AsyncSession,
        city: str,
        csrftken: str
) -> CityQuery:
    query_db = CityQuery(city=city, csrftoken=csrftken)
    session.add(query_db)
    await session.commit()
    await session.refresh(query_db)
    return query_db


async def count_cities_query(
        session: AsyncSession
) -> CityStatsRead:
    stmt = (
        select(CityQuery.city, func.count(CityQuery.city).label("count"))
        .group_by(CityQuery.city)
        .order_by(func.count(CityQuery.city).desc())
        .limit(100)
    )
    results: Result = await session.execute(stmt)
    city_stats = results.all()
    
    stats = [CityStats(city=city, count=count) for city, count in city_stats]
    return CityStatsRead(stats=stats)
