from django import forms
from django.forms import fields
from commerce.models import YorumModel

class YorumEkleModelForm(forms.ModelForm):
    CHOICES=[(1,''),
         (2,''),
         (3,''),
         (4,''),
         (5,''),
         ]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = YorumModel
        fields = ('yorum', 'rating')
        labels= {
            'yorum': '', 'rating':''
        }
        widgets = {
            'yorum': forms.TextInput(attrs={'class': 'myfieldclass'}),
          
        }

