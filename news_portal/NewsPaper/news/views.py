from django.http import request
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator  # класс позволяющий удобно осуществлять постраничный вывод
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import Post, Category, User, Author
from .filters import PostFilter, CathegoryPostFilter
from .forms import PostForm, ProfileForm
from django.core.cache import cache # импортируем кэш

class PostListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы
    # обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-post_date']  # сортировка по дате
    paginate_by = 10

    #собираем отфильтрованные по категории объекты
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # общаемся к содержимому контекста представления
        id = self.request.GET.get('post_category', )  # получаем ИД категории из Get запроса
        all_cat = Category.objects.all().values_list('pk', flat=True)
        cur_path = self.request.get_full_path()
        check = True
        user_name = self.request.user.username

        # цикл проверки подписан ли текущий юзер на ВСЕ категории
        for i in all_cat:
            z = Category.objects.filter(pk=i).values("subscribers__username")
            if not z.filter(subscribers__username=user_name).exists():
                check = False

        if id != "":
            sub_cat = Category.objects.filter(pk=id).values("subscribers__username")
            context['is_not_subscribe'] = not sub_cat.filter(subscribers__username=self.request.user.username).exists()

        context['subscribe_all'] = check
        context['without_get'] = cur_path == '/news/'
        context['cat_filter'] = CathegoryPostFilter(self.request.GET, queryset=self.get_queryset())
        return context

# подписка на категорию/все категории
@login_required
def add_subscribe(request):
    pk = request.GET.get('post_category', )
    all_cat = Category.objects.all().values_list('pk', flat=True)
    if pk == "":
        for cat in all_cat:
            Category.objects.get(pk=cat).subscribers.add(request.user)
    else:
        Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')

# отписка от категории/всех категорий
@login_required
def unsubscribe(request):
    pk = request.GET.get('post_category', )
    all_cat = Category.objects.all().values_list('pk', flat=True)
    if pk == '':
        for cat in all_cat:
            Category.objects.get(pk=cat).subscribers.remove(request.user)
    else:
        Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/')

# создаём представление, в котором будут детали конкретного отдельного поста
class PostDetailView(DetailView):
    template_name = 'new.html'
    context_object_name = 'new'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'new-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует также.
        # Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'new-{self.kwargs["pk"]}', obj)

        return obj


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

    # def post(self, request, *args, **kwargs):
    #     form = PostForm(request.POST)
    #     cat_pk = request.POST.get('post_category')
    #     sub_text = request.POST.get('body')
    #     sub_title = request.POST.get('heading')
    #     category = Category.objects.get(pk=cat_pk)
    #     subscribers = category.subscribers.all()
    #     # получаем адрес хоста и порта (в нашем случае 127.0.0.1:8000), чтоб в дальнейшем указать его в ссылке
    #     # в письме, чтоб пользователь мог с письма переходить на наш сайт, на конкретную новость
    #     host = request.META.get('HTTP_HOST')
    #
    #     # валидатор - для исключения подмены кода со стороны клиента
    #     if form.is_valid():
    #         news = form.save(commit=False)
    #         news.save()
    #
    #     for subscriber in subscribers:
    #          print('Адреса рассылки:', subscriber.email)
    #          html_content = render_to_string(
    #              'mail_send.html', {'user': subscriber, 'text': sub_text[:50], 'post': news, 'host': host})
    #
    #          msg = EmailMultiAlternatives(
    #              # Заголовок письма, тема письма
    #              subject=f'Здравствуй, {subscriber.username}. Новая статья в твоем любимом разделе!',
    #              # Наполнение письма
    #              body=f'{sub_text[:50]}',
    #              # От кого письмо (должно совпадать с реальным адресом почты)
    #              from_email='alex.sorokovykh@yandex.ru',
    #              # Кому отправлять, конкретные адреса рассылки, берем из переменной, либо можно явно прописать
    #              to=[subscriber.email],
    #          )
    #
    #          msg.attach_alternative(html_content, "text/html")
    #          print(html_content)
    #          msg.send()
    #
    #     return redirect('/news/')

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



