from django import forms
from .models import Company, Component
from registration.models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['businessName', 'rut', 'address', 'number', 'office', 'country', 'postalCode', 'phone', 'email']
        widgets = {
            'businessName': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Business Name', 'style': 'text-transform:none;color:#ffffff;'}),
            'rut': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Company Rut, e.g. 11222333-k', 'style': 'text-transform:none;color:#ffffff;'}),
            'address': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Address', 'style': 'text-transform:none;color:#ffffff;'}),
            'number': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Number', 'style': 'text-transform:none;color:#ffffff;'}),
            'office': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Office', 'style': 'text-transform:none;color:#ffffff;'}),
            'country': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
            'postalCode': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Postal Code', 'style': 'text-transform:none;color:#ffffff;'}),
            'phone': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Phone', 'style': 'text-transform:none;color:#ffffff;'}),
            'email': forms.EmailInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Email', 'style': 'text-transform:none;color:#ffffff;'}),
        }
        
    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        if Company.objects.filter(rut=rut).exists() or Profile.objects.filter(rut=rut).exists():
            raise ValidationError("The Rut you want to use already exists, try another please.")
        return rut    
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Company.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
            raise ValidationError("The Email you want to use already exists, try another please.")
        return email
    
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.initial['country'] = 'N/A'

class CompanyUpdateForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['address', 'number', 'office', 'country', 'postalCode', 'phone', 'logoLink']
        widgets = {
            'address': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Address', 'style': 'text-transform:none;color:#ffffff;'}),
            'number': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Number', 'style': 'text-transform:none;color:#ffffff;'}),
            'office': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Office', 'style': 'text-transform:none;color:#ffffff;'}),
            'country': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
            'postalCode': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Postal Code', 'style': 'text-transform:none;color:#ffffff;'}),
            'phone': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Phone', 'style': 'text-transform:none;color:#ffffff;'}),
            'logoLink': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
        }

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['alias', 'serialCode', 'description', 'imeiRecord', 'componentType', 'connectionType', 'supplyType', 'latitude', 'longitude', 'isEnabled']
        widgets = {
            'alias': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Alias del Dispositivo', 'style': 'text-transform:none'}),
            'serialCode': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de Serie del Dispositivo', 'style': 'text-transform:none'}),
            'description': forms.Textarea(attrs={'class':'form-control mt-3', 'placeholder':'Número de Serie del Dispositivo', 'style': 'text-transform:none'}),
            'imeiRecord': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de Serie del Dispositivo', 'style': 'text-transform:none'}),
            'componentType': forms.Select(attrs={'class':'form-control mt-3', 'placeholder':'Número de Serie del Dispositivo', 'style': 'text-transform:none'}),
            'connectionType': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de Serie del Dispositivo', 'style': 'text-transform:none'}),
            'supplyType': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de Serie del Dispositivo', 'style': 'text-transform:none'}),
            'latitude': forms.NumberInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de Serie del Dispositivo', 'style': 'text-transform:none'}),
            'longitude': forms.NumberInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de Serie del Dispositivo', 'style': 'text-transform:none'}),
            'isEnabled': forms.CheckboxInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de Serie del Dispositivo', 'style': 'text-transform:none'}),
        }
