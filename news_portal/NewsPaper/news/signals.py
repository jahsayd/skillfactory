from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.shortcuts import redirect
from django.template.loader import render_to_string
from .models import Category, PostCategory
from .tasks import send_mail_for_sub_once

# создаём функцию обработчик
# запускает выполнение кода при
# сохранение в БД модели Post записи через связь M2M


@receiver(m2m_changed, sender=PostCategory)
def send_sub_mail(sender, instance, **kwargs):
    # получаю текущее действие, из 2 pre_add и post_add, на post_add нет множества id категорий
    action = kwargs.pop('action', None)
    # получаю множество связи M2M поста с категорией (если больше 1й категории)
    pk_set = kwargs.pop('pk_set', None)
    # если действие до добавления связи M2M (в этот момент есть id)
    if action == "pre_add":
        for i in pk_set:  # цикл по количеству категорий у публикации
            sub_text = instance.body
            category = Category.objects.get(pk=i)  # получаю категорию
            subscribers = category.subscribers.all()  # подписчики категории
            post = instance

            for subscriber in subscribers:  # цикл по подписчикам категории
                html_content = render_to_string(
                    'mail_send.html', {'user': subscriber, 'text': sub_text[:150], 'post': post, 'category': category})
                sub_uname = subscriber.username
                sub_email = subscriber.email

                # функция для таска, передаем в нее все что нужно для отправки подписчикам письма

                send_mail_for_sub_once.delay(sub_uname, sub_email, html_content)

    return redirect('/news/')
