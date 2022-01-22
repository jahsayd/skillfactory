from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


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
        user_comment_rate = sum([x['comment_rating'] for x in Comment.objects.filter(post_rel__in=post_author).values()])

        # Расчет рейтинга автора
        self.aut_rating = p_rate * 3 + c_rate + user_comment_rate
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    post_auth = models.ForeignKey(Author, on_delete=models.CASCADE)
    news = 'N'
    article = 'A'
    CONTENT_TYPE = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    cont_type = models.CharField(max_length=1,
                                 choices=CONTENT_TYPE,
                                 default=news)
    post_date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField('Category', through='PostCategory')
    heading = models.CharField(max_length=128)
    body = models.TextField()
    post_rating = models.SmallIntegerField(default=0)

    def like(self):  # Увеличивает рейтинг публикации на 1
        self.post_rating += 1
        self.save()

    def dislike(self):  # Уменьшает рейтинг публикации на 1
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.body[:123] + '...'


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
