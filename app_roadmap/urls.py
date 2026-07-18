from django.contrib import admin
from django.urls import include, path

from . import views
app_name = 'app_roadmap'
urlpatterns = [ 
     
    path('', views.roadmap_list, name='roadmap_list'), 
    path('create/', views.roadmap_create, name='roadmap_create'), 
    path('update/<int:id>/', views.roadmap_update, name='roadmap_update'), 
    path('explore/<int:id>/', views.roadmap_explore, name='roadmap_explore'), 
    #path('explore/', views.roadmap_explore, name='admin_roadmap_explore'),  
    #path('delete/', views.roadmap_delete, name='admin_roadmap_delete'), 
 
    #path('node/', views.logout_view, name='logout'), 
    path('node/create', views.node_create, name='node_create'), 
    path('node/update/<int:id>/', views.node_update, name='node_update'), 
    path('node/delete/<int:id>/', views.node_delete, name='node_delete'), 

    path('explore/<int:roadmap_id>/<int:node_id>/', views.assignment_list, name='assignment_list'),
    path('explore/<int:roadmap_id>/<int:node_id>/remedial/', views.assignment_remedial_list, name='assignment_list'),
    path('explore/<int:roadmap_id>/<int:node_id>/create', views.assignment_create, name='assignment_create'),
    path('explore/<int:roadmap_id>/<int:node_id>/remedial/<int:submission_id>/create', views.assignment_remedial_create, name='assignment_remedial_create'),
    path('explore/<int:roadmap_id>/<int:node_id>/update/<int:assignment_id>/', views.assignment_update, name='assignment_update'), 
    path('explore/<int:roadmap_id>/<int:node_id>/delete/<int:assignment_id>/', views.assignment_delete, name='assignment_delete'), 
    
    path('explore/<int:roadmap_id>/<int:node_id>/submission/<int:assignment_id>/', views.submission_list, name='submission_list'),
    path("submission/score/save/",views.score_save,name="score_save",), 
    path("submission/reaction/update/", views.submission_reaction_update, name="submission_reaction_update"),
    path('submission/create/<int:assignment_id>/', views.submission_create, name='submission_create'),
    
    #path('node/assesment/create', views.reset_password_view, name='reset'), 
    #path('node/assesment/update', views.register_view, name='register'), 
    #path('node/assesment/delete', views.register_view, name='register'), 

]   