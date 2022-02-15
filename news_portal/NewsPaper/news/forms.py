from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.forms import ModelForm
from .models import Post, User


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель,
    # по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['post_auth', 'cont_type', 'post_category', 'heading', 'body']


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
