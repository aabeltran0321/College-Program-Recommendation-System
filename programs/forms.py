from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=2000)
    file = forms.FileField()