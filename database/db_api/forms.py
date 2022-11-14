from django import forms


class NameForm(forms.Form):
    db_name = forms.CharField(label='DB name', max_length=100)
