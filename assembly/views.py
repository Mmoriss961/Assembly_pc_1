import datetime
import os
from io import BytesIO, StringIO
from tempfile import template

from django.core import validators
from django.core.exceptions import ValidationError
from django.views.generic import DetailView, ListView
from django.db.models import Min,Max
import datetime
from Assembly_pc import settings
from Assembly_pc.settings import DEFAULT_FROM_EMAIL
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
from time import gmtime, strftime

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


import csv





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
    return render(request,'assembly/build_pc.html', {'test_view':test,'title':'Сборка ПК','id_test':test[0].id_test})

def result(request):
    if request.method=='POST':
        form=request.POST.getlist('test')
        dicts={"proc":[],"video":[],"ddr":[]}
        x=int(form[len(form)-1][0]) #переменная для поиска накопителя( 1 - находим hdd, 0 не находим)
        # print(x)
        for i in form:
            k=i.split()
            dicts["proc"].append(int(k[0]))
            dicts["video"].append(int(k[1]))
            dicts["ddr"].append(int(k[2]))
        proc = max(dicts["proc"])
        video = max(dicts["video"])
        ddr = max(dicts["ddr"])
        id_test= request.POST.get('id_test')
        # print(id_test)
        # print(form)
        # print(proc,video,ddr)

        queryset = Processor.objects.filter(Q(proc_benchmark__gte=proc) & Q(proc_max_syze_ddr__gte=ddr))
        take_price_proc = queryset.aggregate(Min('price_rub'))
        take_proc = queryset.filter(price_rub=take_price_proc['price_rub__min']).first()
        # print(take_proc)

        queryset = Motherboard.objects.filter(mboard_socket=take_proc.id_socket)
        take_price_mboard = queryset.aggregate(Min('price_rub'))
        take_mboard = queryset.filter(price_rub=take_price_mboard['price_rub__min']).first()
        # print(take_mboard)

        queryset = Cooler.objects.filter(Q(cooler_max_tdp__gte=take_proc.tdp) & Q(cooler_socket=take_proc.id_socket))
        queryset1= Cooler.objects.all()
        take_price_cooler = queryset.aggregate(Min('price_rub'))
        take_cooler = queryset.filter(price_rub=take_price_cooler['price_rub__min']).first()
        # print(take_cooler)
        print(queryset1)

        # flag = 0
        queryset = Ddr.objects.filter(Q(ddr_size=ddr/2) & Q(ddr_size__lte=take_proc.proc_max_syze_ddr) & Q(ddr_type=take_proc.id_type_mem_ddr))
        if not(queryset) :
            queryset = Ddr.objects.filter(Q(ddr_size=ddr) & Q(ddr_size__lte=take_proc.proc_max_syze_ddr) & Q(ddr_type=take_proc.id_type_mem_ddr))
            # flag = 1
        take_price_ddr = queryset.aggregate(Min('price_rub'))
        take_ddr = queryset.filter(price_rub=take_price_ddr['price_rub__min']).first()
        # print(take_ddr)

        queryset = Videocard.objects.filter( Q(video_benchmark__gte=video ))
        take_price_video = queryset.aggregate(Min('price_rub'))
        take_video = queryset.filter(price_rub=take_price_video['price_rub__min']).first()
        # print(take_video)

        if take_mboard.mboard_m2 :
            queryset = Storage.objects.filter( Q(id_storage_type=2) & Q(storage_volume__gte=120) & Q(id_form_factor=2))
            # print(queryset)
        else:
            queryset = Storage.objects.filter(Q(id_storage_type=2) & Q(id_form_factor=1) & Q(storage_volume__gte=120))
        take_price_storage = queryset.aggregate(Min('price_rub'))
        take_storage1 = queryset.filter(price_rub=take_price_storage['price_rub__min'])
        take_storage = queryset.filter(price_rub=take_price_storage['price_rub__min']).first()

        # print(take_storage)

        take_price_storage_hdd = 0
        take_storage_hdd = Storage.objects.none()
        take_storage_hdd1 = Storage.objects.none()
        if x == 1:
            queryset = Storage.objects.filter( Q(id_storage_type=1 )& Q(storage_volume__gte=500))
            take_price_storage_hdd = queryset.aggregate(Min('price_rub'))
            take_storage_hdd1 = queryset.filter(price_rub=take_price_storage_hdd['price_rub__min'])
            take_storage_hdd = queryset.filter(price_rub=take_price_storage_hdd['price_rub__min']).first()
            # print(take_storage_hdd)
            # print(take_storage_hdd1)
        # print(take_price_storage_hdd)


        if take_storage:
            if take_storage.id_form_factor == 1:
                queryset = CasePc.objects.filter(Q(max_height_cooler__gte=take_cooler.cooler_height )
                                                 & Q(max_length_video__gte =take_video.video_length)
                                                 & Q(id_mboard_size = take_mboard.id_mboard_size)
                                                 & Q(form_factor_3_5_gte=0))
            else:
                queryset = CasePc.objects.filter( Q(max_height_cooler__gte=take_cooler.cooler_height )
                                                  & Q(max_length_video__gte =take_video.video_length)
                                                  & Q(id_mboard_size = take_mboard.id_mboard_size))
        else:
            queryset = CasePc.objects.filter(Q(max_height_cooler__gte=take_cooler.cooler_height)
                                             & Q(max_length_video__gte=take_video.video_length)
                                             & Q(id_mboard_size=take_mboard.id_mboard_size))

        take_price_case = queryset.aggregate(Min('price_rub'))
        take_case = queryset.filter(price_rub=take_price_case['price_rub__min']).first()
        # print(take_case)

        if take_video.video_pci_e:
            queryset = PowerSupply.objects.filter(Q(power_supply_power__gte=take_video.power_supply_unit)
                                                  & Q(power_supply_pci_e__gte=take_video.video_pci_e))
        else:
            queryset = PowerSupply.objects.filter(Q(power_supply_power__gte=take_video.power_supply_unit))
        take_price_pow_sup = queryset.aggregate(Min('price_rub'))
        take_pow_sup = queryset.filter(price_rub=take_price_pow_sup['price_rub__min']).first()
        # print(take_pow_sup)
        # if flag == 0:
        #     take_price_ddr['price_rub__min'] = take_price_ddr['price_rub__min']*2
        #     print(take_price_ddr['price_rub__min'])
        if x == 0:
            price_end = take_price_pow_sup['price_rub__min'] + take_price_case['price_rub__min'] +take_price_cooler['price_rub__min']+ \
                        take_price_mboard['price_rub__min'] +take_price_video['price_rub__min']+ \
                        take_price_storage['price_rub__min']+take_price_storage_hdd+take_price_ddr['price_rub__min']+take_price_proc['price_rub__min']
        else:
            price_end = take_price_pow_sup['price_rub__min'] + take_price_case['price_rub__min'] +take_price_cooler['price_rub__min']+ \
                        take_price_mboard['price_rub__min'] +take_price_video['price_rub__min']+ \
                        take_price_storage['price_rub__min']+take_price_storage_hdd['price_rub__min']+take_price_ddr['price_rub__min']+take_price_proc['price_rub__min']
        # print(price_end)

        current_user= AuthUser.objects.get(pk=request.user.id)
        # print(request.user.id)
        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        # print(take_storage_hdd1)
        if len(take_storage_hdd1)>0:
            take_storage_end = take_storage_hdd1|take_storage1
        else:
            take_storage_end =take_storage1
        instance = PcAssembly.objects.create(id_case=take_case, id_cooler=take_cooler,id_motherboard=take_mboard,
                                             id_power_supply=take_pow_sup,id_proc=take_proc, id_vga=take_video,id_ddr=take_ddr,
                                             id_user =current_user, pc_assembly_date=showtime,pc_assembly_price_end=price_end)
        instance.id_storage.set(take_storage_end)
        instance = instance.save()
        pc_assembly = PcAssembly.objects.get(pc_assembly_date=showtime)

        # print(take_storage_end)

        context = {}
        if x == 1:
            context = {
                'title': 'Результат',
                'take_proc': take_proc,
                'take_mboard': take_mboard,
                'take_cooler': take_cooler,
                'take_ddr': take_ddr,
                'take_video': take_video,
                'take_storage': take_storage,
                'take_storage_hdd': take_storage_hdd,
                'take_case': take_case,
                'take_pow_sup': take_pow_sup,
                'x': x,
                'price_end': price_end,
                'showtime':showtime,
                'id_test':id_test,
                'pc_assembly':pc_assembly.pk,

            }
        else:
            context = {
                'title': 'Результат',
                'take_proc': take_proc,
                'take_mboard': take_mboard,
                'take_cooler': take_cooler,
                'take_ddr': take_ddr,
                'take_video': take_video,
                'take_storage': take_storage,
                'take_case': take_case,
                'take_pow_sup': take_pow_sup,
                'x': x,
                'price_end': price_end,
                'showtime':showtime,
                'id_test':id_test,
                'pc_assembly': pc_assembly.pk,

            }
        return render(request, 'assembly/result.html', context)

