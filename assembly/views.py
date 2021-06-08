from django.core import validators
from django.core.exceptions import ValidationError
from django.views.generic import DetailView, ListView
from django.db.models import Min,Max

from Assembly_pc.settings  import DEFAULT_FROM_EMAIL
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, FeedbackForm
from .models import *
from django.db.models import Max, Q
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.core.validators import validate_email
from . import forms
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse



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

# class build_pc(ListView):
#     model= Test
#     template_name = 'assembly/build_pc.html'

    # def get_context_data(self,  **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     dis_test_title = Test.objects.values('test_title')
    #     dis_test_desc = Test.objects.values('test_desc')
    #     context['title'] = 'Подборк ПК'
    #     context['dis_test_title'] = dis_test_title
    #     context['dis_test_desc'] = dis_test_desc
    #     return context

# def build_pc_view(request, id_test):
#     test=Test.objects.get(pk=id_test)
#     return render(request,'assembly/build_pc.html',{'build_pc_v':test,'title':'Сборка ПК'})

# class question(ListView):
#     model = Question
#     template_name = 'assembly/build_pc.html'
#
#     def get_queryset(self):
#         question = Question.objects.prefetch_related('answer_set').get(pk=)


def test_view(request, id_test):
    test=Test.objects.filter(pk=id_test).prefetch_related('question_set','question_set__answer_set')
    return render(request,'assembly/build_pc.html', {'test_view':test,'title':'Сборка ПК'})
#
def result(request):
    if request.method=='POST':
        form=request.POST.getlist('test')
        dicts={}
        keys=len(form)
        print(keys)
        print(form)
        values = list(map(int,form.split()))
        # values_ = str(values.split(','))
        # result = [c for c in values[0]]
        print(values)


        # for (index, elem) in enumerate(values):
        #     values[index]=elem+"!"
        # print(values)
        # for i in keys:
        #     dicts[i]=values[i]
        # print(dicts)
        # d={}
        # for k in form.items():
        #     if k.startswith('test'):
        #      d = d(k)

        # dict={v for k, v in form.items()if k.startswith ('test')}
        # d=dict
        # print(d)




    return render(request,'assembly/result.html')


# def question_view(request, id_question):
#     question=Question.objects.prefetch_related('answer_set').get(pk=id_question)
#     print(question)
#     return  render(request,'assembly/build_pc.html',{'question_view':question,'title':'Сборка ПК'})

# def question_data_view(request, pk):
#     test= Test.objects.get(pk=pk)
#     question=[]
#     for q in Test.get_question():
#         answer =[]
#         for a in q


class video_list(ListView):
    model = Videocard
    template_name = "assembly/video.html"
    context_object_name = "video"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis_video_mem = Videocard.objects.values('video_memory').distinct().order_by('video_memory')
        dis_video_manuf = Videocard.objects.values('id_manuf__name').distinct().order_by('id_manuf__name')
        minPrice = Videocard.objects.aggregate(Min('price_rub'))
        maxPrice = Videocard.objects.aggregate(Max('price_rub'))
        context['title'] = 'Видеокарты'
        context['dis_video_mem'] = dis_video_mem
        context['dis_video_manuf'] = dis_video_manuf
        context['minPrice'] = minPrice
        context['maxPrice'] = maxPrice

        return context

