У вас уже должен быть включен сервер MySQL, с готовой базой, пользователем и паролём.
Для подключения к базе:
    1. Введите следующие комманды в терминал чтобы установить нужные пакеты:
        ```
            sudo apt-get install python3 python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip
        ```
    2. Установите пакеты из requirements.txt
    3. 
        В папке source/main/ добавьте файл settings_local.py. Напишите в нём следующие данные:
        ```
            DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'movie_db',
                'USER': 'movie_user',
                'PASSWORD': 'movie_pass',
                'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
                'PORT': '3306',
                'OPTIONS': {
                    'charset': 'utf8mb4'  # This is the important line
                }
            }
        }
    ```
    Вместо Name - название базы данных, User - пользователь в на сервере MySQL, Password - пароль к пользователю.
    
    4. Совершите миграцию:
        python manage.py migrate
    5. Загрузите данные из фикстуры:
        python manage.py loaddata fixtures/auth.json
        python manage.py loaddata fixtures/dump.json
