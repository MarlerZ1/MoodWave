from django import forms


class UserSearchForm(forms.Form):
    search_field = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-start',
        'placeholder': 'Поиск пользователя...'
    }))