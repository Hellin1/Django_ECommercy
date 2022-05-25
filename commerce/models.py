from decimal import MAX_EMAX
from pyexpat import model
from django.db import models
from autoslug import AutoSlugField
from commerce.abstract_models import DateAbstractModel
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

ILLER = (
    ('ist', 'İstanbul'),
    ('ist', 'İstanbul'),
)


import sqlite3

con = sqlite3.connect(r"C:\Users\hal1l\Desktop\d\tr_adres.db")

"""
 butun = {
     'mahalleler' : ((1,'a'),
                    (2,'b'),
                    )
    'ilceler' : 

 }


butun2 = (
    (1, 'mahallle'),
    (2, ''),
    (3, 'c'),
    (4, 'd'),
)


# 3

iller = (
    (1, 'a'),
    (2, 'b'),
    (3, 'c'),
)

ilceler = (
    (1, 'a'),
    (2, 'b'),
)
mahalleler = (
    (1, 'a'),
    (2, 'b'),
)


"""

analiste = []

with con:

    c = con.cursor()
    c.execute(f"SELECT mah.mahalle_adi FROM mahalleler mah  JOIN ilceler ilc ON mah.ilce_id  = ilc.ilce_id")
    mahalleler = c.fetchall()
    # print(len(mahalleler))
    # print(mahalleler[:4])

    count = 0
    for mahalle in mahalleler:
        listem = []
        # print(mahalle[0])
        # print(type(listem))
        listem.append((mahalle[0][:3],mahalle[0]))
        listem = tuple(listem)
        analiste.append((listem[0][0],listem[0][1]))
        # print(listem[0])
        # print((mahalle[0][:3],mahalle[0]))
        # print((mahalle[0][:3],mahalle[0]))
        if count == 1000:
            break
        count += 1
    
# print("analiste: ",analiste)
# print("analiste2: ",tuple(analiste))

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


    


class DenemeAdres(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adres2')
    title = models.CharField(max_length=150, default="s")
    province = models.CharField(max_length=150)
    district = models.CharField( max_length=150)
    neighborhood = models.CharField(max_length=150)
    short_description = models.TextField(max_length=150)
    zip = models.CharField(max_length=100)
    adress_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    tel = PhoneNumberField(blank=False, null=False, default='+905435040968')

    def get_tum_adres(self):
        print("adress_choice: ",ADDRESS_CHOICES)
        return ADDRESS_CHOICES

    def __str__(self):
        return f"{self.short_description} {self.province} {self.district} {self.neighborhood} {self.tel}"


#     # adres.title
    



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



    # def get_absolute_url(self):
    #     from django.urls import reverse
    #     return reverse('', kwargs={'pk': self.pk})

 

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
        return f"{self.urun.baslik}"

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

    def get_toal(self):
        print("adet: ", self.quantity)
        print("price: ", self.urun.price)
        return self.quantity * self.urun.price 
        toal = 0
        for i in self.product.all():
            toal += i.price
        print("toal: ",toal)
        return toal




    class Meta:
        verbose_name = 'sepet'
        verbose_name_plural = 'Sepet'
        db_table = 'sepet'



def get_iller():
    with open(r"C:\Users\hal1l\Desktop\d\iller.txt", "r", encoding="utf-8") as f:
        okunan = f.readlines()
    print("okunan: ", okunan)

    sonuc = []
    for i in okunan:
        sonuc.append((i[:2],i[:-1]))


        




    print(tuple(sonuc))
    return tuple(sonuc)


def get_ilceler():
    #     'zonguldak':(('ilce', 'ilce1'),
    #                  ('ilce2', 'ilce2')
    #                  ('ilce2', 'ilce2') )}

    with open(r"C:\Users\hal1l\Desktop\d\app3.json", "r", encoding="utf-8") as f:
        import json
        sonucx = json.loads(f.read())


    return sonucx

def get_mahalleler(ilce, il):
    print(f"ilce:{ilce}-il:{il}")

    def buyukHarfCevir(sStr):
        str      = sStr
        aranan   = ''
        HARFDIZI = [
                    ('i','İ'), ('ğ','Ğ'),('ü','Ü'), ('ş','Ş'), ('ö','Ö'),('ç','Ç'),
                    ('ı','I')
                ]
        for aranan, harf in HARFDIZI:
            str  = str.replace(aranan, harf)
        str      = str.upper()
        str = str.strip()
        return str





    sonuc = ""
    import os 
    print(os.getcwd())

    import sqlite3

    con = sqlite3.connect(r"C:\Users\hal1l\Desktop\d\tr_adres.db")


    with con:

        c = con.cursor()

        if ilce and il:
            print(ilce.upper(), il.upper())
            print(f"{ilce.upper()}-{il.upper()}")
            print(f"il:{buyukHarfCevir(il)}-ilce:{buyukHarfCevir(ilce)}")
            print("AFYONKARAHİSAR")
            print(buyukHarfCevir(il))
            if buyukHarfCevir(ilce) == "ALADAĞ" and buyukHarfCevir(il)== "AFYONKARAHİSAR":
                print("aynı")

            c.execute(f"SELECT mah.mahalle_adi FROM mahalleler mah  JOIN ilceler ilc ON mah.ilce_id  = ilc.ilce_id WHERE ilc.ilce_adi like '%{buyukHarfCevir(ilce)}%' AND ilc.il_adi like '%{buyukHarfCevir(il)}%'")

        else:
        # c.execute("SELECT * FROM mahalleler WHERE ilce_adi=SEYHAN")
        # c.execute("SELECT * FROM mahalleler WHERE ilce_adi=SEYHAN")
        # SELECT cp.pro_id, cp.price, cp.time FROM computer_components ct INNER JOIN computer_components_prices cp ON ct.pro_id = cp.pro_id WHERE cp.pro_id={gid} ORDER BY cp.pro_id
        # c.execute("SELECT * FROM mahalleler mah  INNER JOIN ilceler ilc ON mah.mahalle_id  = ilc.ilce_id WHERE ilc.ilce_adi='SİNCAN'  LIMIT 10  ")
            c.execute(f"SELECT mah.mahalle_adi, mah.ilce_adi, ilc.il_adi FROM mahalleler mah  JOIN ilceler ilc ON mah.ilce_id  = ilc.ilce_id WHERE ilc.ilce_adi like '%{ilce}%' AND ilc.il_adi like '%{il}%'")

        sonuc = c.fetchall()
        print(sonuc)
        print(len(sonuc))



    return sonuc