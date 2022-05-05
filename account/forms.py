from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class KayitFormu(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2')


class ProfilDuzenlemeForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

            