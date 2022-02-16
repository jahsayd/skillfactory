from django.http import request
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator  # класс позволяющий удобно осуществлять постраничный вывод
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post, Category, User, Author
from .filters import PostFilter, CathegoryPostFilter
from .forms import PostForm, ProfileForm


class PostListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы
    # обратиться к самому списку объектов через HTML-шаблон
    # queryset = Post.objects.order_by('-post_date')
    ordering = ['-post_date']  # сортировка по дате
    paginate_by = 10

    #собираем отфильтрованные по категории объекты
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_filter'] = CathegoryPostFilter(self.request.GET, queryset=self.get_queryset())
        return context


# создаём представление, в котором будут детали конкретного отдельного поста
class PostDetailView(DetailView):
    template_name = 'new.html'
    context_object_name = 'new'
    queryset = Post.objects.all()


# представление данных пользователя
class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    context_object_name = 'profile'

    #получаю объект текущего зарегистрированного пользователя
    def get_object(self, **kwargs):
        id = self.request.user.id
        return User.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profile_edit.html'
    form_class = ProfileForm
    success_url = '/profile/'

    # получаю объект текущего зарегистрированного пользователя
    def get_object(self, **kwargs):
        id = self.request.user.id
        return User.objects.get(pk=id)


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/profile')

class SearchResultsView(ListView):
    model = Post
    template_name = 'search.html'
    ordering = ['-post_date']
    paginate_by = 10

    # забираем отфильтрованные объекты переопределяя метод get_context_data у
    # наследуемого класса (полиморфизм)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                          queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostAddView(PermissionRequiredMixin, CreateView):
    template_name = 'post_add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)


# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'post_add.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    context_object_name = 'new_delete'
    success_url = '/news/'
    permission_required = ('news.delete_post',)



