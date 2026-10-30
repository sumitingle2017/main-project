# Mala Shree Om Bhel & Namkeen - Django
1. MySQL madhe DB: `CREATE DATABASE shreeom CHARACTER SET utf8mb4;`
2. `pip install -r requirements.txt`
3. Env: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST (ki settings.py madhe bhara)
4. `python manage.py makemigrations shop && python manage.py migrate`
5. `python manage.py createsuperuser`  (hach staff/counter/kitchen login)
6. `python manage.py runserver 0.0.0.0:8000`
Pages: / (customer menu), /counter/, /kitchen/, /manage/, /login/
