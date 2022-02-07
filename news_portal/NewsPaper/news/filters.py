import django_filters
from django.forms import DateInput
from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики


from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    post_date = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        label='Позже',
        lookup_expr='gt'
        )
    heading = django_filters.CharFilter(
        label='Заголовок',
        lookup_expr='icontains')
    # new_post_auth = django_filters.ChoiceFilter(field_name='post_auth', label='Автор')
    # Здесь в мета классе надо предоставить модель и указать поля,
    # по которым будет фильтроваться информация о публикациях
    class Meta:
        model = Post
        fields = ('post_date', 'heading', 'post_auth')  # поля модели, которые мы будем фильтровать