def save_result(request):
    if request.method == 'POST':
        form = request.POST
        take_proc = form.get('take_proc')
        take_video = form.get('take_video')
        take_mboard = form.get('take_mboard')
        take_cooler = form.get('take_cooler')
        take_ddr = form.get('take_ddr')
        take_pow_sup = form.get('take_pow_sup')
        take_time=form.get('take_time')
        id_test=int(form.get('id_test'))
        pc_assembly=int(form.get('pc_assembly'))
        # print(pc_assembly)

        x=form.get('x')
        if x == '1':
            take_storage_hdd = form.get('take_storage_hdd')
            # print(take_storage_hdd)
        else:
            take_storage_hdd = "Отсутствует"
        take_storage = form.get('take_storage')
        take_case = form.get('take_case')
        price_end = form.get('price_end')

        current_user= AuthUser.objects.get(pk=request.user.id)
        pc_assembly=PcAssembly.objects.get(pk=pc_assembly)
        id_test=Test.objects.get(pk=id_test)

        # print(take_proc,take_video,take_mboard,take_cooler,take_ddr,take_pow_sup,
        #       take_storage_hdd,take_storage,take_case,price_end,take_time, current_user)

        instance = Result.objects.create(result_date=take_time, result_title=take_proc+" "+take_video,power_supply=take_pow_sup,
                                         storage="HDD:"+take_storage_hdd+"; SSD:"+take_storage,mboard=take_mboard, proc=take_proc,id_pc_assembly=pc_assembly,
                                         video =take_video, ddr=take_ddr,cooler=take_cooler, case=take_case, result_price_end = price_end ,id_test = id_test,user=current_user )

        instance = instance.save()
    return redirect('result_list')


