from itertools import product
from django.shortcuts import get_list_or_404, redirect, render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import  KategoriModel, UrunlerModel, OrdersModel, SepetModel, YorumModel
from django.views.generic import ListView
from django.views import View
from commerce.forms import YorumEkleModelForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib import messages

# Create your views here.

# def yazdir(request):
#     urun = UrunlerModel.objects.filter(isActive=True)
#     siparis = OrdersModel.objects.all()
#     # deger = Urunler.objects.first()
#     # deger = deger.order.all()
#     # deger = UrunlerModel.objects.get(pk=1)
#     deger = UrunlerModel.objects.all()
#     # deger = deger.order.all()

#     print("sa")
#     return render(request, 'anasayfa.html', context={'urun':urun, 'siparis': siparis, 'deger':deger})


from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

def star(request):
    print(request.GET.get('rating'))
    print('render edildi')

    return render(request, 'star-rate.html', context={'star': star})




# anasayfa
def anasayfa(request):
    
    sorgu = request.GET.get('sorgu')
    print("sorgu: ",sorgu)
    yor = YorumModel.objects.filter(yazan__username='hal1l')
    for x in yor:
        print("yormmm",x.limited_integer_field)
    
    urun = UrunlerModel.objects.get(id='2')
    urunx = UrunlerModel.objects.first()
    yorumx = urunx.yorumlar.all()
    yorum = YorumModel.objects.filter(urun=urunx)
    print("yorumx ", yorumx)
    for deger in yorumx:
        print("loo: ",deger.limited_integer_field)
    # print("ypu ", yorum.limited_integer_field)
    print("puan")
    for j in yorum:
        print("puan ",j.limited_integer_field)
    
    print("yor: ",yorum)
    urunler = UrunlerModel.objects.filter(isActive=True).order_by('-id')
    print('urunlerr: ',urunler)
    
    # for x in urunler:

    #         print("yorumlar: ",x.yorumlar.limited_integer_field)
        # print("tabi efendim: ",x.yorumlar.get_total_point)

    print("urunler: ", urunler)
    if sorgu:
        urunler = urunler.filter(
            Q(baslik__icontains=sorgu) |
            Q(product__icontains=sorgu )
        ).distinct()
    # urunler = urunler.objects.all()
    print("urunler: ",urunler)
    sayfa = request.GET.get('sayfa')
    # sayfa = 2
    paginator = Paginator(urunler, 3)
    # denme\index.html

    

    return render(request, 'anasayfa.html', context={
        'urunler': paginator.get_page(sayfa), 'sorgu':sorgu
    })


class KategoriListView(ListView):
    template_name = 'kategori.html'
    # hangi isimle gönderilecek
    context_object_name = 'urunler'
    paginate_by = 2

    def get_queryset(self):
        kategori = get_object_or_404(KategoriModel, slug=self.kwargs['kategoriSlug'])
        print(self.kwargs['kategoriSlug'])
        print("kategori: ",kategori)
        return kategori.urunler.all().order_by("?")
        # return kategori.all().order_by('-duzenlenme_tarihi')


def sepetEkleView(request, UrunSlug):
    print(UrunSlug)
    urun  = get_object_or_404(UrunlerModel, slug= UrunSlug)
    order_item, created = SepetModel.objects.get_or_create(
        urun=urun,
        user=request.user,
    )
    print("order_item: ",order_item)
    # oder_item : def __str__ nin yanıtını döndürür
    # created : eğer oluştuysa true değeri verir
    print("created: ",created)

    sepet = SepetModel.objects.filter( user=request.user)
    print("sepet: ", sepet)

    tum_fiyat = SepetModel.objects.filter( user=request.user)
    toplam = 0
    for i in tum_fiyat:
        print(i.urun.price)
        toplam += i.urun.price

    # sepet = get_object_or_404(SepetModel, slug=UrunSlug)


    return render(request, 'sepet.html', context={'sepet':sepet, 'tum_fiyat': toplam})


    
