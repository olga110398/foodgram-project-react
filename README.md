# Foodrgam

## Описание

Проект **Foodrgam** - это "продуктовый помощник". На этот сайте авторизованные пользователи могу публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Так же пользователям сайта доступен сервис "Список покупок". Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

*Полная документация к API находится по эндпоинту /redoc/*


**Как запустить проект локально:**

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:olga110398/foodgram-project-react.git

```
Перейти в него:

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Наполнить БД данными из .csv файлов:

```
python manage.py load_data
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


**Авторы проекта:**

+ Ольга Аверкиева

*Проект разработан в рамках учебного курса Яндекс.Практикум Python Бэкенд-разработчик*