def my_acc(request):
    return render(request, 'assembly/my_account.html')






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

class all_pc_assembly(ListView):
    model=PcAssembly
    template_name = "assembly/all_pc_assembly.html"
    context_object_name = "all_pc_assembly"
    paginate_by = 12

    def get_queryset(self):
        queryset = PcAssembly.objects.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(all_pc_assembly, self).get_context_data(*args, **kwargs)
        get_count = PcAssembly.objects.count()
        context['get_count'] = get_count
        return context

class detail_pc_assembly(DetailView):
    model = PcAssembly
    template_name = "assembly/detail_pc_assembly.html"
    context_object_name = "detail_pc_assembly"
    pk_url_kwarg = "id_pc_assembly"

    def get_object(self, queryset=None):
        pk=self.kwargs.get(self.pk_url_kwarg)
        # print(pk)
        queryset = PcAssembly.objects.get(pk=pk)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(detail_pc_assembly, self).get_context_data( *args, **kwargs)
        get_q = self.get_object().id_pc_assembly
        # print(get_q)
        pc_assembly = PcAssembly.objects.get(id_pc_assembly=get_q)
        context['pc_assembly'] = pc_assembly
        # context['pc_assembly']=pc_assembly_img
        # print(pc_assembly_img.id_proc.proc_img)
        return context

    # def characteristic_video(self, id_pc_assembly):
    #     detail_pc_assembly = PcAssembly.objects.get(pk=id_pc_assembly)
    #     return render(self, 'assembly/detail_pc_assembly.html',
    #                   {"detail_pc_assembly": characteristic_video, "title": "Характиристики видеокарты"})
    # def get_queryset(self):
    #     queryset = PcAssembly.objects.filter(id_pc_assembly=self.request)
    #     print(queryset)
    #     return queryset
    #
    # def get_context_data(self, *args, **kwargs):
    #     context = super(detail_pc_assembly, self).get_context_data(*args, **kwargs)
    #     get_q1 = self.get_object().id_pc_assembly.id_pc_assembly
    #     print(get_q1)
    #     pc_assembly = PcAssembly.objects.get(id_pc_assembly=get_q1)
    #     context['pc_assembly'] = pc_assembly
    #     # context['pc_assembly']=pc_assembly_img
    #     # print(pc_assembly_img.id_proc.proc_img)
    #     return context
# class report_admin_assembly(ListView):
#     model = PcAssembly
#     template_name = "assembly/report_admin_assembly.html"
#     context_object_name = "report_admin_assembly"
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # d_min = datetime.date(2001,7,28)
#         # d_max = datetime.date(2021,15,6)
#         date_min = PcAssembly.objects.filter(pc_assembly_date__lte=datetime.now())
#         date_max = PcAssembly.objects.filter(pc_assembly_date__gte=datetime.now())
#         # date_test = PcAssembly.objects.filter(pc_assembly_date__contains=datetime.now())
#         # print(date_max)
#         # print(date_min)
#         # date_end = PcAssembly.objects.filter(pc_assembly_date__lte=d_min)
#         context['date_min'] = date_min
#         context['date_max'] = date_max
#         # context['date_end'] = date_end
#
#
#         return context

