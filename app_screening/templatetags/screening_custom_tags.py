from django import template

register = template.Library()

@register.filter
def has_attr(obj, attr_name):
    return hasattr(obj, attr_name)


# ▀▄▀▄ redirect menampilkan laman daftar QUESTION
@register.simple_tag
def placement_question_list_url(user):

    if hasattr(user, 'admin'):
        return '/admin/screening/question-list/'

    elif hasattr(user, 'teacher'):
        return '/teacher/screening/question-list/' 

    return '/screening/'

# ▀▄▀▄ json redirect create QUESTIOn
@register.simple_tag
def placement_question_create_url(user):

    if hasattr(user, 'admin'):
        return '/admin/screening/question/create/'

    elif hasattr(user, 'teacher'):
        return '/teacher/screening/question/create/' 

    return '/admin/screening/question/create/'

# ▀▄▀▄ json redirect update QUESTIOn
@register.simple_tag
def submit_level_session(): 
    return '/screening/submit-level-session/'

