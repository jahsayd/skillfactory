# Generated by Django 4.0.1 on 2022-02-16 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=64, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='post',
            name='cont_type',
            field=models.CharField(choices=[('N', 'Новость'), ('A', 'Статья')], default='N', max_length=1, verbose_name='Тип публикации'),
        ),
        migrations.AlterField(
            model_name='post',
            name='heading',
            field=models.CharField(max_length=128, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_auth',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_category',
            field=models.ManyToManyField(through='news.PostCategory', to='news.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_rating',
            field=models.SmallIntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category', verbose_name='Категория'),
        ),
    ]