class DetayView(View):
    http_method_names = ['get', 'post']
    yorum_ekleme_formu = YorumEkleModelForm

    def get(self, request, UrunSlug):
        urun = get_object_or_404(UrunlerModel, slug=UrunSlug)

        if request.user.is_authenticated:
            # info seviyesinde log oluşturma
            # logger.info('konu okundu: ' + request.user.username)
            pass
        yorumlar  = urun.yorumlar.order_by("-id")
        return render(request, 'detay.html', context={
            'urun': urun,
            'yorumlar': yorumlar,
            'yorum_ekle_form': self.yorum_ekleme_formu()
        })

    def post(self, request, UrunSlug):
        star = request.POST.get('rating')
        print("star: ",star)
        print(request)
        print(list(request.GET.items()))
        urun = get_object_or_404(UrunlerModel, slug=UrunSlug)
        yorum_ekle_form = self.yorum_ekleme_formu(data=request.POST)
        

        if yorum_ekle_form.is_valid():
            # commit false önemli
            # yorum = yorum_ekle_form.save(commit=False)
            # yorum.yazan = request.user
            # yorum.urun  = urun
            # yorum.save()
            # # messages.success(request, 'Yorum başarılı bir şekilde eklendi.')
            limited_integer_field=request.POST['rating']
            yorum = request.POST['yorum']
            obj, created = YorumModel.objects.update_or_create(
                        yazan = request.user, urun=urun,
                        defaults={ 'limited_integer_field':request.POST['rating'], 'yorum':yorum },
                        )   
        
        # print(yorum_ekle_formu.cleaned_data)
        print('cevaps: ',list(request.POST.items()))
        print(request.POST["rating"])


        print("urunSlug: ",UrunSlug)
        return redirect('detay', UrunSlug= UrunSlug)

def denme(request):
    star = request.POST.get('rating')
    print(star)
    print(request)
    print(list(request.GET.items()))

    yorum_ekle_formu = YorumEkleModelForm

    if request.method == 'POST':
        urun = UrunlerModel.objects.order_by('-id')[0]
        print('post')
        yorum_ekle_form = yorum_ekle_formu(data=request.POST)
        if yorum_ekle_form.is_valid():
        #     yorum = yorum_ekle_form.save(commit=False)
        #     yorum.yazan = request.user
        #     yorum.urun =  urun
        #     # yorum.limited_integer_field = request.POST['rating']
        #     yorum.save()
            limited_integer_field=request.POST['rating']
            yorum = request.POST['yorum']
            obj, created = YorumModel.objects.update_or_create(
                        yazan = request.user, urun=urun,
                        defaults={ 'limited_integer_field':request.POST['rating'], 'yorum':yorum },
                        )   
        
        # print(yorum_ekle_formu.cleaned_data)
        print('cevaps: ',list(request.POST.items()))
        print(request.POST["rating"])


        # le = get_object_or_404(YorumModel ,yazan=request.user, yorum=request.POST['yorum'])
        # le.update(limited_integer_field=request.POST["rating"])


    return render(request, 'denme.html', context={
    'star':star, 
    'yorum_ekle_form': yorum_ekle_formu,

    })


class YaziSilDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('giris')
    template_name = 'pages/yazi-sil-onay.html'
    success_url = reverse_lazy('yazilarim')

    def get_queryset(self):
        yazi = SepetModel.objects.filter(user= self.request.user)
        return yazi


def sepetView(request):

    sepet = SepetModel.objects.filter( user=request.user)
    print("sepet: ", sepet)

    tum_fiyat = SepetModel.objects.filter( user=request.user)
    toplam = 0
    for i in tum_fiyat:
        print(i.urun.price)
        toplam += i.urun.price

    # sepet = get_object_or_404(SepetModel, slug=UrunSlug)


    return render(request, 'sepet.html', context={'sepet':sepet, 'tum_fiyat': toplam})


# class SepetUrunSilDeleteView(LoginRequiredMixin, DeleteView):
#     login_url = reverse_lazy('giris')
#     template_name = 'pages/urun-sil-onay.html'
#     success_url = reverse_lazy('sepet')

#     def get_queryset(self):
#         sepet = SepetModel.objects.filter(urun = self.kwargs["UrunSlug"]  ,user= self.request.user)
#         return sepet


@login_required(login_url='/')
def SepetUrunSilDeleteView(request, UrunSlug):
    get_object_or_404(SepetModel,  urun__slug=UrunSlug, user=request.user).delete()
    return redirect('sepet')


