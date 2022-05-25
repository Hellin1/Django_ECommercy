from django.shortcuts import get_list_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from traitlets import default
from .models import  AdreslerModel, KategoriModel, UrunlerModel, OrdersModel, SepetModel, YorumModel, get_iller, get_ilceler, get_mahalleler, DenemeAdres
from django.views.generic import ListView
from django.views import View
from commerce.forms import YorumEkleModelForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib import messages
import datetime
import time

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


# anasayfa
def anasayfa(request):
    
    sorgu = request.GET.get('sorgu')
    print("sorgu: ",sorgu)
    # yor = YorumModel.objects.filter(yazan__username='hal1l')
    # for x in yor:
    #     print("yormmm",x.limited_integer_field)
    
    # urunx = UrunlerModel.objects.first()
    # yorumx = urunx.yorumlar.all()
    # yorum = YorumModel.objects.filter(urun=urunx)
    # print("yorumx ", yorumx)
    # for deger in yorumx:
    #     print("loo: ",deger.limited_integer_field)
    # # print("ypu ", yorum.limited_integer_field)
    # print("puan")
    # for j in yorum:
    #     print("puan ",j.limited_integer_field)
    
    # print("yor: ",yorum)
    urunler = UrunlerModel.objects.filter(isActive=True).order_by('-id')
    print('urunlerr: ',urunler)
    
 
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
    paginate_by = 5 


    def get_context_data(self, **kwargs):
        context = super(KategoriListView, self).get_context_data(**kwargs)
        kategori = self.kwargs['kategoriSlug']
        context['kategori'] = kategori
        return context

    def get_queryset(self):
        kategori = KategoriModel.objects.filter(slug=self.kwargs['kategoriSlug'])
        kategori = get_object_or_404(KategoriModel, slug=self.kwargs['kategoriSlug'])
        print(self.kwargs['kategoriSlug'])
        print("kategori: ",kategori)
        return kategori.urunler.all().order_by("?")
        # return kategori.all().order_by('-duzenlenme_tarihi')


