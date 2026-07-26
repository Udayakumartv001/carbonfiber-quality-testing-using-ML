from django.urls import path
from .import views

urlpatterns = [

    path('car_home/', views.car_home,name="car_home"),


    path('car_register/',views.car_register),
    path('car_login/',views.car_login),
    path('car_logout/', views.car_logout, name="car_logout"),


    path('form_final_report/', views.form_final_report, name="form_final_report"),


    path('getkey_car/<str:project_id>/',views.getkey_car),
    path('decrypt_data_car/<str:project_id>/',views.decrypt_data_car),


    path('car_scan/',views.car_scan, name="car_scan"),
    path('car_calculation/<str:project_id>/',views.car_calculation, name="car_calculation"),
    path('car_file/',views.car_file,name="car_file")


]

