from django.urls import path
from .import views

urlpatterns = [

    path('act_home/', views.act_home,name="act_home"),


    path('act_register/',views.act_register),
    path('act_login/',views.act_login),
    path('act_logout/', views.act_logout, name="act_logout"),


    path('car_final_report/', views.car_final_report, name="car_final_report"),


    path('getkey_act/<str:project_id>/',views.getkey_act),
    path('decrypt_data_act/<str:project_id>/',views.decrypt_data_act),


    path('act_scan/',views.act_scan, name="act_scan"),
    path('act_calculation/<str:project_id>/',views.act_calculation, name="act_calculation"),
    path('act_file/',views.act_file,name="act_file")


]

