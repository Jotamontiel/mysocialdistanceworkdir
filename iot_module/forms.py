from django import forms
from .models import Component

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
