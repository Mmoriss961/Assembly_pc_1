from django.urls import path

from.views import *
from.import views


urlpatterns = [
    path('PC_Assembly_list/', views.PcAssemblyView.as_view()),
    path('', index, name='home'),
    path('videocards/', video_list.as_view(), name='video'),
    path('processors/', proc, name='proc'),
    path('case_pc/', case_pc, name='case'),
    path('cooler/', cooler, name='cooler'),
    path('ddr/', ddr, name='ddr'),
    path('mboard/', mboard, name='mboard'),
    path('power_supply /', power_supply , name='power_supply '),
    path('storage/', storage, name='storage'),
    # path('test/', test, name='test'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('feedback/', feedback, name ='feedback'),

    # path('build_pc/',build_pc.as_view(),name='build_pc'),
    # path('build_pc/<int:id_test>',build_pc_view, name='build_pc_view'),
    #
    # path('build_pc/', question.as_view(), name='build_pc'),
    path('pc_assembly/<int:id_test>', test_view, name='test_view'),

    path('result/',result,name='result'),


    path('videocards/<int:id_vga>/', characteristic_video, name='characteristic_video'),
    path('processors/<int:id_proc> /', characteristic_proc, name='characteristic_proc'),
    path('case_pc/<int:id_case> /', characteristic_case_pc, name='characteristic_case_pc'),
    path('cooler/<int:id_cooler> /', characteristic_cooler, name='characteristic_cooler'),
    path('ddr/<int:id_ddr> /', characteristic_ddr, name='characteristic_ddr'),
    path('mboard/<int:id_mboard> /', characteristic_mboard, name='characteristic_mboard'),
    path('processors/<int:id_power_supply> /', characteristic_power_supply, name='characteristic_power_supply'),
    path('processors/<int:id_proc> /', characteristic_proc, name='characteristic_storage'),


    path('filter-data/',filter_video.as_view(), name ='filter'),
    #path('search/',Search.as_view(), name ='search'),

]