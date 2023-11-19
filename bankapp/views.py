from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView
from bankapp.models import CustomUser, MoneyOrder
import random
from bankapp.forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserChangeForm, MoneyOrderForm
# Create your views here.

def mainpage(request):
    return render(request, 'homepage.html', {'text': "Писька"})

        
def SignUp(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account_number = random.randint(100000, 1000000 - 1)
            while CustomUser.objects.filter(account_number = account_number).count() != 0:
                account_number = random.randint(100000, 1000000 - 1)
            form.save()
            temp = CustomUser.objects.get(username = username)
            temp.account_number = account_number
            temp.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('homepage')
    else:
        form = CustomUserCreationForm
    return render(request, 'signup.html', {'form': form})


def LoginUser(request):
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # print(cd)
            user = authenticate(request, username=cd['username'], password=cd['password'])
            print(user)
            if user:
                login(request, user)
                return redirect('homepage')
            else:
                form.add_error(None, 'Неверно введён логин или пароль')
    else:
        form = CustomUserCreationForm()
    return render(request, 'login.html', {'form': form})

def LogOut(request):
    logout(request)
    return redirect('homepage')

def PersonalPage(request):
    if request.user.is_authenticated:
        sender = request.user.account_number
        return render(request, 'personalpage.html', {'money_orders': MoneyOrder.objects.filter(recipient_number = sender) | MoneyOrder.objects.filter(sender_number = sender)})
    return redirect('homepage')

def UserChangePage(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_first_name = cd['first_name']
            new_last_name = cd['last_name']
            new_password = cd['password']
            last_password = cd['last_password']
            if authenticate(username = request.user.username, password = last_password) == request.user:
                user = CustomUser.objects.get(username = request.user.username)
                user.first_name = new_first_name
                user.last_name = new_last_name
                user.set_password(new_password)
                user.save()
                print("Ввели новые данные")
                login(request, user)
                return redirect('homepage')
            else:
                form.add_error(None, 'Введён неверный пароль')
    else:
        form = CustomUserChangeForm()
    return render(request, 'userchangepage.html', {'form': form})


def SendMoneyPage(request):
    if request.user.is_authenticated:
        sender = request.user.account_number
        if request.method == "POST":
            form = MoneyOrderForm(request.POST)
            # print(request.POST)
            # print(form)
            form.sender_number = sender
            if form.is_valid():
                cd = form.cleaned_data
                print(cd)
                recipient = cd['recipient_number']
                money_sum = cd['money_sum']
                if CustomUser.objects.get(account_number = sender).money < money_sum:
                    form.add_error('money_sum', 'На вашем счёте недостаточно средств.')
                    return render(request, 'sendmoneypage.html', {'form': form})
                temp = MoneyOrder.objects.create(
                    sender_number = sender,
                    recipient_number = recipient,
                    money_sum = money_sum
                )
                temp.save()
                recipient_user = CustomUser.objects.get(account_number = recipient)
                recipient_user.money += money_sum
                recipient_user.save()
                sender_user = CustomUser.objects.get(account_number = request.user.account_number)
                sender_user.money -= money_sum
                sender_user.save()
                # return render(request, 'personalpage.html', {'money_orders': MoneyOrder.objects.filter(recipient_number = sender) | MoneyOrder.objects.filter(sender_number = sender)})
                # return redirect('personal', {'money_orders': MoneyOrder.objects.filter(recipient_number = sender) | MoneyOrder.objects.filter(sender_number = sender)})
                return redirect('personal')
        else:
            form = MoneyOrderForm()
        return render(request, 'sendmoneypage.html', {'form': form})
    return redirect('homepage')