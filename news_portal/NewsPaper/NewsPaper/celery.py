import os

# Из только что установленной библиотеки celery импортируем класс Celery
from celery import Celery

# Указываем где находится модуль django и файл с настройками django (имя_вашего_проекта.settings)
# в свою очередь в файле settings будут лежать все настройки celery.
# Соответственно при указании данной директивы нам не нужно будет при вызове каждого task(функции) прописывать
# эти настройки.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

# Создаем объект(экземпляр класса) celery и даем ему имя
app = Celery('NewsPaper')

# Загружаем config с настройками для объекта celery.
# т.е. импортируем настройки из django файла settings
# namespace='CELERY' - в данном случае говорит о том, что применятся будут только
# те настройки из файла settings.py которые начинаются с ключевого слова CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# В нашем приложении мы будем создавать файлы tasks.py в которых будут находится
# task-и т.е. какие-либо задания. При указании этой настройки
# celery будет автоматом искать такие файлы и подцеплять к себе.
app.autodiscover_tasks()

# для еженедельной рассылки настраиваем расписание запусков таска
app.conf.beat_schedule = {
    'send_mail_every_monday_8am': {
        'task': 'news.tasks.send_mail_for_sub_weekly',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}