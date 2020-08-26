from django import forms


class GetOntForm(forms.Form):
    ont = forms.CharField(max_length=20)
