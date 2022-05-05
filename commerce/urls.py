from django.urls import path
from .views import (
    anasayfa, anasayfa,
    KategoriListView,
    sepetView, DetayView,
    sepetEkleView,
    SepetUrunSilDeleteView,
    YorumEkleFormView,
    HepsiniSil, onay,
    ozet, siparislerim,
    yeni,star, denme,  yorum_sil)

from django.views.generic import TemplateView, RedirectView


urlpatterns = [  
    path('siparis', siparislerim, name='siparislerim'),
    path('', anasayfa, name="index"),
    # path('ss', anasayfa, name="anasayfa"),
    path('kategori/<slug:kategoriSlug>', KategoriListView.as_view(), name="kategori"),
    path('sepet/<slug:UrunSlug>', sepetEkleView, name='sepete-ekle'),
    path('sepet/', sepetView, name='sepet'),
    path('urun/<slug:UrunSlug>', DetayView.as_view(), name="detay"),
    path('hesabim', TemplateView.as_view(
        template_name = 'hesabim.html'
    ), name='hesabım'),
    path('sil/<slug:UrunSlug>', SepetUrunSilDeleteView, name='urun-sil'),
    path('yorum-yap',  YorumEkleFormView, name='yorum-ekle'),
    path('yorum-sil/<int:id>', yorum_sil, name='yorum-sil'),
    path('hepsini-sil', HepsiniSil, name='hepsini-sil'),
    path('onay', onay, name='onayla'),
    path('ozet', ozet , name='ozet'),
    path('yeni', yeni, name='yeni'),
    path('star', star, name='star'),
    path('denme', denme, name='denme'),
]