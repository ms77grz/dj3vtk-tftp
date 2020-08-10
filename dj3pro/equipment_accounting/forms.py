from django import forms


class SearchSubscriber(forms.Form):
    account_number = forms.CharField(
        label='Введите номер лицевого счета',
        widget=forms.TextInput(attrs={'placeholder': 'Без 11'}),
        min_length=5, max_length=10)
