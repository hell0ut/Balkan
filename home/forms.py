from django import forms


class BookForm(forms.Form):
    name=forms.CharField(label='Ваше имя', max_length=100)
    number =forms.CharField(label='Ваш номер', max_length=100)
    date=forms.CharField(label='Дата', max_length=100)
    time= forms.CharField(label='Время', max_length=100)
    quantity=forms.IntegerField(label='Количество человек')
    message =forms.CharField(label='Сообщение', max_length=300)
