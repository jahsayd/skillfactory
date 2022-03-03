import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import datetime

from news.models import Category, Post


logger = logging.getLogger(__name__)


# рассылка подписчикам новых новостей за прошлую неделю по определенным категориям новостей
def news_sender():
    print()
    print('===================================ПРОВЕРКА ОТПРАВКИ===================================')
    print()

    # Первый цикл - получение из модели категории всех объектов

    for category in Category.objects.all():

        # пустой список для будущего формирования списка статей, разбитых по категориям + ссылка перехода на каждую
        # статью, своя уникальная рядом с названием статьи

        news_from_each_category = []

        # определение номера недели
        week_number_last = datetime.now().isocalendar()[1] - 1

        # Второй цикл - из первого цикла получаем рк категории, и подставляем его в запрос, в первый фильтр, во второй
        # фильтр подставляем значение предыдущей недели, то есть показать статьи с датой создания предыдущей недели

        for news in Post.objects.filter(post_category=category.id,
                                        post_date__week=week_number_last).values('pk',
                                                                                    'heading',
                                                                                    'post_date',
                                                                                    'post_category__category_name'):

            # преобразование даты в нужный формат
            date_format = news.get("post_date").strftime("%m/%d/%Y")

            # формирование строки с данными о публикации

            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("heading")}, '
                   f'Категория: {news.get("post_category__category_name")}, Дата создания: {date_format}')

            # формирование списка строк
            news_from_each_category.append(new)

        # для удобства в консоль добавляем разграничители и пометки
        print()
        print('+++++++++++++++++++++++++++++', category.category_name, '++++++++++++++++++++++++++++++++++++++++++++')
        print()
        print("Письма будут отправлены подписчикам категории:", category.category_name, '( id:', category.id, ')')

        # получаем объект подписчиков категории
        subscribers = category.subscribers.all()


        # Третий цикл - до формирование письма (имя кому отправляем получаем тут) и рассылка готового
        # письма подписчикам, которые подписаны под данной категорией
        # создаем приветственное письмо с нашим списком новых за неделю статей конкретной категории,
        # помещаем в письмо шаблон (html страничку), а также передаем в шаблон нужные нам переменные
        for subscriber in subscribers:
            # для удобства в консоль добавляем разграничители и пометки
            print('____________________________', subscriber.email, '___________________________________')
            print()
            print('Письмо, отправленное по адресу: ', subscriber.email)
            html_content = render_to_string(
                'mail_weekly.html', {'user': subscriber,
                                     'text': news_from_each_category,
                                     'category_name': category.category_name,
                                     'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.username}, новые статьи за прошлую неделю в вашем разделе!',
                from_email='factoryskill@yandex.ru',
                to=[subscriber.email]
            )

            msg.attach_alternative(html_content, 'text/html')
            print()

            # содержимое письма для проверки
            print(html_content)

            # Чтобы запустить реальную рассылку нужно раскоментить
            # msg.send()

# удаление неактуальных задач
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавление работы задачнику
        scheduler.add_job(
            news_sender,

            # для проверки отправки  каждые 10 секунд
            #trigger=CronTrigger(second="*/10"),

            # еженедельная задача на отправку писем
            trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),

            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="news_sender",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена задача 'news_sender'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить,
            # либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Добавление еженедельной задачи: 'delete_old_job_executions'."
        )

        try:
            logger.info("Задачник запущен")
            print('Задачник запущен')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Задачник остановлен")
            scheduler.shutdown()
            print('Задачник остановлен')
            logger.info("Задачник остановлен успешно!")
