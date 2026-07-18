from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [ 
    
    # ▀▄▀▄ authentikasi website
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'), 
    path('reset/', views.reset_password_view, name='reset'), 
    path('register/', views.register_view, name='register'), 

    # ▀▄▀▄ pengelolaan user di dashboard admin
    path('list/', views.user_list, name='admin_user_list'),
    path('detail/<int:id>/', views.user_detail, name='admin_user_detail'),
    path('delete/<int:id>/', views.user_delete, name='admin_user_delete'),
    path("student-own-parent/<int:student_id>/", views.student_own_parent, name="student_own_parent"),

]   