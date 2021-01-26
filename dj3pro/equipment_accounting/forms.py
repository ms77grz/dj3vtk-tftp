from django import forms


class SearchSubscriber(forms.Form):
    account_number = forms.CharField(
        label='Введите номер лицевого счета',
        # widget=forms.TextInput(attrs={'placeholder': 'Без 11', 'autocomplete': 'off'}),
        widget=forms.TextInput(),
        min_length=8, max_length=12)