def sepetEkleView(request, UrunSlug):
    print(UrunSlug)
    print("get: ",request.GET) 

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
        toplam += i.get_toal()

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

    print("get: ", request.GET)
    print("name: ", request.GET.get('name'))
    print("email: ", request.GET.get('email'))
    print('artir->', request.GET.get('arttır'))
    print('post_id: ', request.GET.get('post_id'))
    
    if request.GET.get('urun'):
        print('true')
        sepet = SepetModel.objects.filter(user=request.user)
        # sepet.filter(urun=request.GET.get('urun'))
        sonuc = sepet.filter(urun=4)
        print("sonuc", sonuc)
        print("ney: ",request.GET.get('urun'))
        sepet.urun  = request.GET.get('urun')
        print("sepeturun: ", sepet)


        # urunu request.GET.get('urun') olan urunu sepet içinde bul
        sepet = SepetModel.objects.filter(user=request.user)
        sepet3 = SepetModel.objects.filter(user=request.user)[int(request.GET.get('urun'))-1]
        print("adet",sepet3.quantity)
        if request.GET.get('updown') == 'arttir':
            print("arttir")
            sepet3.quantity += 1
        elif request.GET.get('updown') == 'azalt':
            print('azalt')
            if sepet3.quantity <= 1:
                pass
            else:
                sepet3.quantity -= 1
            


        adet = sepet3.quantity
        print("adet2",sepet3.quantity)
        print("2. ürün",sepet3)
        sepet3.save()
        
        print('bu ne ', request.GET.get('urun'))
        sonuc = sepet.filter(urun_id=request.GET.get('urun'))
        sonuc2 = sepet.filter(urun=5)
        print('sonucum ', sonuc)
        print('sonucum2 ', sonuc2)
        sonuc = sepet3

        print("toplam: ", sepet3.get_toal())
       
        # sepet = SepetModel.objects.filter(user=request.user)
        # sepet2 = SepetModel.objects.filter(user=request.user).filter(urun__baslik=request.GET.get('urun'))
        # print("spt: ", sepet)
        # sonuc = sepet.filter(urun__baslik=request.GET.get('urun'))
        # sonuc2 = sepet.filter(urun__baslik='Lenovo V15 G2 Intel Core i5 1135G7 8GB RAM 256GB SSD Windows 10 Home 15.6" FHD Taşınabilir Bilgisayar 82KB000RTX')[0]
        # # print("result", sonuc[0])

        # print("sonuc: ", sonuc)
        # print("sonuc2: ", sonuc2)
        # print("aynı mı: ", request.GET.get('urun'))
        # print("1:", sonuc2)
        # print("2:", request.GET.get('urun'))
        # if request.GET.get('urun') == 'Lenovo V15 G2 Intel Core i5 1135G7 8GB RAM 256GB SSD Windows 10 Home 15.6" FHD Taşınabilir Bilgisayar 82KB000RTX':
        #     print('ayni')
        # else:
        #     print('ayni değil')


        # for x in sonuc:
        #     print("quantity: ", x.quantity)
        #     x.quantity += 1
        #     print("x.quantity: ",x.quantity)
        #     x.save()
        # yor = YorumModel.objects.filter(yazan__username='hal1l')
        print("çalıştı")
        toplam = 0
        for i in sepet:
            print(i.urun.price)
            toplam += i.get_toal()
        print(toplam)
        print("ur_toplam: ", sepet3.get_toal())

        return JsonResponse({"valid": True,"ur_ toplam":sepet3.get_toal(),"toplam":toplam, "adet":adet}, status=200)



    simdi = time.time()
    sepet = SepetModel.objects.filter( user=request.user)
    print("sepet: ", sepet)

    tum_fiyat = SepetModel.objects.filter( user=request.user)
    toplam = 0

    for i in tum_fiyat:
        print(i.urun.price)
        print("i: ",i)
        # toplam += i.urun.price
        toplam += i.get_toal()
    print("farklı toplam: ", toplam)
    # sepet = get_object_or_404(SepetModel, slug=UrunSlug)
    print("gecen zaman : ", time.time() - simdi)

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
    # ---
    adresler = DenemeAdres.objects.all()
    adresler = DenemeAdres.objects.filter(user=request.user, default=True)
    adres = DenemeAdres.objects.filter(user=request.user, default=True)
    # ----



    if request.method == 'POST':
        print(request.POST) 
        print("değişti")
        texta = request.POST.get("textim")
        print("ilceler: ",get_ilceler()[texta])
        seciliIlce = request.POST.get("ilce")
        print("seciliIlce: ", seciliIlce)
        print("seciliIlcelength : ", len(seciliIlce))
        print("texta: ", texta)

        if request.POST.get("func2"):
            # func2 ilce
            print("func2: ",request.POST.get("func2"))
            print(request.POST)
            ilce = request.POST.get("ilce")
            print("maahalleler: ", len(get_mahalleler(ilce, texta)), get_mahalleler(ilce, texta)[:10])

            return JsonResponse({"valid": True,'ilceler': get_ilceler()[texta], 'mahalleler': get_mahalleler(ilce, texta)}, status=200)

        return JsonResponse({"valid": True,'ilceler': get_ilceler()[texta]}, status=200)

    # context["mahalleler"] = get_mahalleler(request.POST.get("ilce"), request.POST.get("il"))
    context = {}
    context["adres"] = adresler
    context["sonuc"] = get_iller()
    context["ilceler"] = get_ilceler()
    context["mahalleler"] = get_mahalleler("ALADAĞ","ADANA")
    print("aladağ: ", context["mahalleler"])
    print("mahalleler: ", get_mahalleler("Sultanbeyli", "İstanbul"))

    print("keys: ", context.keys())


    for i in sayi:
        sayac+=1
        print(i)
        

    print("sayi:",   sayi)
    print("bitiş:")
    print("sayac: ", sayac)

    if sayac < 1:
        print("küçük")
        messages.error(request, 'Sepet Boş olamaz')
        return redirect('sepet')
    else:
        print("küçük değil")


    # default adres
    # adresler -> adres1, adres2 

    

    return render(request, 'odeme.html', context={'adres':adres, 'adresler':adresler, 'context': context})

