# Yatube API

REST API социальной сети: публикации, тематические группы и комментарии.
Вся логика API находится в отдельном приложении `api`.

API использует TokenAuthentication. Все ресурсы доступны только после
аутентификации. Пользователь может читать чужие публикации и комментарии,
но изменять и удалять — только собственные. Группы доступны только для чтения;
создание групп выполняется через админку. Авторы назначаются по токену.

## Технологии

Python 3.10, Django 3.2, Django REST Framework 3.12.4, SQLite.
Зависимости закреплены в исходном `requirements.txt` Практикума.
Для их установки используйте Python 3.10.

## Запуск в Windows

```powershell
git clone https://github.com/welcometoforeverr/api_yatube.git
cd api_yatube
py -3.10 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe yatube_api\manage.py migrate
.\venv\Scripts\python.exe yatube_api\manage.py createsuperuser
.\venv\Scripts\python.exe yatube_api\manage.py runserver
```

Админка: http://127.0.0.1:8000/admin/ . Зарегистрированы Post, Group и Comment.
Создавайте обычных пользователей в админке; суперпользователь создаётся командой
выше. Пароли и локальная база данных в репозиторий не включены.
Настройки предназначены для локального учебного запуска.

## Получение токена и запросы

POST `/api/v1/api-token-auth/` с JSON:

```json
{"username": "your_username", "password": "your_password"}
```

Ответ: `{"token": "..."}`. В остальных запросах передавайте заголовок
`Authorization: Token <полученный_токен>`.

| Адрес | Методы | Назначение |
| --- | --- | --- |
| `/api/v1/posts/` | GET, POST | Список постов и создание |
| `/api/v1/posts/{id}/` | GET, PUT, PATCH, DELETE | Отдельный пост |
| `/api/v1/groups/` | GET | Список групп |
| `/api/v1/groups/{id}/` | GET | Отдельная группа |
| `/api/v1/posts/{post_id}/comments/` | GET, POST | Комментарии поста |
| `/api/v1/posts/{post_id}/comments/{id}/` | GET, PUT, PATCH, DELETE | Комментарий |

Создание поста: POST `/api/v1/posts/`:

```json
{"text": "Моя первая публикация", "group": 1}
```

`group` необязателен. Поле `author` возвращает username и доступно только
для чтения. `image` можно передать как файл с multipart/form-data.

Создание комментария: POST `/api/v1/posts/1/comments/`:

```json
{"text": "Мой комментарий"}
```

Поле `post` доступно только для чтения: родительский пост определяется URL.
Несуществующий пост или комментарий из другого поста дают 404.
Изменение чужого контента даёт 403; запрос без токена — 401.
Данные не прошедшей валидацию заявки дают 400; запрещённый метод — 405.
POST возвращает созданный объект и 201, PUT/PATCH — изменённый объект и 200,
DELETE — пустой ответ 204.

## Проверки

Из корня репозитория:

```powershell
.\venv\Scripts\python.exe -m pytest
.\venv\Scripts\python.exe yatube_api\manage.py check
.\venv\Scripts\python.exe yatube_api\manage.py makemigrations --check --dry-run
```

Пройдены 49 исходных и 11 дополнительных pytest-тестов. Дополнительные тесты
проверяют вложенные адреса комментариев, защиту от подмены автора/поста
и удаление своего комментария. Исходные тесты сохранены без изменений.

Коллекция `postman_collection/CRUD_for_yatube.postman_collection.json`
также проверена через Newman: 60 запросов, 88 успешных проверок, ошибок нет.
Инструкция ручного запуска коллекции — в `postman_collection/README.md`.
