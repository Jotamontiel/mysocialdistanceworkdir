from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Name", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Write your name', 'style':'text-transform:none'}
    ), min_length=3, max_length=100)
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
        attrs={'class':'form-control', 'placeholder':'Write your email, e.g. XXXXXX@gmail.com', 'style':'text-transform:none'}
    ), min_length=3, max_length=100)
    phone = forms.CharField(label="Cellphone", required=False, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Write your cellphone, e.g. 09 XXXX XXXX', 'style':'text-transform:none'}
    ), min_length=3, max_length=1000)
    content = forms.CharField(label="Content", required=True, widget=forms.Textarea(
        attrs={'class':'form-control', 'rows':7, 'placeholder':'Write your message', 'style':'text-transform:none'}
    ), min_length=3, max_length=1000)