class filter_video(video_list,ListView):

    def get_queryset(self):
        q=self.request.GET.get('q')
        video_memory = self.request.GET.getlist('video_memory')
        id_manuf__name =self.request.GET.getlist('id_manuf__name')
        minPrice = self.request.GET.get('minPrice')
        maxPrice = self.request.GET.get('maxPrice')
        queryset = Videocard.objects.all()
        s=""
        if len(q)>0:
            s = q.split(" ")
        if len(s) > 1:
            for i in range(len(s) - 1):
                queryset = queryset.filter((Q(id_manuf__name__icontains=s[i]) | Q(name__icontains=s[i])) &
                                           (Q(id_manuf__name__icontains=s[i + 1]) | Q(
                                               name__icontains=s[i + 1])))
        else:
            queryset = queryset.filter(Q(id_manuf__name__icontains=q) |
                                       Q(name__icontains=q))



        if len(video_memory)>0:
            queryset=queryset.filter(Q(video_memory__in=video_memory))

        if len(id_manuf__name)>0 :
            queryset = queryset.filter(Q(id_manuf__name__in=id_manuf__name))

        if len(minPrice) > 0:
            queryset = queryset.filter(Q(price_rub__gte=minPrice))

        if len(maxPrice) >0:
            queryset = queryset.filter(Q(price_rub__lte=maxPrice))
        return queryset


    def get_context_data(self, *args, **kwargs):
        context = super(filter_video, self).get_context_data(*args, **kwargs)
        context["video_memory"] = ''.join([f"video_memory={x}&" for x in self.request.GET.getlist("video_memory")])
        context["id_manuf__name"] = ''.join([f"id_manuf__name={x}&" for x in self.request.GET.getlist("id_manuf__name")])
        context["minPrice_"] = ''.join([f"minPrice={self.request.GET.get('minPrice')}&"])
        context["maxPrice_"] = ''.join([f"maxPrice={self.request.GET.get('maxPrice')}&"])
        context["q"] =''.join([f"q={self.request.GET.get('q')}&"])

        return context

'''
class Search(filter_video,ListView):


    def get_queryset(self):
        get_q=self.request.GET.get("q")

        return Videocard.objects.filter(
            Q(id_manuf__name__icontains=get_q) |
            Q(name__icontains=get_q))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
'''

'''
def video (request):
    videocard = Videocard.objects.all()
    dis_video_mem= Videocard.objects.values('video_memory').distinct().order_by('video_memory')
    dis_video_manuf = Videocard.objects.values('id_manuf__name').distinct().order_by('id_manuf__name')
    paginator = Paginator(videocard,12)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)
    context={
        'title': 'Видеокарты',
        'video':videocard,
        'page_obj':page_objects,
        'dis_video_mem': dis_video_mem,
        'dis_video_manuf': dis_video_manuf,

    }

    return render(request,  'assembly/video.html', context=context)
'''
'''
def  get_filters(request):
    dis_video_mem= Videocard.objects.values('video_memory').distinct().order_by('video_memory')
    dis_video_manuf = Videocard.objects.values('id_manuf__name').distinct().order_by('id_manuf__name')
    context={
        'dis_video_mem':dis_video_mem,
        'dis_video_manuf':dis_video_manuf,
    }
    return context
'''
'''
def filter_data(request):
    dis_video_mem =request.GET.getlist('video_memory')
    dis_video_manuf = request.GET.getlist('id_manuf__name')
    video =Videocard.objects.all()
    if len(dis_video_mem)>0:
        video=video.filter(video_memory__in = dis_video_mem).distinct()
    if len(dis_video_manuf)>0:
        video=video.filter(id_manuf__name__in = dis_video_manuf).distinct()
    t=render_to_string('assembly/video.html',{'data':video})
    return JsonResponse({'data':t})
'''
'''
def get_dis_vm(request):

    queryset = Videocard.objects.filter(
        Q(video_memory__in=request.GET.getlist('video_memory')) |
        Q(id_manuf__name__in = request.GET.getlist('id_manuf__name')))
    dis_video_mem= Videocard.objects.values('video_memory').distinct().order_by('video_memory')
    dis_video_manuf = Videocard.objects.values('id_manuf__name').distinct().order_by('id_manuf__name')
    paginator = Paginator(queryset,12)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)
    context={
        'video':queryset,
        'page_obj':page_objects,
        'dis_video_mem':dis_video_mem,
        'dis_video_manuf':dis_video_manuf,
    }
    return render(request,  'assembly/video.html', context=context)

'''
'''
class FilterDisVideo:

    def get_video_mem(self):
        return Videocard.objects.values('video_memory').distinct().order_by('video_memory')

    def get_video_manuf(self):
        return  Videocard.objects.values('id_manuf__name').distinct().order_by('id_manuf__name')

class FilterVideo(FilterDisVideo,DetailView):

    def get_queryset_dis(self):
        queryset = Videocard.objects.filter(
            video_memory__in = self.request.GET.getlist('video_memory')
       )
        return queryset
'''
def proc (request):
    proc = Processor.objects.all()
    paginator = Paginator(proc,12)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)
    context={
        'title': 'Процессоры',
        'proc':proc,
        'page_obj': page_objects,
    }
    return render(request,  'assembly/proc.html', context=context)

