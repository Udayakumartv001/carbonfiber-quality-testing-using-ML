from django.conf import settings
from django.urls import path
from ad_min import views
from django.conf.urls.static import static


urlpatterns = [

    # home page......................

    path('', views.home, name='home'),

#     # Admin login and logout.......................

    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('adminlogout/', views.adminlogout, name='logout'),

     # admin home..........................

    path('adminhome/', views.adminhome, name='adminhome'),


    # admin requirements...................................................

    path('requirements/',views.requirements, name='requirements'),

    # admin approve tables for all modules...............................

    path('formapprove/', views.formapprove, name='formapprove'),
    path('carapprove/', views.carapprove, name='carapprove'),
    path('actapprove/', views.actapprove, name='actapprove'),
    path('evalapprove/', views.evalapprove, name='evalapprove'),
    

    # admin manage tables for all modules...............................

    path('formmanage/', views.formmanage, name='formmanage'),
    path('carmanage/', views.carmanage, name='carmanage'),
    path('actmanage/', views.actmanage, name='actmanage'),
    path('evalmanage/', views.evalmanage, name='evalmanage'),
  

    #manage status...............................................

    path('managestatus/', views.managestatus, name='managestatus'),

    # admin approve and reject.......................................

    path('approve/<int:id>/', views.approve, name='approve'),
    path('reject/<int:id>/', views.reject, name='reject'),

    # generate report .............................................

    path('final_report/<str:project_id>/', views.final_report, name='final_report'),


    


 ]

urlpatterns += static(settings.MEDIA_URL,document_root=settings
 .MEDIA_ROOT)