def ozet(request):
    urunler = SepetModel.objects.filter( user=request.user)
    toplam = 0
    for i in urunler:
        print(i.urun.price)
        toplam += i.get_toal()


    if request.method == 'POST':
        print("post ozet")
        


    return render(request, 'ozet.html', context={'toplam': toplam, 'urunler':urunler})


def siparislerim(request):
    # sepet = SepetModel.objects.filter(user=request.user)
    # siparislerim = OrdersModel.objects.filter(user=request.user)
    # OrdersModel.objects.create(
    #     user = request.user,
    #     product = sepet.urun
    # )
    if request.method == 'POST':
        from datetime import date
        print('post edildi')
        urun = SepetModel.objects.first()
        sepetler = SepetModel.objects.filter(user=request.user)
        toplam_fiyat = 0
        for i in sepetler:
            toplam_fiyat += i.get_toal() 

        lo = OrdersModel.objects.create(price=toplam_fiyat, ordered_date=date.today(), ordered=False, user=request.user)
        
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
        
    
    # urunler = get_list_or_404(OrdersModel, user=request.user)
    # print(urunler)
    # urun = SepetModel.objects.filter(user=request.user)

    # urunler = OrdersModel.objects.filter(user=request.user)
    # urunlerx = OrdersModel.objects.filter(user=request.user)
    urunler = OrdersModel.objects.filter(user=request.user)
    print("hata: ", urunler)
    if urunler:
        print("dolu")
        urunler = OrdersModel.objects.filter(user=request.user).latest('start_Date')
    else:
        print("boş")


    
    # print("urunler: ",urunler)
    # print("yupi",urunler.product.all)
    # yes = urunler.product.all()
    # for j in urunler.product.all():
    #     print("j: ",j)

    urunlery = OrdersModel.objects.filter(user=request.user).order_by('-start_Date')

    # if request.method == 'POST':
    #     print('post')
    #     order_item, created = OrdersModel.objects.get_or_create(
    #     urun=urun.urun,
    #     user=request.user,
    #     quantity = urun.quantity,
    # )
    

  
    yes = ""


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



def adresler(request):
    adresler = AdreslerModel.objects.filter(user=request.user)
    # adresler2 = DenemeAdres.objects.create(user=request.user, province=)
    # ---------------
    adresler = DenemeAdres.objects.all()
    adres = DenemeAdres.objects.filter(user=request.user)
    # --------

    if request.method == 'POST':
        print(request.POST) 
        print("değişti")
        texta = request.POST.get("textim")
        print("ilceler: ",get_ilceler()[texta])
        seciliIlce = request.POST.get("ilce")
        print("seciliIlce: ", seciliIlce)
        print("seciliIlcelength : ", len(seciliIlce))
        print("texta: ", texta)

        if request.POST.get("func2"):
            # func2 ilce
            print("func2: ",request.POST.get("func2"))
            print(request.POST)
            ilce = request.POST.get("ilce")
            print("maahalleler: ", len(get_mahalleler(ilce, texta)), get_mahalleler(ilce, texta)[:10])

            return JsonResponse({"valid": True,'ilceler': get_ilceler()[texta], 'mahalleler': get_mahalleler(ilce, texta)}, status=200)

        return JsonResponse({"valid": True,'ilceler': get_ilceler()[texta]}, status=200)

    # context["mahalleler"] = get_mahalleler(request.POST.get("ilce"), request.POST.get("il"))
    context = {}
    context["adres"] = adresler
    context["sonuc"] = get_iller()
    context["ilceler"] = get_ilceler()
    context["mahalleler"] = get_mahalleler("ALADAĞ","ADANA")
    print("aladağ: ", context["mahalleler"])
    print("mahalleler: ", get_mahalleler("Sultanbeyli", "İstanbul"))

    print("keys: ", context.keys())
    
    
    return render(request, 'adresler.html', context={'adres':adres, 'adresler':adresler, 'context': context})
