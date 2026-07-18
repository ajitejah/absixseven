from django import template
from django.urls import reverse

register = template.Library()

# ▀▄▀▄ json redirect kirim url
@register.simple_tag
def message_send_url(user, user_id):  
    if hasattr(user, 'teacher'): 
        return f'/admin/guidance/message/send/{user_id}/' 
    elif hasattr(user, 'student'):
        return f'/student/guidance/message/send/{user_id}/' 
    elif hasattr(user, 'parent'):
        return f'/parent/guidance/message/send/{user_id}/' 
    return f'/admin/guidance/send/message/send/{user_id}/'

# ▀▄▀▄ redirect menampilkan laman message
@register.simple_tag
def message_url(user):  
    if hasattr(user, 'teacher'):
        return '/teacher/guidance/message/' 
    elif hasattr(user, 'student'):
        return '/student/guidance/message/' 
    elif hasattr(user, 'parent'):
        return '/parent/guidance/message/' 
    return '/teacher/guidance/message/'

# ▀▄▀▄ json info seen terakhir
@register.simple_tag
def last_seen_url(user):  
    if hasattr(user, 'teacher'):
        return '/teacher/guidance/message/last-seen/' 
    elif hasattr(user, 'student'):
        return '/student/guidance/message/last-seen/' 
    elif hasattr(user, 'parent'):
        return '/parent/guidance/message/last-seen/' 
    return '/teacher/guidance/message/last-seen/'

# ▀▄▀▄ json redirect presence
@register.simple_tag
def presence_url(user, user_id): 
    if hasattr(user, 'teacher'):
        return f'/teacher/guidance/message/presence/{user_id}/' 
    elif hasattr(user, 'student'):
        return f'/student/guidance/message/presence/{user_id}/' 
    elif hasattr(user, 'parent'):
        return f'/parent/guidance/message/presence/{user_id}/' 
    return f'/teacher/guidance/message/presence/{user_id}/'

# ▀▄▀▄ json redirect fetch message
@register.simple_tag
def message_fetch_url(user, user_id): 
    if hasattr(user, 'teacher'):
        return f'/teacher/guidance/message/fetch/{user_id}/' 
    elif hasattr(user, 'student'):
        return f'/student/guidance/message/fetch/{user_id}/' 
    elif hasattr(user, 'parent'):
        return f'/parent/guidance/message/fetch/{user_id}/' 
    return f'/teacher/guidance/message/fetch/{user_id}/'

# ▀▄▀▄ json redirect mengambil detail message
@register.simple_tag
def message_detail_url(user, user_id):  
    if hasattr(user, 'teacher'):
        return f'/teacher/guidance/message/{user_id}/' 
    elif hasattr(user, 'student'):
        return f'/student/guidance/message/{user_id}/' 
    elif hasattr(user, 'parent'):
        return f'/parent/guidance/message/{user_id}/' 
    return f'/teacher/guidance/message/{user_id}/'


@register.simple_tag
def notification_redirect_url(user, notification_id):

    if user.is_authenticated:

        if hasattr(user, "admin"):
            return f"/admin/guidance/notification/{notification_id}/"

        elif hasattr(user, "teacher"):
            return f"/teacher/guidance/notification/{notification_id}/"

        elif hasattr(user, "parent"):
            return f"/parent/guidance/notification/{notification_id}/"

        elif hasattr(user, "student"):
            return f"/student/guidance/notification/{notification_id}/"

    return "#"


@register.simple_tag
def notification_list_url(user):

    if user.is_authenticated:

        if hasattr(user, "admin"):
            return "/admin/guidance/notification/"

        elif hasattr(user, "teacher"):
            return "/teacher/guidance/notification/"

        elif hasattr(user, "parent"):
            return "/parent/guidance/notification/"

        elif hasattr(user, "student"):
            return "/student/guidance/notification/"

    return "#"

@register.simple_tag
def log_activity_url(user):
    if hasattr(user, "teacher"):
        return "/admin/guidance/log-activity/"
    elif hasattr(user, "student"):
        return "/student/guidance/log-activity/"
    elif hasattr(user, "parent"):
        return "/parent/guidance/log-activity/"
    return "/admin/guidance/log-activity/"