class filter_report_admin_assembly(all_pc_assembly,ListView):

    template_name = "assembly/report_admin_assembly.html"

    def get_queryset(self):
        date_min = self.request.GET.get('date_min')
        date_max = self.request.GET.get('date_max')
        queryset = PcAssembly.objects.filter(Q(pc_assembly_date__gte=date_min) & Q(pc_assembly_date__lte=date_max))

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(filter_report_admin_assembly, self).get_context_data(*args, **kwargs)
        queryset = self.get_queryset()
        context['get_count'] = queryset.count()
        return context
#
def report_admin_assembly(request):
    return render(request,'assembly/report_admin_assembly.html')




def report_admin_fb(request):
    return  render(request,'assembly/report_admin_fb.html')

class filter_report_admin_fb(ListView):
    model = Feedback
    template_name = "assembly/report_admin_fb.html"
    context_object_name = "filter_report_admin_fb"

    def get_queryset(self):
        date_min = self.request.GET.get('date_min')
        date_max = self.request.GET.get('date_max')
        queryset = Feedback.objects.filter(Q(fb_date__gte=date_min) & Q(fb_date__lte=date_max))
        print(queryset)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(filter_report_admin_fb, self).get_context_data(*args, **kwargs)
        get_count = Feedback.objects.count()
        context['get_count'] = get_count
        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     dis_video_mem = Videocard.objects.values('video_memory').distinct().order_by('video_memory')
    #     dis_video_manuf = Videocard.objects.values('id_manuf__name').distinct().order_by('id_manuf__name')
    #     minPrice = Videocard.objects.aggregate(Min('price_rub'))
    #     maxPrice = Videocard.objects.aggregate(Max('price_rub'))
    #     context['title'] = 'Видеокарты'
    #     context['dis_video_mem'] = dis_video_mem
    #     context['dis_video_manuf'] = dis_video_manuf
    #     context['minPrice'] = minPrice
    #     context['maxPrice'] = maxPrice
    #
    #     return context


class result_list(ListView):
    model=Result
    template_name = "assembly/my_account.html"
    context_object_name = "result_list"
    paginate_by = 12

    def get_queryset(self, queryset=None):
        queryset = Result.objects.filter(user_id=self.request.user.id).order_by('result_date')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(result_list, self).get_context_data(*args, **kwargs)
        get_count = Result.objects.filter(user_id=self.request.user.id).count()
        context['get_count'] = get_count
        return context

class detail_result(DetailView):
    model = Result
    template_name = "assembly/detail_result.html"
    context_object_name = "detail_result"
    pk_url_kwarg = "id_result"

    def get_object(self, queryset=None):
        pk=self.kwargs.get(self.pk_url_kwarg)
        queryset = Result.objects.prefetch_related('id_pc_assembly', 'id_test').get(pk=pk)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(detail_result, self).get_context_data(*args, **kwargs)
        get_q = self.get_object().id_pc_assembly.id_pc_assembly
        # print(get_q)
        pc_assembly = PcAssembly.objects.prefetch_related('id_proc','id_vga','id_ddr','id_cooler','id_case',
                                                          'id_storage','id_motherboard','id_power_supply').get(id_pc_assembly=get_q)
        context['pc_assembly'] = pc_assembly
        # context['pc_assembly']=pc_assembly_img
        # print(pc_assembly_img.id_proc.proc_img)
        return context







# def link_callback(uri, rel):
#     """
#     Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#     resources
#     """
#     result = finders.find(uri)
#     if result:
#         if not isinstance(result, (list, tuple)):
#             result = [result]
#         result = list(os.path.realpath(path) for path in result)
#         path=result[0]
#     else:
#         sUrl = settings.STATIC_URL        # Typically /static/
#         sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
#         mUrl = settings.MEDIA_URL         # Typically /media/
#         mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/
#
#         if uri.startswith(mUrl):
#             path = os.path.join(mRoot, uri.replace(mUrl, ""))
#         elif uri.startswith(sUrl):
#             path = os.path.join(sRoot, uri.replace(sUrl, ""))
#         else:
#             return uri
#
#     # make sure that file exists
#     if not os.path.isfile(path):
#         raise Exception(
#             'media URI must start with %s or %s' % (sUrl, mUrl)
#         )
#     return path
#
#
# def render_pdf_view(request):
#     result_test = Result.objects.all()
#
#     template_path = 'assembly/pdf1.html'
#     context = {'result_test': result_test}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)
#
#     # create a pdf
#     pisa_status = pisa.CreatePDF(html.encode('utf-8'), dest=response, link_callback=link_callback)
#     # if error then show some funy view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response



class video_list(ListView):
    model = Videocard
    template_name = "assembly/video.html"
    context_object_name = "video"
    paginate_by = 12

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
    dis_video_manuf = request.GET.getlist('id_manuf__name')q
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

