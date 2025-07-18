### Опис проєкту CAR-SALE-PLATFORM

Цей проєкт є бекенд-частиною платформи для продажу автомобілів, що розробляється як сучасна альтернатива застарілому сайту клієнта з 2010 року. Нова платформа розрахована на значне зростання клієнтської бази та високе навантаження, тому використовує масштабовану архітектуру із контейнеризацією. Система розроблена з урахуванням гнучкості для легкого додавання, редагування чи відключення функціоналу.

#### Основні задачі:
1. **Ролі користувачів**:
   - **Покупець**: переглядає оголошення, зв’язується з продавцями чи автосалонами.
   - **Продавець**: створює оголошення про продаж авто.
   - **Менеджер**: модерує контент, перевіряє та видаляє невалідні оголошення.
   - **Адміністратор**: має повний контроль над платформою.
   - Планується підтримка автосалонів із додатковими ролями (менеджери, адміністратори, механіки), реалізована через систему прав доступу.

2. **Типи акаунтів**:
   - **Базовий**: безкоштовний, дозволяє продавцям розміщувати лише одне оголошення.
   - **Преміум**: платний, надає статистику (перегляди, середня ціна авто), необмежену кількість оголошень.

3. **Основний функціонал**:
   - **Створення оголошень**: продавці додають авто, обираючи марку та модель із випадаючого списку. Є можливість повідомити адміністрацію про відсутність марки/моделі.
   - **Валюти**: ціна вказується в USD, EUR або UAH, автоматично конвертується за курсом ПриватБанку (оновлення раз на день).
   - **Модерація**: автоматична перевірка на нецензурну лексику. Оголошення активується, якщо проходить перевірку, або пропонується редагування (до 3 спроб). У разі невдачі — відправка менеджеру на перевірку.

4. **Інформація для преміум-користувачів**:
   - Кількість переглядів оголошення (загалом, за день/тиждень/місяць).
   - Середня ціна авто в регіоні продажу та по Україні.

#### Технічні особливості:
- **Масштабованість**: архітектура розрахована на десятки разів більше навантаження.
- **Гнучкість**: модульна структура для легкої модифікації.
- **AWS**: платформа може бути контейнеризована для розгортання на AWS.
- **Система пермішинів**: для майбутньої підтримки автосалонів та їхніх ролей.
- **Хмарна база даних**: платформа підтримує та зберігає інформацію в хмарній базі даних PostgreSQL на сервісі Neon.

Цей бекенд реалізовано на Python, із фокусом на надійність, масштабованість та зручність розширення функціоналу.

#### API Документація:

Swagger: http://localhost/api/doc
Postman колекція: car-sale-platform.postman_collection.json

#### Рекомендації щодо запуску, тестування та використання проекту:

