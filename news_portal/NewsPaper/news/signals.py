from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.shortcuts import redirect
from django.template.loader import render_to_string
from .models import Category, PostCategory

# создаём функцию обработчик
# запускает выполнение кода при
# сохранение в БД модели Post записи через связь M2M


@receiver(m2m_changed, sender=PostCategory)
def send_sub_mail(sender, instance, **kwargs):
    # получаю текущее действие, их 2 pre_add и post_add, на post_add нет множества id категорий
    action = kwargs.pop('action', None)

    # получаю множество связи M2M поста с категорией (если больше 1й категории)
    pk_set = kwargs.pop('pk_set', None)
    # если действие до добавления связи (в этот момент есть id)
    if action == "pre_add":
        for i in pk_set:  # цикл по количеству категорий у публикации
            sub_text = instance.body
            category = Category.objects.get(pk=i)  # получаю категорию
            subscribers = category.subscribers.all()  # подписчики категории
            post = instance

            for subscriber in subscribers:  # цикл по подписчикам категории
                html_content = render_to_string(
                    'mail_send.html', {'user': subscriber, 'text': sub_text[:150], 'post': post, 'category': category})

                msg = EmailMultiAlternatives(
                    subject=f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе!',
                    from_email='alex.sorokovykh@yandex.ru',
                    to=[subscriber.email]
                )
                msg.attach_alternative(html_content, 'text/html')

                # печать в консоль html письма, для проверки из-за предупреждения о спаме
                print(html_content)

                # ПИСЬМО НЕ ОТПРАВЛЯЕТСЯ
                # msg.send()
    return redirect('/news/')
