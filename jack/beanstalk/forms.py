
from django import forms

class PutForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea())
    tube = forms.CharField(initial='default')
    priority = forms.IntegerField(initial=2147483648)
    delay = forms.IntegerField(initial=0)
    ttr = forms.IntegerField(initial=120)

