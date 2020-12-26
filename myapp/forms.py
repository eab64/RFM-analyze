from django import forms


class UserForm(forms.Form):
    date = forms.DateTimeField()

class IncomeHigh(forms.Form):
    high = forms.IntegerField()

class IncomeLow(forms.Form):
    low = forms.IntegerField()

class Max_day(forms.Form):
    max_day = forms.IntegerField()

class Min_day(forms.Form):
    min_day = forms.IntegerField()

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()