from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from celery.schedules import crontab


# отправка писем подписчикам категории при появлении новой публикации
@shared_task
def send_mail_for_sub_once(sub_uname, sub_email, html_content):
    print('Отправка письма')
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {sub_uname}. Новая статья в твоём любимом разделе!',
        from_email='alex.sorokovykh@yandex.ru',
        to=[sub_email]
    )
    msg.attach_alternative(html_content, 'text/html')
    # проверка содержимого письма в консоли
    print()
    print(html_content)
    print()

    msg.send()
    print('Письмо отправлено')

