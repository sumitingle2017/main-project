import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = ["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","shop"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware"]
ROOT_URLCONF = "shreeom.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,
    "OPTIONS":{"context_processors":["django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "shreeom.wsgi.application"
DATABASES = {"default": {"ENGINE":"django.db.backends.mysql","NAME":os.environ.get("DB_NAME","shreeom"),
    "USER":os.environ.get("DB_USER","root"),"PASSWORD":os.environ.get("DB_PASSWORD","Sumit@123"),
    "HOST":os.environ.get("DB_HOST","127.0.0.1"),"PORT":os.environ.get("DB_PORT","3306"),
    "OPTIONS":{"charset":"utf8mb4"}}}
LANGUAGE_CODE = "en"
TIME_ZONE = "Asia/Kolkata"
USE_TZ = True
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/counter/"
LOGOUT_REDIRECT_URL = "/"

