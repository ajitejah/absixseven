from django.contrib import admin
from django.urls import include, path

from . import views
app_name = 'app_guidance'

urlpatterns = [   
    path('message/', views.message_redirect, name='message'),
    path('message/<int:user_id>/', views.message, name='message_detail'),
    path('message/send/<int:user_id>/', views.message_send, name='message_send'),
    path('message/fetch/<int:user_id>/', views.message_fetch, name='message_fetch'), 
    path("message/last-seen/", views.last_seen, name="last_seen"),
    path("message/presence/<int:user_id>/", views.presence, name="presence"),
    path("log-activity/", views.log_activity, name="log_activity"),
    path("notification/", views.notification, name="notification"),
    path("notification/<int:pk>/", views.notification_redirect, name="notification_redirect")
]  