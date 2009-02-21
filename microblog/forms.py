from django import forms

class PostEntryForm(forms.Form):
    content = forms.CharField(max_length=250)

