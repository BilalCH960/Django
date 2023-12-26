from django.urls import path
from app import views

urlpatterns = [
    path('',views.index,name='index'),
    # path('about',views.about,name='about'),
    # path('contact',views.contact,name='contact'),
    path('login',views.handlelogin,name='handlelogin'),
    path('signup',views.handlesignup,name='handlesignup'),
    path('logout',views.handlelogout,name='handlelogout'),
    path('adminn',views.adminpanel,name='adminpanel'),
    path('update/<id>',views.updateuser,name='updateuser'),
    path('delete/<id>',views.deleteuser,name='deleteuser'),
    # path('alogin',views.handleadminlogin,name='handleadminlogin'),   
    path('create',views.createuser,name='createuser'),
]

