from django import forms

class ImageForm(forms.Form):
    text = forms.CharField(max_length=100)
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))