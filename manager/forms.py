from django import forms
from django.forms import fields, widgets
from .models import CreatePasswordModel

class DateInput(forms.DateInput):
    input_type = 'date'

class CreatePasswordForm(forms.ModelForm):
    class Meta:
        model = CreatePasswordModel
        fields = ['password', 'used_for_website', 'retired_date', 'explanation']
        widgets = {
            'retired_date' : DateInput(format='%d%m%Y'),
            'password' : forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'password'})
        }
class GeneratePasswordForm(forms.Form):
    CHOICES = (
        ('8' , '8'),
        ('9' , '9'),
        ('10' , '10'),
        ('11' , '11'),
        ('12' , '12'),
        ('13' , '13'),
        ('14' , '14'),
        ('15' , '15'),
        ('16' , '16'),
        ('17' , '17'),
        ('18' , '18'),
        ('19' , '19'),
        ('20' , '20'),
        ('21' , '21'),
        ('22' , '22'),
        ('23' , '23'),
        ('24' , '24'),
        ('25' , '25'),
        ('26' , '26'),
        ('27' , '27'),
        ('28' , '28'),
        ('29' , '29'),
        ('30' , '30'),
        ('31' , '31'),
        ('32' , '32'),
    )
    passwordLength = forms.CharField(label="Password Length",widget=forms.Select(choices=CHOICES))
    has_letters = forms.BooleanField(label="Letters",widget=forms.CheckboxInput, required= True)
    has_mixed_case = forms.BooleanField(label="Mixed Case",widget=forms.CheckboxInput, required= False)
    has_panctuation = forms.BooleanField(label="Panctuation",widget=forms.CheckboxInput, required= False)
    has_numbers = forms.BooleanField(label="Numbers",widget=forms.CheckboxInput, required= False)
