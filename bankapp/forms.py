from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from bankapp.models import CustomUser, MoneyOrder

def IsNormalName(username):
    for i in range(len(username)):
        if not(username[i].lower() in 'йцукенгшщзхъфывапролджэячсмитьбюqwertyuiopasdfghjklzxcvbnm'):
            return False
    return True

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'course']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email):
            raise forms.ValidationError('Такой email уже кем-то используется')
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) <= 3 or len(username) >= 20:
            raise forms.ValidationError('Длина логина не может быть меньше 4-ёх или больше 19-ти символов.')
        return username
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not(IsNormalName(first_name)):
            raise forms.ValidationError('Имя может содержать только символы латиницы или кириллицы.')
        return first_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not(IsNormalName(last_name)):
            raise forms.ValidationError('Имя может содержать только символы латиницы или кириллицы.')
        return last_name
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if (password1 and password2):
            if (password1 != password2):
                raise forms.ValidationError('Введённые пароли не совпадают')
            else:
                return password2
        else:
            raise forms.ValidationError('Пароль отсутствует')
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs.update({"placeholder": 'Придумайте логин'})
            self.fields['email'].widget.attrs.update({"placeholder": 'Введите свой email'})
            self.fields['first_name'].widget.attrs.update({"placeholder": 'Ваше имя'})
            self.fields['last_name'].widget.attrs.update({"placeholder": 'Ваша фамилия'})
            self.fields['password1'].widget.attrs.update({"placeholder": 'Придумайте пароль'})
            self.fields['password2'].widget.attrs.update({"placeholder": 'Повторите пароль'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.fields['email'].help_text = None

class CustomUserChangeForm(forms.Form):
    first_name = forms.CharField(label='Новое имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Новая фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    courses = {
        (1, '1 курс (бакалавр)'),
        (2, '2 курс (бакалавр)'),
        (3, '3 курс (бакалавр)'),
        (4, '4 курс (бакалавр)'),
        (5, '1 курс (магистр)'),
        (6, '2 курс (магистр)'),
    }
    course = forms.ChoiceField(choices=courses, label='Новый курс')
    password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    last_password = forms.CharField(label='Введите старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not(IsNormalName(first_name)):
            raise forms.ValidationError('Имя может содержать только символы латиницы или кириллицы.')
        return first_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not(IsNormalName(last_name)):
            raise forms.ValidationError('Имя может содержать только символы латиницы или кириллицы.')
        return last_name
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if (len(password) < 8):
            raise forms.ValidationError('Длина пароля должна быть не менее 8 символов')
        return password
    
class CustomUserLoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def clean_username(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data['username']
        if username is None:
            # raise forms.ValidationError('Отсутствует логин')
            self.add_error('username', 'Отсутствует логин')
        return username
    def clean_password(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data['password']
        if password is None:
            raise forms.ValidationError('Отсутствует логин')
        return password

class MoneyOrderForm(forms.Form):
    sender_number = forms.HiddenInput()
    recipient_number = forms.IntegerField(label="Получатель", widget=forms.NumberInput(attrs={'class': 'form-input'}))
    money_sum = forms.IntegerField(label="Сумма перевода", widget=forms.NumberInput(attrs={'class': 'form-input'}))
    def clean_recipient_number(self):
        cd = self.cleaned_data
        recipient_number = cd['recipient_number']
        if CustomUser.objects.filter(account_number = recipient_number).count() == 0:
            raise forms.ValidationError('Не найден пользователь с данным номером счёта')
        return recipient_number
    # def clean_money_sum(self):
    #     cd = self.cleaned_data
    #     money_sum = cd['money_sum']
    #     sender_number = cd['sender_number']
    #     if money_sum < MoneyOrder.objects.get(sender_number = sender_number).money_sum:
    #         raise forms.ValidationError('На вашем счёте недостаточно средств')
    #     return money_sum
    