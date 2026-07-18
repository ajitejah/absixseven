from django.contrib import admin
from django.urls import include, path

from . import views
app_name = 'app_screening'

urlpatterns = [ 
    
    path('question-list/', views.question_list, name='question_list'), 
    path('question/<int:placement_question_id>/json/', views.question_detail, name='question_detail'),
    path("question/<int:question_id>/update/", views.question_update, name="question_update"),
    path("question/create/", views.question_create, name="question_create"),
    path("submit-level-session/", views.submit_level_session, name="screening_submit_session")
    
    #path('question-update/', views.question_update, name='question_list'),  
    #path('node/assesment/delete', views.register_view, name='register'), 

]