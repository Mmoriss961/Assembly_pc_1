from django.urls import path

from.views import *
from.import views


urlpatterns = [
    path('PC_Assembly_list/', views.PcAssemblyView.as_view()),

    path('', index, name='home'),
    path('videocards/', video, name='video'),
    path('processors/', proc, name='proc'),
    path('test/', test, name='test'),
    path('videocards/<int:id_vga>/', characteristic_video, name='characteristic_video'),
    path('processors/<int:id_proc> /', characteristic_proc, name='characteristic_proc'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('feedback/', feedback, name ='feedback')
]