# yamdb_final
yamdb_final
![workflow](https://github.com/NikolayRudakkov/yambd_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## **Об авторе:**


* Имя: Николай Рудаков	
* Род деятельности: Студент курса Яндекс.Практикум Python-разработчик
* Контакты: https://github.com/NikolayRudakov/


## **Описание:**

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

---
# Описание Workflow
##### Workflow состоит из четырёх шагов:
###### tests
- Проверка кода на соответствие PEP8, автоматический запуск тестов.
###### Push Docker image to Docker Hub
- Сборка и публикация образа на DockerHub.
###### deploy 
- Автоматический деплой на боевой сервер при пуше в главную ветку main.
###### send_massage
- Отправка уведомления в телеграм-чат.

## Подготовка и запуск проекта
##### Клонирование репозитория
Склонируйте репозиторий на локальную машину:
```bash
git clone https://github.com/NikolayRudaov/yamdb_final.git
```

## Установка на удаленном сервере (Ubuntu):
##### Шаг 1. Выполните вход на свой удаленный сервер
Прежде, чем приступать к работе, необходимо выполнить вход на свой удаленный сервер:
```bash
ssh <USERNAME>@<IP_ADDRESS>
```

##### Шаг 2. Установите docker на сервер:
Введите команду:
```bash
sudo apt install docker.io 
```

##### Шаг 3. Установите docker-compose на сервер:
Введите команды:
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

##### Шаг 4. Скопируйте подготовленные файлы:
Скопируйте подготовленные файлы `docker-compose.yaml` и `nginx/default.conf` из вашего проекта на сервер в `home/<ваш_username>/docker-compose.yaml` и `home/<ваш_username>/nginx/default.conf` соответственно.
Введите команду из корневой папки проекта:
```bash
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp -r nginx/ <username>@<host>:/home/<username>/
```

##### Шаг 5. Добавьте Secrets:
Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
```bash
SECRET_KEY=<SECRET_KEY>
DEBUG=<True/False>
ALLOWED_HOSTS=<hosts>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID своего телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```

##### Шаг 6. После успешного деплоя:
Зайдите на боевой сервер и выполните команды (только после первого деплоя):
###### Создаем и применяем миграции:
```bash
sudo docker-compose exec web python manage.py makemigrations --noinput
sudo docker-compose exec web python manage.py migrate --noinput
```
###### Подгружаем статику
```bash
sudo docker-compose exec web python manage.py collectstatic --no-input 
```
###### Заполнить базу данных:
```bash
sudo docker-compose exec web python3 manage.py loaddata fixtures.json
```
###### Создать суперпользователя Django:
```bash
sudo docker-compose exec web python manage.py createsuperuser
```

##### Шаг 7. Проект запущен
Проект будет доступен по вашему IP-адресу.

Проект доступен по адресу: http://51.250.106.201/api/v1/

Образ на DockerHub: https://hub.docker.com/repository/docker/nrudaov/yamdb_final


## **Документация API YaMDb**

Документация доступна по эндпойнту: http://localhost/redoc/