def case_pc (request):
    case_pc = CasePc.objects.all()
    paginator = Paginator(case_pc,12)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)
    context={
        'title': 'Кулера',
        'case_pc':case_pc,
        'page_obj': page_objects,
    }
    return render(request,  'assembly/case_pc.html', context=context)

def cooler (request):
    cooler = Cooler.objects.all()
    paginator = Paginator(cooler,12)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)
    context={
        'title': 'Кулера',
        'cooler':cooler,
        'page_obj': page_objects,
    }
    return render(request,  'assembly/cooler.html', context=context)

def ddr (request):
    ddr = Ddr.objects.all()
    paginator = Paginator(ddr,12)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)
    context={
        'title': 'Оперативная память',
        'ddr':ddr,
        'page_obj': page_objects,
    }
    return render(request,  'assembly/ddr.html', context=context)

def mboard (request):
    mboard = Motherboard.objects.all()
    paginator = Paginator(mboard,12)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)
    context={
        'title': 'Мат. платы',
        'mboard':mboard,
        'page_obj': page_objects,
    }
    return render(request,  'assembly/mboard.html', context=context)

def power_supply (request):
    power_supply = PowerSupply.objects.all()
    paginator = Paginator(power_supply,12)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)
    context={
        'title': 'Блоки питания',
        'power_supply':power_supply,
        'page_obj': page_objects,
    }
    return render(request,  'assembly/power_supply.html', context=context)

def storage (request):
    storage = Storage.objects.all()
    paginator = Paginator(storage,12)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)
    context={
        'title': 'Накопители',
        'storage':storage,
        'page_obj': page_objects,
    }
    return render(request,  'assembly/storage.html', context=context)


# def test(request):
#     test = Test.objects.all()
#     context={
#         'title':'Тесты',
#         'test':test,
#     }
#     return render(request,  'assembly/test.html',context=context)


def characteristic_video (request, id_vga):
    characteristic_video = Videocard.objects.get(pk=id_vga)
    return render(request, 'assembly/characteristic_video.html', {"char_video":characteristic_video, "title":"Характиристики видеокарты"})

def characteristic_proc(request, id_proc):
    characteristic_proc = Processor.objects.get(pk=id_proc)
    return render(request, 'assembly/characteristic_proc.html', {"char_proc":characteristic_proc, "title":"Характиристики процессора"})

def characteristic_case_pc (request, id_case):
    characteristic_case_pc = CasePc.objects.get(pk=id_case)
    return render(request, 'assembly/characteristic_case_pc.html', {"char_case":characteristic_case_pc, "title":"Характиристики корпуса"})

def characteristic_cooler (request, id_cooler):
    characteristic_cooler = Cooler.objects.get(pk=id_cooler)
    return render(request, 'assembly/characteristic_cooler.html', {"char_cooler":characteristic_cooler, "title":"Характиристики куллера"})

def characteristic_ddr (request, id_ddr):
    characteristic_ddr = Ddr.objects.get(pk=id_ddr)
    return render(request, 'assembly/characteristic_ddr.html', {"char_ddr":characteristic_ddr, "title":"Характиристики памяти"})

def characteristic_mboard(request, id_mboard):
    characteristic_mboard = Motherboard.objects.get(pk=id_mboard)
    return render(request, 'assembly/characteristic_mboard.html', {"char_mboard":characteristic_mboard, "title":"Характиристики мат. платы"})

def characteristic_power_supply (request, id_power_supply):
    characteristic_power_supply = PowerSupply.objects.get(pk=id_power_supply)
    return render(request, 'assembly/characteristic_power_supply.html', {"char_power_supply":characteristic_power_supply, "title":"Характиристики блока питания"})

def characteristic_storage (request,  id_storage):
    characteristic_storage = Storage.objects.get(pk=id_storage)
    return render(request, 'assembly/characteristic_storage.html', {"char_storage":characteristic_storage, "title":"Характиристики накопителя"})

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
                fail_silently=True,)
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

