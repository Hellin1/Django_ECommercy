from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from account.forms import KayitFormu, ProfilDuzenlemeForm
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



def cikis(request):
    logout(request)
    return redirect("index")


def kayit(request):
    print("request: get: ",request.POST.get("bencheckbox"))
    if request.method == 'POST':
        form = KayitFormu(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password= password)
            login(request, user)
            return redirect('index')

    else:
        form = KayitFormu()
    return render(request, 'pages/kayit.html', context= {
        'form': form        
    })



class ProfilDetailView(DetailView):
    template_name = 'pages/profil.html'
    # profil html üzerinden hangi isimle ulaşılacak
    context_object_name = 'profil'

    def get_object(self):
        return get_object_or_404(
            User, username = self.kwargs.get("username")
        )


@login_required(login_url="/")
def profil_guncelle(request):
    if request.method == 'POST':
        form = ProfilDuzenlemeForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'PROFİL GÜNCELLENDİ')
    else:
        form = ProfilDuzenlemeForm(instance = request.user)
    return render(request, 'pages/profil-guncelle.html', context= {
        'form': form
    })

@login_required(login_url="/")
def sifre_degistir(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            kullanici = form.save()
            update_session_auth_hash(request, kullanici)
            messages.success(request, "Şifre başarıyla değiştirildi")
            return redirect('sifre-degistir')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'pages/sifre-degistir.html', context= {
        'form': form
    })



from django.shortcuts import get_object_or_404

class ProfilDetailView(DetailView):
    template_name = 'pages/profil.html'
    # profil html üzerinden hangi isimle ulaşılacak
    context_object_name = 'profil'

    def get_object(self):
        return get_object_or_404(
            User, username = self.kwargs.get("username")
        )


