from django.db import models
from autoslug import AutoSlugField
from commerce.abstract_models import DateAbstractModel
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

# Create your models here.


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

biralti = (
    (1, '1'),
    (2, '2'),
    (3, '4'),
    (5, '5'),
    )

class KategoriModel(models.Model):
    isim = models.CharField(max_length=30, blank=True, null=True, unique=True)
    slug = AutoSlugField(populate_from='isim', unique = True)

    def __str__(self):
        return self.isim


    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        db_table = 'Kategori'


class UrunlerModel(DateAbstractModel):
    resim = models.ImageField(upload_to='urun_resimleri')
    baslik = models.CharField(max_length=130)
    product = RichTextField()
    stock = models.IntegerField()
    kategoriler = models.ManyToManyField(KategoriModel, related_name='urunler')
    slug = AutoSlugField(populate_from ='baslik', unique=True)
    price = models.FloatField()
    isActive = models.BooleanField(default=True)

    def discount(self):
        import random 
        ind = random.randint(1,75)
        return self.price * ((ind/100)+1)



    def get_al_puan(self):
        toal = 0
        count = 0
        for i in self.yorumlar.all():
            print("i:",i.limited_integer_field)
            toal += i.limited_integer_field
            count += 1
        if toal == 0:
            return 0
        sonuc = round(toal/count,1)
        print("sonuc: ", sonuc)
        sonuc = str(sonuc)
        
        if (sonuc[2]) == '0':
            sonuc = (sonuc[0]) 

        return sonuc

    class Meta:
        verbose_name = 'Urun'
        verbose_name_plural = 'Urunler'
        # veritabanın da gözükücek isim
        db_table = 'Urun'

    def __str__(self):
        return f"{self.baslik}"
        # return f"deneme lo deneme"


class AdreslerModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adres')
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Adresler'
        verbose_name = 'Adres'
        db_table = 'Adress'

    def __str__(self):
        return self.user.username


class OrdersModel(DateAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(UrunlerModel, related_name='order')
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    start_Date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField()
    # adres
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    

    
    # stock = models.ForeignKey(Urunler, related_name='stock', on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Siparis'
        verbose_name_plural = 'Siparisler'
        db_table = 'Siparis'

    def __str__(self):
        return f"{self.id} + {self.product} "

    def get_toal(self):
        toal = 0
        for i in self.product.all():
            toal += i.price
        print("toal: ",toal)
        return toal

class YorumModel(models.Model):
    yazan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='yorum')
    urun = models.ForeignKey(UrunlerModel, on_delete=models.CASCADE, related_name='yorumlar')
    yorum = models.TextField(null=True, blank=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    limited_integer_field = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])

    def __str__(self):
        return f"{self.yorum[:10]} {self.limited_integer_field}"


    # def get_total_point(self):
    #     # total = 0
    #     # for item in self.limited_integer_field.all():
    #     #     total+=item
    #     # count = self.limited_integer_field.count()
    #     # print(total/count)

    #     # from django.db.models import Avg

        
    #     # total = self.objects.aggregate(Avg('limited_integer_field'))
    #     total = 0
    #     total = 0
    #     print("tabi efendim: ",self.limited_integer_field)
    #     # for order_item in:
    #     #     total += order_item.self
        
   

    class Meta:
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'
        db_table = 'yorum'



class SepetModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='sepet')
    # urunlermodel deki data  silinirse sepete nolcak 
    urun = models.ForeignKey(UrunlerModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} | {self.urun.baslik}"

    def get_tum_fiyat(self):
        return self.quantity * self.urun.price


    def get_total(self):
        # total = 0
        # for order_item in self.urun.all():
        #     total += order_item.get_tum_fiyat()
        # if self.coupon:
        #     total -= self.coupon.amount
        from django.db.models import Avg
        total =  self.urun.aggregate(Avg('price'))

        return total



    class Meta:
        verbose_name = 'sepet'
        verbose_name_plural = 'Sepet'
        db_table = 'sepet'


def al_sepet():
    total = SepetModel.objects.aggregate(Avg('price'))