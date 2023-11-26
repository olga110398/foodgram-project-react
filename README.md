# Foodrgam

## Описание

Проект **Foodrgam** - это "продуктовый помощник". На этот сайте авторизованные пользователи могу публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Так же пользователям сайта доступен сервис "Список покупок". Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

*Полная документация к API находится по эндпоинту /redoc/*

*Проект доступен по адресу https://olgaaverkieva.ddns.net/*

**Как запустить проект на серевере:**

Установить на сервере docker и docker-compose. Скопировать на сервер файлы docker-compose.yaml и default.conf:
```
scp docker-compose.yml <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/docker-compose.yml
scp nginx.conf <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/nginx.conf
```
Добавить в Action secrets на Github следующие данные:
```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение
```
Выполнить команды:
- git add .
- git commit -m "Коммит"
- git push

После этого будут запущены процессы workflow:
- проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
- сборка и доставка докер-образа для контейнера backend на Docker Hub
- автоматический деплой проекта на сервер
- отправка уведомления в Telegram о том, что процесс деплоя успешно завершился

После успешного завершения процессов workflow необходимо будет создать суперюзера и загрузить в базу данных информацию об ингредиентах:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
```
sudo docker-compose exec backend python manage.py load_data --path <путь_к_файлу> --model_name <имя_модели> --app_name <название_приложения>
```

### В API доступны следующие эндпоинты:

- `/api/users/` Get-запрос – получение списка пользователей. POST-запрос – регистрация нового пользователя. Доступно без токена.
- `/api/users/{id}` GET-запрос – профиль пользователя с указанным id. Доступно без токена.
- `/api/users/me/` GET-запрос – профиль текущего пользователя. PATCH-запрос – редактирование собственной страницы. Доступно авторизированным пользователям.
- `/api/users/set_password` POST-запрос – изменение собственного пароля. Доступно авторизированным пользователям.
- `/api/auth/token/login/` POST-запрос – получение токена. Используется для авторизации по электронной почте и паролю, чтобы далее использовать токен при запросах.
- `/api/auth/token/logout/` POST-запрос – удаление токена.
- `/api/tags/ GET-запрос` — получение списка всех тегов. Доступно без токена.
- `/api/tags/{id}` GET-запрос — получение информации о теге по его id. Доступно без токена.
- `/api/recipes/` GET-запрос – получение списка всех рецептов. Возможен поиск рецептов по тегам и по id автора (доступно без токена). POST-запрос – добавление нового рецепта (доступно для авторизированных пользователей).
- `/api/recipes/?is_favorited=1` GET-запрос – получение списка всех рецептов, добавленных в избранное. Доступно для авторизированных пользователей.
- `/api/recipes/is_in_shopping_cart=1` GET-запрос – получение списка всех рецептов, добавленных в список покупок. Доступно для авторизированных пользователей.
- `/api/recipes/{id}/` GET-запрос – получение информации о рецепте по его id (доступно без токена). PATCH-запрос – изменение собственного рецепта (доступно для автора рецепта). DELETE-запрос – удаление собственного рецепта (доступно для автора рецепта).
- `/api/recipes/{id}/shopping_cart/` POST-запрос – добавление нового рецепта в список покупок. DELETE-запрос – удаление рецепта из списка покупок. Доступно для авторизированных пользователей.
- `/api/recipes/download_shopping_cart/` GET-запрос – получение текстового файла со списком покупок. Доступно для авторизированных пользователей.
- `/api/recipes/{id}/favorite/` POST-запрос – добавление нового рецепта в избранное. DELETE-запрос – удаление рецепта из избранного. Доступно для авторизированных пользователей.
- `/api/users/{id}/subscribe/` GET-запрос – подписка на пользователя с указанным id. POST-запрос – отписка от пользователя с указанным id. Доступно для авторизированных пользователей
- `/api/users/subscriptions/` GET-запрос – получение списка всех пользователей, на которых подписан текущий пользователь Доступно для авторизированных пользователей.
- `/api/ingredients/` GET-запрос – получение списка всех ингредиентов. Подключён поиск по частичному вхождению в начале названия ингредиента. Доступно без токена.
- `/api/ingredients/{id}/` GET-запрос — получение информации об ингредиенте по его id. Доступно без токена.


**Автор проекта:**

+ Ольга Аверкиева

*Проект разработан в рамках учебного курса Яндекс.Практикум Python Бэкенд-разработчик*