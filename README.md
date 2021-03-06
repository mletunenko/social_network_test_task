# Social network test task

Настоящий репозиторий содержит проект, выполненный в рамках тестового задания для вакансии django-разработчик. Код проекта
написан на языке Python 3.8, с использованием библиотек Django и Django REST framework, зависимости описаны в requirements.txt.

Проект работает с базой данных sqlite3.

Проект представляет REST API социальной сети. Описаны модели User и Post. Реализована регистрация новых пользователей социальной
сети, создание и редактирование постов пользователями, возможность поставить и убрать лайк поста.

Для использования проекта необходимо:

- Создать локально директорию для нового проекта python с виртуальным окружением
- Скопировать файлы данного репозитория в директорию с проектом
- Перейти в директорию проекта _test_task_ и выполнить команду _pip install -r requirements.txt_ для установки необходимых
  зависимостей
- Запустить сервер командой _python manage.py runserver_

Репозиторий содержит файл с базой данных, которая готова к использованию.

Авторизация реализована с помощью JWT, использование и тестирование рекомендуется осуществлять с применением Postman.

## Регистрация нового пользователя

Для регистрации нового пользователя необходимо отправить POST запрос на url _http://127.0.0.1:8000/registration/_. В теле запроса
передать данные необходимые для регистрации:

    {
        "username": "test_user",
        "first_name": "test",
        "last_name": "test",
        "email": "test@mail.com",
        "password": "12345"
    }

## Авторизация пользователя

Для авторизации пользователя необходимо запросить токен, оправив POST запрос на url _http://127.0.0.1:8000/token/_. В теле
запроса передать данные для авторизации:

    {
        "username": "test_user",
        "password": "12345"
    }

Ответом на запрос будут access и refresh токены, они необоходимы для будущих запросов.

## Создание нового поста

Авторизованный пользователь может создать пост с помощью POST запроса на url _http://127.0.0.1:8000/post/_. В теле запроса
передать данные для создания поста:

    {
        "title": "Post's Title",
        "content": "Post's content"
    }

В header запроса необходимо добавить ключ авторизации Authorization, а в значении указать "Bearer {access_token}", где
access_token это токен, который был получен при авторизации.

## Редактирование поста

Автор поста может изменить пост. Для полного изменения необходимо отправить PUT запрос на
url _http://127.0.0.1:8000/post/{post_id}/_. В теле запроса передать новые данные:

    {
        "title": " New Post's Title",
        "content": "New Post's content"
    }

Для частичного изменения необходимо отправить PATCH запрос на url _http://127.0.0.1:8000/post/{post_id}/_. В теле запроса
передать новые данные:

    {
        "title": " New Post's Title"
    }

## Лайк поста

Авторизованный пользователь может поставить лайк на любой пост, для этого необходимо отправить POST запрос на url _http://127.0.0.1:8000/post/{post_id}/like/_. Тело запроса пустое.

## Отмена лайка поста

Авторизованный пользователь может убрать свой лайк с поста, для этого необходимо отправить POST запрос на url _http://127.0.0.1:8000/post/{post_id}/unlike/_. Тело запроса пустое.

