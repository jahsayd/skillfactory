from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator  # класс позволяющий удобно осуществлять постраничный вывод

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы
    # обратиться к самому списку объектов через HTML-шаблон
    # queryset = Post.objects.order_by('-post_date')
    ordering = ['-post_date']  # сортировка по дате
    paginate_by = 10


# создаём представление, в котором будут детали конкретного отдельного поста
class PostDetailView(DetailView):
    template_name = 'new.html'  # название шаблона будет product.html
    context_object_name = 'new'
    queryset = Post.objects.all()


class SearchResultsView(ListView):
    model = Post
    template_name = 'search.html'
    ordering = ['-post_date']
    paginate_by = 10

    # забираем отфильтрованные объекты переопределяя метод get_context_data у
    # наследуемого класса (полиморфизм)
    def get_context_data(self,
                         **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                          queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostAddView(CreateView):
    template_name = 'post_add.html'
    form_class = PostForm


# дженерик для редактирования объекта
class PostUpdateView(UpdateView):
    template_name = 'post_add.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    context_object_name = 'new_delete'
    success_url = '/news/'



