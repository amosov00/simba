# Elastoo boilerplate

## Запуск для локальной разработки

### Frontend

#### Вариант 1. Запуск без докера

- Установить зависимости через yarn install
- Скопировать `.env.example` как `.env.local` и поместить в папку frontend/
- Изменить baseURL и browserBaseURL
- Запустить через yarn dev

#### Вариант 2. С докером

- Установить зависимости через yarn install
- Скопировать `./deployment/enviroment/.frontend.example` как `.env.frontend` и поместить в корневую папку
- Запустить через `docker-compose run --rm --service-ports frontend`

### Backend && Fullstack

- Скопировать из `./deployment/enviroment/` файлы конфигурации в корневую папку, назвать их как `.env.{name}`,
  где {name} = frontend || backend || db
- `docker-compose build` для первоначальной сборки контейнеров (если нужен только backend, то `docker-compose build backend`)
- `docker-compose up` для запуска полного проекта, `docker-compose run --rm --service-ports backend` только для backend
