# weather_forcast_app

#### Стек: Python, FastAPI, uvicorn, sqlmodel, postgresql, asyncpg, jinja2

## О проекте
Web приложение(сайт), где пользователь вводит название города, и получает прогноз погоды в этом городе на ближайшее время.

## Запуск проекта

#### Запуск через Docker

1. Установите Docker согласно инструкции с официального сайта: https://docs.docker.com/
2. Клонировать репозиторий
```
git clone https://github.com/pashpiter/weather_forcast_app.git
```
3. Перейти в папку weather_forcast_app
```
cd weather_forcast_app
```
4. В папке создайте файл `.env` с переменных окружения
```
touch .env
```
5. Заполните по примеру своими значениями как в этом [файле](example.env)
6. Для запуска проекта введите команду:
```
docker compose up -d
```

## Документация
После запуска документация доступна по адресу:
```
{FASAPI_HOST}:{FASAPI_PORT}/docs
{FASAPI_HOST}:{FASAPI_PORT}/redoc
```

## Сделано
1. Вывод данных на фронте
2. Контейнеризация
3. Подсказки при поиск города
4. Предложение города, в которой пользователь смотрел ранее (если у клиента есть csrf токен)
5. История поиска со статистикой

## Примечание
Использовано API для погоды: https://open-meteo.com/ 

#### Pavel Drovnin [@pashpiter](http://t.me/pashpiter)