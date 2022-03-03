from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    aut_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        # Сумма рейтинга за посты автора
        post_rate = self.post_set.aggregate(postRating=Sum('post_rating'))
        p_rate = 0
        p_rate += post_rate.get('postRating')

        # Сумма рейтинга за комментарии автора
        comment_rate = self.author.comment_set.aggregate(commentRating=Sum('comment_rating'))
        c_rate = 0
        c_rate += comment_rate.get('commentRating')

        # Сумма рейтинга комментариев к постам автора
        post_author = self.post_set.all()
        user_comment_rate = \
            sum([x['comment_rating'] for x in Comment.objects.filter(post_rel__in=post_author).values()])

        # Расчет рейтинга автора
        self.aut_rating = p_rate * 3 + c_rate + user_comment_rate
        self.save()

    def __str__(self):
        return f'{self.author}'


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    post_auth = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    news = 'N'
    article = 'A'
    CONTENT_TYPE = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    cont_type = models.CharField(max_length=1,
                                 choices=CONTENT_TYPE,
                                 default=news,
                                 verbose_name='Тип публикации')
    post_date = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    post_category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория', related_name='category')
    heading = models.CharField(max_length=128, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст')
    post_rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    def like(self):  # Увеличивает рейтинг публикации на 1
        self.post_rating += 1
        self.save()

    def dislike(self):  # Уменьшает рейтинг публикации на 1
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.body[:123] + '...'

    # добавим абсолютный путь, чтобы после создания нас
    # перебрасывало на страницу с новостью
    def get_absolute_url(self):
        return f'/news/{self.id}'

    # переопределяем метод для удаления ключа объекта
    # из кэша после изменения объекта
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'new-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_rel = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_rel = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.SmallIntegerField(default=0)

    def like(self):  # Увеличивает рейтинг комментария на 1
        self.comment_rating += 1
        self.save()

    def dislike(self):  # Уменьшает рейтинг комментария на 1
        self.comment_rating -= 1
        self.save()
