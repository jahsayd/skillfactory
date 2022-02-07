from django.urls import path
from .views import PostListView, PostDetailView, SearchResultsView, PostAddView, PostDeleteView, PostUpdateView

urlpatterns = [
        path('', PostListView.as_view(), name='post_list'),
        # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
        path('<int:pk>', PostDetailView.as_view(), name='new'),
        # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
        path('search/', SearchResultsView.as_view(), name='search_results'),
        path('add/', PostAddView.as_view(), name='post_add'),
        path('<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
        path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
]
