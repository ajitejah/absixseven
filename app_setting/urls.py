from django.contrib import admin
from django.urls import include, path

from . import views
app_name = 'app_setting'

urlpatterns = [ 
    
    path('content/', views.content, name='setting_content'), 
    path('web/', views.web, name='setting_web'),
    path('rule/', views.rule, name='setting_rule'),
    
    #path('question-update/', views.question_update, name='question_list'),  
    #path('node/assesment/delete', views.register_view, name='register'), 

]