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

    path("question-set", views.question_set, name="question_set",),
    path("question-set/create", views.question_set_create, name="question_set_create",),
    path("question-set/<int:question_set_id>/update", views.question_set_update, name="question_set_update",),
    path("question-set/<int:question_set_id>/delete", views.question_set_delete, name="question_set_delete",),

    path("question-set/<int:question_set_id>/question",views.question,name="question",),
    path("question-set/<int:question_set_id>/question/create",views.question_create,name="question_create",),
    path("question-set/<int:question_set_id>/question/<int:question_id>/update",views.question_update,name="question_update",), 
    path("question-set/<int:question_set_id>/question/<int:question_id>/delete",views.question_delete,name="question_delete",),
]   