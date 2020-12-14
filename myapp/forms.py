from django import forms


class UserForm(forms.Form):
    date = forms.DateTimeField()

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()