from django.contrib import admin
from django.urls import include, path

from . import views
app_name = 'app_scoring'
urlpatterns = [ 
     
    path('evaluation/', views.evaluation_list, name='evaluation_list'),  
    path('evaluation/confirm/', views.evaluation_confirm,name='evaluation_confirm'),
    path('evaluation/<int:evaluation_id>/preview/',views.evaluation_preview,name='evaluation_preview'),
    path('evaluation/<int:evaluation_id>/chart/',views.evaluation_chart,name='evaluation_chart'),
    path('evaluation/create/<int:roadmap_id>/',views.evaluation_create,name='evaluation_create'),
    path('evaluation/summary', views.evaluation_list, name='evaluation_summary'), 
 
    #path('node/assesment/delete', views.register_view, name='register'), 

]   