def YorumEkleFormView(request):
    return render(request, 'yorum-yap.html', context={})



def HepsiniSil(request):
    sepet = SepetModel.objects.filter(user=request.user).delete()
    return redirect('sepet')

def onay(request):
    # sayi = SepetModel.objects.count(user=request.user)
    # sayi = SepetModel.objects.annotate(urun=Count(user=request.user))
    sayac = 0

    sayi = SepetModel.objects.filter(user=request.user)
    sayi = SepetModel.objects.filter(user=request.user)
    for i in sayi:
        sayac+=1
        print(i)
        

    print("sayi:", sayi)
    print("bitiş:")
    print("sayac: ", sayac)

    if sayac < 1:
        print("küçük")
        messages.error(request, 'Sepet Boş olamaz')
        return redirect('sepet')
    else:
        print("küçük değil")

    return render(request, 'odeme.html', context={})

def ozet(request):
    tum_fiyat = SepetModel.objects.filter( user=request.user)
    toplam = 0
    for i in tum_fiyat:
        print(i.urun.price)
        toplam += i.urun.price


    return render(request, 'ozet.html', context={'toplam': toplam})


def siparislerim(request):
    # sepet = SepetModel.objects.filter(user=request.user)
    # siparislerim = OrdersModel.objects.filter(user=request.user)
    # OrdersModel.objects.create(
    #     user = request.user,
    #     product = sepet.urun
    # )
    if request.method == 'POST':
        from datetime import date
        print('post ettin güzelim')
        urun = SepetModel.objects.first()
        sepetler = SepetModel.objects.filter(user=request.user)
        lo = OrdersModel.objects.create(price=3, ordered_date=date.today(), ordered=False, user=request.user)
        
        for i in sepetler:
            print("i:",i.urun)
            lo.product.add(i.urun)
            
        SepetModel.objects.filter(user=request.user).delete()
        # sepet = get_list_or_404(SepetModel, user=request.user)
        # print("sepet: ", sepet)
        # urunlerc  = get_list_or_404(SepetModel, user= request.user)
        # urunlerc = SepetModel.objects.filter(user=request.user)
        # print("urunlwerc: ",urunlerc)
        # # for urun in urunlerc:
        # #     print("urun: ",urun.quantity)
        # #     print(urun.urun)
        # #     order_item, created = OrdersModel.objects.create(
        # # product=urun.urun,
        # # )
        # instance = OrdersModel.objects.create(
        #     price=urunlerc.price)
        # instance.product = urun
        
    
    urunler = get_list_or_404(OrdersModel, user=request.user)
    print(urunler)
    urun = SepetModel.objects.filter(user=request.user)

    urunler = OrdersModel.objects.filter(user=request.user)
    urunlerx = OrdersModel.objects.filter(user=request.user)
    urunler = OrdersModel.objects.filter(user=request.user).latest('start_Date')



    
    print("urunler: ",urunler)
    print("yupi",urunler.product.all)
    yes = urunler.product.all()
    for j in urunler.product.all():
        print("j: ",j)

    urunlery = OrdersModel.objects.filter(user=request.user).order_by('-start_Date')
    

    # zippl = urunlerx.product.get()
    # for staff in urunler:
    #     print(staff.product.all())

    # if request.method == 'POST':
    #     print('post')
    #     order_item, created = OrdersModel.objects.get_or_create(
    #     urun=urun.urun,
    #     user=request.user,
    #     quantity = urun.quantity,
    # )
    

    # print("uruner: ",urunler)
    # for x in urunler:
    #     print(x.product)


    return render(request, 'siparislerim.html', context={'urun':urunler,'zippl': yes, 'urunlery':urunlery})

def yeni(request):
    return redirect('index')


@login_required(login_url='/')
def yorum_sil(request, id):
    yorum = get_object_or_404(YorumModel, id=id)
    if yorum.yazan == request.user or yorum.yazi.yazar == request.user:
        yorum.delete()
        messages.success(request, "Yorum Başarıyla Silindi")
        return redirect('detay', UrunSlug=yorum.urun.slug)
    return redirect('index')