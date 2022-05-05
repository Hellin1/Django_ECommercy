from django.contrib import admin
from commerce.models import AdreslerModel, KategoriModel, SepetModel, UrunlerModel, OrdersModel, YorumModel
# Register your models here.

#admin.register(Urunler)
#admin.site.register(Urunler)



@admin.register(UrunlerModel)
class UrunlerAdmin(admin.ModelAdmin):
    # eklerken 
    search_fields = ('baslik', 'resim','product')
    list_display = ('baslik','olusturulma_tarihi','duzenlenme_tarihi')


admin.site.register(OrdersModel)
admin.site.register(AdreslerModel)
admin.site.register(KategoriModel)
admin.site.register(YorumModel)
admin.site.register(SepetModel)