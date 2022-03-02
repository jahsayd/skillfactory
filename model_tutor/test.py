from django.db import models
from django.contrib.auth.models import User  # Д.2 Импортируем встроенную модель User
from django.db.models import Sum  # Д.2 Импортируем функцию Sum


class Author(models.Model):  # Модель "Автор"
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)  # Поле "автор" со связью "Один-к-Одному" с User
    ratingAuthor = models.SmallIntegerField(default=0)  # Поле "рейтинг", по умолчанию "0"

    def update_rating(self):  # Обновление рейтинга автора

        postRat = self.post_set.aggregate(postRating=Sum('rating'))  # к связанной модели "post_set" применяем функция "aggregate" которое Суммирует поле "рейтинг"
        pRat = 0  # промежуточная переменная
        pRat += postRat.get('postRating')  # получаем итог рейинга с "postRating"

        commentRat = self.authorUser.comment_set.aggtegate(commentRating=Sum('rating'))  # к связанной модели "authorUser" применяем функция "aggregate" которое Суммирует поле "рейтинг"
        cRat = 0  # промежуточная переменная
        cRat += commentRat.get('commentRating')  # получаем итог рейинга с "commentRating"

        self.ratingAuthor = pRat * 3 + cRat  # пост "рейтинг" * 3 и прибавляется рейтиг "статьи"
        self.save()  # сохраняем нашу модель




class Category(models.Model):  # Модель "Категории"

    name = models.CharField(max_length=64, unique=True)  # поле "имя", макс_длинна=64, унакальность=да


class Post(models.Model): # Модель "Пост"

    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # поле "автор", со связью "Многие-к-Одному" с моделью "Автор"

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES =(
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)  # поле "Выбор категории", макс_длинна=2, выбор=выбор категорий, по умолчанию="статья"
    dateCreation = models.DateTimeField(auto_now_add=True)  # поле "Дата сооздания", автоматически добавлять дату и время=Да
    postCategory = models.ManyToManyField(Category, through='PostCategory')  # поле "Пост_категории", со связь "Многие-ко-Многим" с моделью "Категории", через="Пост_категории"
    title = models.CharField(max_length=128)  # поле "Заголовок", макс_длинна=128
    text = models.TextField()  # поле "Текст"
    rating = models.SmallIntegerField(default=0)  # # Поле "рейтинг", по умолчанию "0"

    def like(self):  # метод класса "лайк"
        self.rating += 1  # поле объект.рейтинг + 1
        self.save()  # записываем изменение

    def dislike(self):  # метод класса "дислайк"
        self.rating -= 1  # поле объект.рейтинг - 1
        self.save()  # записываем изменение

    def preview(self):
        return f'{self.text[:78]} ...'  # возвращаем 78 символов с начала текста


class PostCategory(models.Model):  # промежуточная модель "Посты-Категории"

    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)  # поле "через_пост", модель "Многие-к-Одному", через "Пост", удаление=сразу
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)  # поле "через_категории", модель "Многие-к-Одному", через "Пост", удаление=сразу


class Comment(models.Model):  # модель "Коментарии"
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)  # поле "коментарий_пост", модель "Многие-к-Одному", через "Пост", удаление=сразу
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)  # поле "коментарий_юзер", модель "Многие-к-Одному", через "Пост", удаление=сразу
    text = models.TextField()  # поле "текст"
    dateCreation = models.DateTimeField(auto_now_add=True)  # поле "Дата сооздания", автоматически добавлять дату и время=Да
    rating = models.SmallIntegerField(default=0)  # # Поле "рейтинг", по умолчанию "0"

    def like(self):  # метод класса "лайк"
        self.rating += 1  # поле объект.рейтинг + 1
        self.save()  # записываем изменение

    def dislike(self):  # метод класса "дизлайк"
        self.rating -= 1  # поле объект.рейтинг - 1
        self.save()  # записываем изменение

    def __str__(self):  # функция которая выводит правильно в админ-панель
       return f'{self.commentUser}: {self.text[:20]}'