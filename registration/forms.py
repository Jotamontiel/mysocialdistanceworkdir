from django import forms
from .models import Profile
from iot_module.models import Company
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['nickName', 'rut', 'gender', 'position', 'workPhone', 'phone', 'nationality']
        widgets = {
            'nickName': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter your NickName', 'style': 'text-transform:none;color:#ffffff;'}),
            'rut': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Rut, e.g. 11222333-k', 'style': 'text-transform:none;color:#ffffff;'}),
            'gender': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#ffffff;background: black;'}),
            'position': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Office Position', 'style': 'text-transform:none;color:#ffffff;'}),
            'workPhone': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter WorkPhone, e.g. +56999123002', 'style': 'text-transform:none;color:#ffffff;'}),
            'phone': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Phone, e.g. +56999123002', 'style': 'text-transform:none;color:#ffffff;'}),
            'nationality': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#ffffff;background: black;'}),
        }
    
    def clean_nickName(self):
        nickName = self.cleaned_data.get("nickName")
        if Profile.objects.filter(nickName=nickName).exists():
            raise ValidationError("The NickName you want to use already exists, please try another one.")
        return nickName
    
    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        if Profile.objects.filter(rut=rut).exists() or Company.objects.filter(rut=rut).exists():
            raise ValidationError("The Rut you want to use already exists, try another please.")
        return rut    
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.initial['gender'] = 'N/A'
        self.initial['nationality'] = 'N/A'

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['avatar', 'birthDate', 'gender', 'position', 'workPhone', 'phone', 'nationality']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'birthDate': DateInput(attrs={'class':'form-control mt-3', 'style': 'color:#ffffff;'}),
            'gender': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#ffffff;background: black;'}),
            'position': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Office Position', 'style': 'text-transform:none;color:#ffffff;'}),
            'workPhone': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter WorkPhone, e.g. +56999123002', 'style': 'text-transform:none;color:#ffffff;'}),
            'phone': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Phone, e.g. +56999123002', 'style': 'text-transform:none;color:#ffffff;'}),
            'nationality': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#ffffff;background: black;'}),
        }

class ProfileAdminForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['user', 'nickName', 'rut', 'gender', 'position', 'workPhone', 'phone', 'nationality']
        widgets = {
            'user': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
            'nickName': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter NickName', 'style': 'text-transform:none;color:#ffffff;'}),
            'rut': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Rut, e.g. 11222333-k', 'style': 'text-transform:none;color:#ffffff;'}),
            'gender': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#ffffff;background: black;'}),
            'position': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Office Position', 'style': 'text-transform:none;color:#ffffff;'}),
            'workPhone': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter WorkPhone, e.g. +56999123002', 'style': 'text-transform:none;color:#ffffff;'}),
            'phone': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Phone, e.g. +56999123002', 'style': 'text-transform:none;color:#ffffff;'}),
            'nationality': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#ffffff;background: black;'}),
        }
    
    def clean_nickName(self):
        nickName = self.cleaned_data.get("nickName")
        if Profile.objects.filter(nickName=nickName).exists():
            raise ValidationError("The NickName you want to use already exists, please try another one.")
        return nickName
    
    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        if Profile.objects.filter(rut=rut).exists() or Company.objects.filter(rut=rut).exists():
            raise ValidationError("The Rut you want to use already exists, try another please.")
        return rut    
    
    def __init__(self, *args, **kwargs):
        super(ProfileAdminForm, self).__init__(*args, **kwargs)
        self.initial['gender'] = 'N/A'
        self.initial['nationality'] = 'N/A'

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required, 254 characters maximum and must be valid.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists() or Company.objects.filter(email=email).exists():
            raise forms.ValidationError("The email is already registered, try another please.")
        return email

class UserEmailUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Required, 254 characters maximum and must be valid.")

    class Meta:
        model = User
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists() or Company.objects.filter(email=email).exists():
                raise forms.ValidationError("The email is already registered, try another please.")
        return email