1. Клонуйте репозиторій та налаштуйте .env як у .env.example CLOUD_SETUP(.env ЗАЛИШИВ ДЛЯ ПРОСТІШОЇ ПЕРЕВІРКИ, ще одна копія env в кінці README)
2. Збудуйте докер контейнери: docker compose up --build
3. Якщо все піднялось коректно можна тестувати в Postman(приклад алгоритму нижче) або запустити тести в новому терміналі:
    
    docker compose exec app python manage.py test (тести виконуються приблизно 500 секунд, після тестів можлива помилка
    при спробі видалення тестової БД з хмариного кластеру через з'єднання сервісу Celery, але тести відпрацьовують корректно)

    Якщо не обнуляти основну БД там буде в наявності 1 суперюзер та 1 активований користувач у ролі продавця(для простішого тестування)
    А також 1 бренд авто та 1 модель авто, 1 оголошення про продаж
    
    У фронтенді можно потестувати чат якщо додати ще одного активованого користувача(у Postman, алгоритм активації нижче) та увійти в одну кімнату(фронтенд)
    Суперюзер доданий через команду createsuperuser в IDE не буде мати профілю та не зможе користуватись чатом.

   3.5 Якщо проблеми з міграціями(або запуск після обнулення хмарної БД) виконайте наступні дії в іншому вікні терміналу: 
   docker compose run --rm app sh
       python manage.py makemigrations
       python manage.py migrate
        Створіть superuser:
    docker compose run --rm app sh
    python manage.py createsuperuser
    email: admin@gmail.com(зручніше саме ці дані, так як вони додані у Postman колекцію)
    password: admin
   
4. Приклад алгоритму тестування API якщо обнулити хмарну БД:
   1. Після створення суперюзера у IDE додати бренд авто через Postman(CarModels->CarBrand->createCarBrand)
   2. Додати модель авто через Postman(CarModels->CarModel->createCarModel)
   3. Зареєструвати нового користувача з реальним email через Postman(AuthRegistration->UserRegister->userRegister)
   4. Зайти на пошту, натиснути на посилання, у відкритій вкладинці скопіювати токен активації з URL
   5. Активувати користувача через Postman(AuthRegistration->auth->authLoginRecoveryActivate->activateUserToken)
   вставивши скопійований токен в змінну {{ }} в URL Postman
   6. Зайти під активованим аккаунтом через Postman або localhost адресу у браузері(мінімальний функціонал фронтенду)
      (AuthRegistration->auth->authLoginRecoveryActivate->login)
   7. Зробити користувача продавцем через Postman(SellersListings->SellersList->createSeller)
   8. Перевірити доступні бренди авто для перевірки car_brand_id та car_model_id(для створення оголошення)
   Postman(CarModels->CarBrand->allCarBrandList) та використати у наступному кроці
   9. Додати нове оголошення на продаж авто через Postman(SellersListings->ListingsList->createListing)
   10. Додати фото для оголошення (SellersListings->ListingsList->addPhotoToListing)
   11. І так далі...(для ознайомлення з усім функціоналом перейдіть у документацію http://localhost/api/doc або Postman колекцію)

#### П.С. : Було обрано PostgreSQL хмарну БД через те що не вдалось мігрувати моделі з OneToOne відношеннями
#### у декілька безкоштовних MySQL БД (PlanetScale - стала платною, TiDBcloud - не вдалось мігрувати(витратив багато часу на спроби) )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Project Description : CAR-SALE-PLATFORM

This project is the backend component of a car sales platform developed as a modern alternative to the client's outdated website from 2010. The new platform is designed to handle significant client base growth and high load, utilizing a scalable architecture with containerization. The system is built with flexibility in mind to allow easy addition, modification, or disabling of functionality.

#### Main Tasks:
1. **User Roles**:
   - **Buyer**: Browses listings, contacts sellers or dealerships.
   - **Seller**: Creates listings for car sales.
   - **Manager**: Moderates content, reviews, and removes invalid listings.
   - **Administrator**: Has full control over the platform.
   - Future support for dealerships with additional roles (managers, administrators, mechanics) is planned, implemented through a permissions system.

2. **Account Types**:
   - **Basic**: Free, allows sellers to post only one listing.
   - **Premium**: Paid, provides statistics (views, average car price) and unlimited listings.

3. **Core Functionality**:
   - **Listing Creation**: Sellers add cars, selecting make and model from a dropdown list. They can notify the administration if a make/model is missing.
   - **Currencies**: Prices are set in USD, EUR, or UAH, automatically converted based on PrivatBank's exchange rate (updated daily).
   - **Moderation**: Automatic profanity checks. Listings are activated if they pass, or sellers are prompted to edit (up to 3 attempts). If unsuccessful, the listing is sent to a manager for review.

4. **Premium User Information**:
   - Number of listing views (total, daily/weekly/monthly).
   - Average car price in the region of sale and across Ukraine.

#### Technical Features:
- **Scalability**: Architecture designed to handle significantly higher loads.
- **Flexibility**: Modular structure for easy modifications.
- **AWS**: Platform can be containerized for deployment on AWS.
- **Permissions System**: For future support of dealerships and their roles.
- **Cloud Database**: The platform supports and stores data in a PostgreSQL cloud database on the Neon service.

This backend is implemented in Python, focusing on reliability, scalability, and ease of functionality expansion.

API Documentation:

Swagger: http://localhost/api/doc
Postman Collection: car-sale-platform.postman_collection.json

#### Recommendations for Running, Testing and Using the Project:

1. Clone the repository.
2. Build Docker containers: `docker compose up --build`.
3. If everything starts correctly, you can test using Postman (example algorithm below) or run tests in a new terminal:

    ```bash
    docker compose exec app python manage.py test
    ```
    (Tests take approximately 500 seconds. After tests, an error may occur when attempting to delete the test database from the cloud cluster due to a Celery service connection, but the tests execute correctly.)

    If the main database is not reset, it will contain 1 superuser and 1 activated user with the seller role (for easier testing), along with 1 car brand, 1 car model, and 1 sale listing.

    In the frontend, you can test the chat functionality by adding another activated user (via Postman, activation algorithm below) and entering the same chat room (frontend). A superuser created via the `createsuperuser` command in the IDE will not have a profile and cannot use the chat.

4. If there are issues with migrations (or after resetting the cloud database), perform the following steps in another terminal window:
    ```bash
    docker compose run --rm app sh
    python manage.py makemigrations
    python manage.py migrate
    ```
    Create a superuser:
    ```bash
    docker compose run --rm app sh
    python manage.py createsuperuser
    ```
    Email: `admin@gmail.com` (recommended for convenience, as it’s included in the Postman collection)  
    Password: `admin`

5. Example API testing algorithm if the cloud database is reset:
    1. After creating a superuser in the IDE, add a car brand via Postman (`CarModels->CarBrand->createCarBrand`).
    2. Add a car model via Postman (`CarModels->CarModel->createCarModel`).
    3. Register a new user with a real email via Postman (`AuthRegistration->UserRegister->userRegister`).
    4. Check the email, click the activation link, and copy the activation token from the URL in the opened tab.
    5. Activate the user via Postman (`AuthRegistration->auth->authLoginRecoveryActivate->activateUserToken`), inserting the copied token into the `{{ }}` variable in the Postman URL.
    6. Log in with the activated account via Postman or the localhost address in a browser (minimal frontend functionality) (`AuthRegistration->auth->authLoginRecoveryActivate->login`).
    7. Make the user a seller via Postman (`SellersListings->SellersList->createSeller`).
    8. Check available car brands to verify `car_brand_id` and `car_model_id` (for creating a listing) via Postman (`CarModels->CarBrand->allCarBrandList`) and use them in the next step.
    9. Add a new car sale listing via Postman (`SellersListings->ListingsList->createListing`).
    10. Add a photo to the listing (`SellersListings->ListingsList->addPhotoToListing`).
    11. And so on... (to explore all functionality, refer to the documentation at `http://localhost/api/doc` or the Postman collection).

#### CONFIGS

#### docker-compose.yml

services:
  app:
    build:
      context: .
    volumes:
      - ./backend:/app
    env_file:
      - .env
    ports:
      - "8888:8000"
    restart: on-failure
    command: >
      sh -c "python manage.py wait_db && python manage.py runserver 0.0.0.0:8000"
    depends_on:
      - redis
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./client:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./backend/static:/usr/share/nginx/doc
    depends_on:
      - app

  redis:
    image: redis:alpine

  celery:
    build:
      context: .
    volumes:
      - ./backend:/app
    env_file:
      - .env
    restart: on-failure
    command: >
      sh -c "celery -A configs worker -l info -B"
    depends_on:
      - web
      - redis
      - app
  
####  Dockerfile

FROM python:3.13-alpine

MAINTAINER Python Backend Car Sale Platform

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80 \
    POETRY_HOME=/usr/local/poetry

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apk update && apk add --no-cache --virtual .build-deps gcc musl-dev mariadb-dev curl \
    && apk add --no-cache postgresql-client \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apk del curl

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

#### TO MAKE MySQL LOCAL_DB setup 1. change .env like in .env.example LOCAL_SETUP and change configs/settings file in
#### DATABASES section :
        
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('MYSQL_HOST'),
        'PORT': os.environ.get('PORT'),
    }
}
1. REMOVE COMMENTED LINES IN docker-compose.yml
2. THEN delete all migrations in backend/apps/<every app migrations files in folder>
3. stop docker with: docker compose down
4. rebuild docker : docker compose up --build
5. in new terminal window run: 
       docker compose run --rm app sh
       python manage.py makemigrations
       python manage.py migrate
6. python manage.py createsuperuser
7. watch above about documentation and postman collection to work with project

#### ENV_BACKUP

SECRET_KEY='django-insecure-16u0ls%*958v#znux0z9w_1bj58-pk!+zfrtgd5t&vb+rs4h0#'
DEBUG=True

DB_HOST=ep-noisy-shape-a2laozjp-pooler.eu-central-1.aws.neon.tech
DB_PORT=5432
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=npg_no3GTxPlw1Jy
DB_SSL_MODE=require

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=bodk335@gmail.com
EMAIL_HOST_PASSWORD=qvqduxsqlviqhfyp
EMAIL_PORT=587