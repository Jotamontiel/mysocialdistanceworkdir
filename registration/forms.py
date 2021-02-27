from django import forms
from .models import Profile
from django.core.exceptions import ValidationError
from .choices import COUNTRY_CHOICES, GENDER_CHOICES

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['nickName', 'avatar', 'rut', 'birthDate', 'gender', 'position', 'workPhone', 'phone', 'nationality']
        widgets = {
            'nickName': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter your NickName', 'style': 'text-transform:none;color:#d9534f;background: black;'}),
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'rut': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter your Rut or Unique Identifier, example: 11222333-k', 'style': 'text-transform:none;color:#d9534f;background: black;'}),
            'birthDate': forms.DateInput(attrs={'class':'form-control mt-3 date has-value datepicker', 'placeholder':'Enter your Birthday, example: YYYY-MM-DD', 'style': 'text-transform:none;color:#f0ad4e;background: black;'}),
            'gender': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#f0ad4e;background: black;'}),
            'position': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter your Office Position', 'style': 'text-transform:none;color:#f0ad4e;background: black;'}),
            'workPhone': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter your Work Phone, example: +56999123002', 'style': 'text-transform:none;color:#f0ad4e;background: black;'}),
            'phone': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter your Phone, example: +56999123002', 'style': 'text-transform:none;color:#f0ad4e;background: black;'}),
            'nationality': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#f0ad4e;background: black;'}),
        }
    
    def clean_nickName(self):
        nickName = self.cleaned_data.get("nickName")
        if Profile.objects.filter(nickName=nickName).exists():
            raise ValidationError("The NickName you want to use already exists, please try another one.")
        return nickName
    
    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        if Profile.objects.filter(rut=rut).exists():
            raise ValidationError("The Rut you want to use already exists, try another please.")
        return rut    
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.initial['gender'] = 'N/A'
        self.initial['nationality'] = 'N/A'