from django.core import validators
from django.core.exceptions import ValidationError

from Assembly_pc.settings  import DEFAULT_FROM_EMAIL
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, FeedbackForm
from .models import *
from .models import PcAssembly
from .models import Videocard
from django.db.models import Max
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.core.validators import validate_email
from . import forms


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Вы успешно зарегистрировались')
            #return redirect('login')
        else:
            messages.error(request,'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, "assembly/register.html", {"form": form})





def user_login(request):
    if request.method == 'POST':
        form1 = UserLoginForm(data=request.POST)
        if form1.is_valid():
            user = form1.get_user()
            login(request,user)
            messages.success(request, 'Вы успешно вошли')
            #return redirect('home')
        else:
            messages.error(request,'Ошибка авторизации')
    else:
        form1 = UserLoginForm()
    return render(request,"assembly/register.html", {"form1": form1})

def user_logout(request):
    logout(request)
    return redirect('home')




class PcAssemblyView(View):

    def get (self, request):

        pc_assembly = PcAssembly.objects.aggregate(Max('pc_assembly_price_end'))
        return render(request, 'assembly/PC_Assembly_list.html', {"PC_Assembly": pc_assembly})
def index (request):
    pc_assembly = PcAssembly.objects.all()
    context={
        'title':'Главная страница',
        'pc_ass':pc_assembly,
    }
    return render(request,  'assembly/index.html', context=context)

def video (request):
    videocard = Videocard.objects.all()
    context={
        'title': 'Видеокарты',
        'video':videocard,
    }
    return render(request,  'assembly/video.html', context=context)

def proc (request):
    proc = Processor.objects.all()
    context={
        'title': 'Процессоры',
        'proc':proc,
    }
    return render(request,  'assembly/proc.html', context=context)

def test(request):
    videocard = Videocard.objects.all()
    context={
        'title':'Видеокарты',
        'video':videocard,
    }
    return render(request,  'assembly/test.html',context=context)

def characteristic_video (request, id_vga):
    characteristic_video = Videocard.objects.get(pk=id_vga)
    return render(request, 'assembly/characteristic_video.html', {"char_video":characteristic_video})

def characteristic_proc(request, id_proc):
    characteristic_proc = Processor.objects.get(pk=id_proc)
    return render(request, 'assembly/characteristic_proc.html', {"char_proc":characteristic_proc})





def feedback(request):
    if request.method == 'POST':
        form3 = FeedbackForm(request.POST)
        if form3.is_valid():
            form3.save()
            from_email = form3.cleaned_data['from_email']
            subject = form3.cleaned_data['subject']
            message = form3.cleaned_data['message']
            mail1 = send_mail(
                f'{subject} от {from_email}',
                message,
                DEFAULT_FROM_EMAIL,
                [DEFAULT_FROM_EMAIL],
                fail_silently=False,)
            if mail1 > 0:
                mail2 = send_mail('Отчет о доставке',f'Письмо успешно получено.Спасибо за обратную связь!', DEFAULT_FROM_EMAIL, [from_email] ,fail_silently=True)
                if mail2 > 0:
                    messages.success(request,'Письмо отправлено!')
                else:
                    messages.error(request,'Ошибка отправки письма, попробуйте позже.')
        else:
            messages.error(request,'Ошибка в заполнении формы.')
    else:
        form3 = forms.FeedbackForm()
    return render(request, "assembly/feedback.html/", {'form3': form3})

