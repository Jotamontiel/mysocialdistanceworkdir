from django import forms
from .models import Company, ComponentType, Component, SensorType, Sensor
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

class CompanyEmailUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Required, 254 characters maximum and must be valid.")

    class Meta:
        model = Company
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:
            if Company.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
                raise forms.ValidationError("The email is already registered, try another please.")
        return email

class ComponentTypeForm(forms.ModelForm):

    class Meta:
        model = ComponentType
        fields = ['name', 'initials', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Component Type Name, e.g. Fire-Measurement-Station', 'style': 'text-transform:none;color:#ffffff;'}),
            'initials': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Component Type Initials, e.g. FIMEST-01', 'style': 'text-transform:none;color:#ffffff;'}),
            'description': forms.Textarea(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Component Type Description', 'style': 'text-transform:none;color:#ffffff;'}),
        }

class ComponentForm(forms.ModelForm):

    class Meta:
        model = Component
        fields = ['alias', 'serialCode', 'description', 'imeiRecord', 'componentType', 'profile', 'connectionType', 'supplyType', 'latitude', 'longitude', 'isEnabled']
        widgets = {
            'alias': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Compt Alias, e.g. Measurement-Station-Paine', 'style': 'text-transform:none;color:#ffffff;'}),
            'serialCode': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Compt Serial Code, e.g. 77cf159c-e088-4b3a-ad4d-a40cbc640fc0', 'style': 'text-transform:none;color:#ffffff;'}),
            'description': forms.Textarea(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Compt Description', 'style': 'text-transform:none;color:#ffffff;'}),
            'imeiRecord': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Compt IMEI Record', 'style': 'text-transform:none;color:#ffffff;'}),
            'componentType': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
            'profile': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
            'connectionType': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#ffffff;background: black;'}),
            'supplyType': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#ffffff;background: black;'}),
            'latitude': forms.NumberInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Compt Latitude, e.g. -35.675147', 'style': 'text-transform:none;color:#ffffff;'}),
            'longitude': forms.NumberInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Compt Longitude, e.g. -71.542969', 'style': 'text-transform:none;color:#ffffff;'}),
            'isEnabled': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
        }
    
    def clean_alias(self):
        alias = self.cleaned_data.get("alias")
        if Component.objects.filter(alias=alias).exists():
            raise ValidationError("The Alias you want to use already exists, try another please.")
        return alias
    
    def clean_serialCode(self):
        serialCode = self.cleaned_data.get("serialCode")
        if Component.objects.filter(serialCode=serialCode).exists() or Sensor.objects.filter(serialCode=serialCode).exists():
            raise ValidationError("The Serial Code you want to use already exists, try another please.")
        return serialCode

class ComponentUpdateForm(forms.ModelForm):

    class Meta:
        model = Component
        fields = ['description', 'imeiRecord', 'componentType', 'connectionType', 'supplyType', 'latitude', 'longitude', 'isEnabled']
        widgets = {
            'description': forms.Textarea(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Compt Description', 'style': 'text-transform:none;color:#ffffff;'}),
            'imeiRecord': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Compt IMEI Record', 'style': 'text-transform:none;color:#ffffff;'}),
            'componentType': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
            'connectionType': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#ffffff;background: black;'}),
            'supplyType': forms.Select(attrs={'class':'form-control mt-3 form-control-warning', 'style': 'color:#ffffff;background: black;'}),
            'latitude': forms.NumberInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Compt Latitude, e.g. -35.675147', 'style': 'text-transform:none;color:#ffffff;'}),
            'longitude': forms.NumberInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Compt Longitude, e.g. -71.542969', 'style': 'text-transform:none;color:#ffffff;'}),
            'isEnabled': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
        }

class SensorTypeForm(forms.ModelForm):

    class Meta:
        model = SensorType
        fields = ['name', 'initials', 'description', 'measurementUnit', 'isGraphical']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Sensor Type Name, e.g. Humidity-Measurement', 'style': 'text-transform:none;color:#ffffff;'}),
            'initials': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Sensor Type Initials, e.g. HUME-01', 'style': 'text-transform:none;color:#ffffff;'}),
            'description': forms.Textarea(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Sensor Type Description', 'style': 'text-transform:none;color:#ffffff;'}),
            'measurementUnit': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Sensor Type Measurement Unit, e.g. PA, °C, V, etc.', 'style': 'text-transform:none;color:#ffffff;'}),
            'isGraphical': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
        }

class SensorForm(forms.ModelForm):

    class Meta:
        model = Sensor
        fields = ['alias', 'serialCode', 'measurementUnit', 'description', 'sensorType', 'component', 'brand', 'isEnabled']
        widgets = {
            'alias': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Sensor Alias, e.g. Temperature-BME680-Sensor', 'style': 'text-transform:none;color:#ffffff;'}),
            'serialCode': forms.TextInput(attrs={'class':'form-control mt-3 form-control-danger', 'placeholder':'Enter Sensor Serial Code, e.g. 69254b1c-a212-441f-954d-d270410fbf82', 'style': 'text-transform:none;color:#ffffff;'}),
            'measurementUnit': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Sensor Measurement, e.g. PA, °C, V, etc.', 'style': 'text-transform:none;color:#ffffff;'}),
            'description': forms.Textarea(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Sensor Description', 'style': 'text-transform:none;color:#ffffff;'}),
            'sensorType': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
            'component': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
            'brand': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Sensor Brand, e.g. Adafruit, SeeedStudio, etc.', 'style': 'text-transform:none;color:#ffffff;'}),
            'isEnabled': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
        }
    
    def clean_alias(self):
        alias = self.cleaned_data.get("alias")
        if Sensor.objects.filter(alias=alias).exists():
            raise ValidationError("The Alias you want to use already exists, try another please.")
        return alias
    
    def clean_serialCode(self):
        serialCode = self.cleaned_data.get("serialCode")
        if Sensor.objects.filter(serialCode=serialCode).exists() or Component.objects.filter(serialCode=serialCode).exists():
            raise ValidationError("The Serial Code you want to use already exists, try another please.")
        return serialCode

class SensorUpdateForm(forms.ModelForm):

    class Meta:
        model = Sensor
        fields = ['measurementUnit', 'description', 'sensorType', 'brand', 'isEnabled']
        widgets = {
            'measurementUnit': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Sensor Measurement, e.g. PA, °C, V, etc.', 'style': 'text-transform:none;color:#ffffff;'}),
            'description': forms.Textarea(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Sensor Description', 'style': 'text-transform:none;color:#ffffff;'}),
            'sensorType': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
            'brand': forms.TextInput(attrs={'class':'form-control mt-3 form-control-warning', 'placeholder':'Enter Sensor Brand, e.g. Adafruit, SeeedStudio, etc.', 'style': 'text-transform:none;color:#ffffff;'}),
            'isEnabled': forms.Select(attrs={'class':'form-control mt-3 form-control-danger', 'style': 'color:#ffffff;background: black;'}),
        }