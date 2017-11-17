"""
Django settings for dingo project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from .local_settings import SECRETKEY, botToken

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETKEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dingo',
    'polls',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates/")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]

BOTCONFIG={
    'bot':{
        'prefixes': ["."], #command prefixes
        'token': botToken, #this is the Discord Token to connect
        'botmodule': "utils.botcom", #this is the module that the bot will search commands for in each app
        'extraCommands': "bin.extcoms" #this is the module that the bot will
    },
    'strings':{
        'info': {
            'description': "Tomu - The bot with its own webpage", #bots description
            'reconnection': "{botname} is back", #bot reconnection message. This will be passed to the log format
        },
        'errors': { #variables:
                        #user = metions the user that called the command
                        #command = the command name
                        #format = the help format for the command
            'missing-permissions': "{user} you don't have permission to use the `{command}` command",
            'missing_argument': "{user} you are missing required arguments.\n{format}",
            'bad_argument': "{user} you miss entered an argument in the `{command}` command.\n{format}",
            'regular_error': "An error occured while processing the `{command}` command.",
        },
        
        'utils':{
            'antispam':{
                '2manycalls': "Too many simultaneous calls.",
            },
            'require_login':{
                'registration': "You have to register to use some commands. Use the `{prefix}register` command",
            },
            'log':{
                'format': "[{day}/{month}/{year} {hour}:{minute}:{second}] \"{message}\"",
            },
        },
        'commands':{
            'hi': "hi {name}, how are you?",
            'register':{
                'username_linked':"This discord account has already a username linked to it",
                'username_petition':"Please send a message with your username in the website",
                'acc_linked_discord':"This account has already been linked to another discord account",
                'passwd':"Please send the password.",
                'user_already_registered':"You are already registered. you don't have to use this command again",
                'succ_registered': "Success now you can use the commands in the server. Also you can delete the message with your password. It will not be saved",
                'error': "That wasn't quite right. Try again",
            },
        },
    },
    'server': {
        'announces': "announcements", #the name of the anouncements channel
        'output': "logs", #the name of the channel where the bot will send its logs
        'bot-role': "Tomu", #the name of the role that the bot will use
        'admin-role': "admin", #the name for the admin role
        'bot-color': 0x11806A, #the color for the bot role
        'admin-color': 0xE74C3C #the color for the admin role
    },
}