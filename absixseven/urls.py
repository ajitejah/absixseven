from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    path('reset-passwords/', views.reset_all_passwords, name='reset_passwords'),

    #-------------------------------------------#
    #   >> Korpus Visitor
    #-------------------------------------------#
     
    path('', views.home, name='home'),
    path('page/screening/', views.screening, name='screening'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'), 
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('parent/', views.parent_dashboard, name='parent_dashboard'),
    #path('quals/', views.quals, name='quals'), 

    #-------------------------------------------#
    #   >> Korpus Auth
    #-------------------------------------------# 

    path('auth/', include('app_auth.urls'), name='auth'), 
    path('admin/user/', include('app_auth.urls')), 
    
    
    #-------------------------------------------------------#
    #   >> Screening
    #-------------------------------------------------------# 

    path('admin/pretest/', include(('app_pretest.urls', 'app_pretest'), namespace='admin_pretest')),
    path('teacher/pretest/', include(('app_pretest.urls', 'app_pretest'), namespace='teacher_pretest')),
 
    #-------------------------------------------------------#
    #   >> APP_ROADMAP untuk diakses admin, teacher, student
    #-------------------------------------------------------# 
    path('admin/roadmap/',
        include(('app_roadmap.urls', 'app_roadmap'), namespace='admin_roadmap')
    ),

    path('teacher/roadmap/',
        include(('app_roadmap.urls', 'app_roadmap'), namespace='teacher_roadmap')
    ),

    path('student/roadmap/',
        include(('app_roadmap.urls', 'app_roadmap'), namespace='student_roadmap')
    ),

    path('parent/roadmap/',
        include(('app_roadmap.urls', 'app_roadmap'), namespace='parent_roadmap')
    ),

    #-------------------------------------------------------#
    #   >> APP_GUIDANCE untuk diakses teacher, student, parent
    #-------------------------------------------------------# 

    path('admin/guidance/',
        include(('app_guidance.urls', 'app_guidance'), namespace='admin_guidance')
    ),

    path('teacher/guidance/',
        include(('app_guidance.urls', 'app_guidance'), namespace='teacher_guidance')
    ), 
     
    path('parent/guidance/',
        include(('app_guidance.urls', 'app_guidance'), namespace='parent_guidance')
    ),

    path('student/guidance/',
        include(('app_guidance.urls', 'app_guidance'), namespace='student_guidance')
    ),

    #-------------------------------------------------------#
    #   >> Scoring
    #-------------------------------------------------------# 

    path('admin/scoring/',
        include(('app_scoring.urls', 'app_scoring'), namespace='admin_scoring')
    ),

    path('teacher/scoring/',
        include(('app_scoring.urls', 'app_scoring'), namespace='teacher_scoring')
    ),

    path('student/scoring/',
        include(('app_scoring.urls', 'app_scoring'), namespace='student_scoring')
    ),

    #-------------------------------------------------------#
    #   >> Screening
    #-------------------------------------------------------# 

    path('admin/screening/', include(('app_screening.urls', 'app_screening'), namespace='admin_screening')),
    path('teacher/screening/', include(('app_screening.urls', 'app_screening'), namespace='teacher_screening')),
    path('screening/', include(('app_screening.urls', 'app_screening'), namespace='visitor_screening')),

    #-------------------------------------------------------#
    #   >> Setting
    #-------------------------------------------------------# 

    path('admin/setting/', include(('app_setting.urls', 'app_setting'), namespace='admin_setting')),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)