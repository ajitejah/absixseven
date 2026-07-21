from django.contrib import admin
from django.urls import include, path

from . import views
app_name = 'app_pretest'
urlpatterns = [ 
    
    path('lesson/', views.lesson, name='lesson'), 
    path('lesson/create/', views.lesson_create, name='lesson_create'),  
    path('lesson/<int:lesson_id>/update/', views.lesson_update, name='lesson_update'), 
    path('lesson/<int:lesson_id>/delete/', views.lesson_delete, name='lesson_delete'), 

    path('', views.pretest, name='pretest'), 

]   