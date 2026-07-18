from django import template

register = template.Library()

@register.filter
def has_attr(obj, attr_name):
    return hasattr(obj, attr_name)

@register.simple_tag
def user_update_url(user):

    if hasattr(user, 'admin'):
        return f'/admin/user/update/'

    elif hasattr(user, 'teacher'):
        return f'/teacher/user/detail/'

    elif hasattr(user, 'student'):
        return f'/student/user/detail/'

    elif hasattr(user, 'parent'):
        return f'/parent/user/detail/'

    return f'/admin/user/detail/'

# ▀▄▀▄ redirect url dashboard
@register.simple_tag
def dashboard_url(user):

    if hasattr(user, 'admin'):
        return '/admin/'

    elif hasattr(user, 'teacher'):
        return '/teacher/'

    elif hasattr(user, 'student'):
        return '/student/'

    return '/admin/'

# ▀▄▀▄ redirest url daftar roadmap
@register.simple_tag
def roadmap_list_url(user):

    if hasattr(user, 'admin'):
        return '/admin/roadmap/'

    elif hasattr(user, 'teacher'):
        return '/teacher/roadmap/'

    elif hasattr(user, 'student'):
        return '/student/roadmap/'

    return '/admin/roadmap/'

# ▀▄▀▄ redirect daftar evaluasi
@register.simple_tag
def evaluation_list_url(user):

    if hasattr(user, 'admin'):
        return '/admin/scoring/evaluation/'

    elif hasattr(user, 'teacher'):
        return '/teacher/scoring/evaluation/'

    elif hasattr(user, 'student'):
        return '/student/scoring/evaluation/'

    return '/admin/scoring/evaluation/'

# ▀▄▀▄ json redirect "confirm" evaluasi
@register.simple_tag
def evaluation_confirm_url(user):

    if hasattr(user, 'admin'):
        return '/admin/scoring/evaluation/confirm/'

    elif hasattr(user, 'teacher'):
        return '/teacher/scoring/evaluation/confirm/'

    elif hasattr(user, 'student'):
        return '/student/scoring/evaluation/confirm/'

    return '/admin/scoring/evaluation/confirm/'

# ▀▄▀▄ json redirect menampilkan chart
@register.simple_tag
def evaluation_chart_url(user, evaluation_id):

    if hasattr(user, 'admin'):
        return f'/admin/scoring/evaluation/{evaluation_id}/chart/'

    elif hasattr(user, 'teacher'):
        return f'/teacher/scoring/evaluation/{evaluation_id}/chart/'

    elif hasattr(user, 'student'):
        return f'/student/scoring/evaluation/{evaluation_id}/chart/'

    return f'/admin/scoring/evaluation/{evaluation_id}/chart/'

# ▀▄▀▄ redirect preview url
@register.simple_tag
def evaluation_preview_url(user, evaluation_id):

    if hasattr(user, 'admin'):
        return f'/admin/scoring/evaluation/{evaluation_id}/preview/'

    elif hasattr(user, 'teacher'):
        return f'/teacher/scoring/evaluation/{evaluation_id}/preview/'

    elif hasattr(user, 'student'):
        return f'/student/scoring/evaluation/{evaluation_id}/preview/'

    return f'/admin/scoring/evaluation/{evaluation_id}/preview/'

# ▀▄▀▄ redirect laman create ROADMAP
@register.simple_tag
def roadmap_create_url(user):

    if user.is_authenticated:

        if hasattr(user, 'admin'):
            return '/admin/roadmap/create/'

        elif hasattr(user, 'teacher'):
            return '/teacher/roadmap/create/'

        elif hasattr(user, 'student'):
            return '/student/roadmap/create/'

    return '/admin/roadmap/create/'

# ▀▄▀▄ redirect laman update ROADMAP
@register.simple_tag
def roadmap_update_url(user, id):

    if user.is_authenticated:

        if hasattr(user, 'admin'):
            return f'/admin/roadmap/update/{id}/'

        elif hasattr(user, 'teacher'):
            return f'/teacher/roadmap/update/{id}/'

        elif hasattr(user, 'student'):
            return f'/student/roadmap/update/{id}/'

    return f'/admin/roadmap/update/{id}/'

# ▀▄▀▄ redirect laman explore (node-node/check point) ROADMAP
@register.simple_tag
def roadmap_explore_url(user, id):

    if user.is_authenticated:

        if hasattr(user, 'admin'):
            return f'/admin/roadmap/explore/{id}/'

        elif hasattr(user, 'teacher'):
            return f'/teacher/roadmap/explore/{id}/'

        elif hasattr(user, 'student'):
            return f'/student/roadmap/explore/{id}/'

    return f'/admin/roadmap/explore/{id}/'

# ▀▄▀▄ redirect menampilkan daftar assignment
@register.simple_tag
def assignment_list_url(user, roadmap_id, node_id):

    if user.is_authenticated:

        if hasattr(user, 'admin'):
            return f'/admin/roadmap/explore/{roadmap_id}/{node_id}/'

        elif hasattr(user, 'teacher'):
            return f'/teacher/roadmap/explore/{roadmap_id}/{node_id}/'

        elif hasattr(user, 'student'):
            return f'/student/roadmap/explore/{roadmap_id}/{node_id}/'

    return f'/admin/roadmap/explore/{roadmap_id}/{node_id}/'

# ▀▄▀▄ redirect menampilkan laman create ASSIGNMENT
@register.simple_tag
def assignment_create_url(user, roadmap_id, node_id):

    if user.is_authenticated:

        if hasattr(user, 'admin'):
            return f'/admin/roadmap/explore/{roadmap_id}/{node_id}/create'

        elif hasattr(user, 'teacher'):
            return f'/teacher/roadmap/explore/{roadmap_id}/{node_id}/create'

        elif hasattr(user, 'student'):
            return f'/student/roadmap/explore/{roadmap_id}/{node_id}/create'

    return f'/admin/roadmap/explore/{roadmap_id}/{node_id}/create'

# ▀▄▀▄ redirect menampilkan laman update
@register.simple_tag
def assignment_update_url(user, roadmap_id, node_id, assignment_id):

    if user.is_authenticated:

        if hasattr(user, 'admin'):
            return f'/admin/roadmap/explore/{roadmap_id}/{node_id}/update/{assignment_id}'

        elif hasattr(user, 'teacher'):
            return f'/teacher/roadmap/explore/{roadmap_id}/{node_id}/update/{assignment_id}'

        elif hasattr(user, 'student'):
            return f'/student/roadmap/explore/{roadmap_id}/{node_id}/update/{assignment_id}'

    return f'/admin/roadmap/explore/{roadmap_id}/{node_id}/update/{assignment_id}'

# ▀▄▀▄ redirect fungsi hapus assignment
@register.simple_tag
def assignment_delete_url(user, roadmap_id, node_id, assignment_id):

    if user.is_authenticated:

        if hasattr(user, 'admin'):
            return f'/admin/roadmap/explore/{roadmap_id}/{node_id}/delete/{assignment_id}'

        elif hasattr(user, 'teacher'):
            return f'/teacher/roadmap/explore/{roadmap_id}/{node_id}/delete/{assignment_id}'

        elif hasattr(user, 'student'):
            return f'/student/roadmap/explore/{roadmap_id}/{node_id}/delete/{assignment_id}'

    return f'/admin/roadmap/explore/{roadmap_id}/{node_id}/delete/{assignment_id}'

@register.simple_tag
def notification_icon(notification_type):

    mapping = {

        "chat": {
            "bg": "bg-info/10",
            "icon": "fa-solid fa-comments",
            "color": "text-info",
        },

        "parent_activity": {
            "bg": "bg-secondary/10",
            "icon": "fa-solid fa-user-clock",
            "color": "text-secondary",
        },

        "assignment": {
            "bg": "bg-success/10",
            "icon": "fa-solid fa-book",
            "color": "text-success",
        },

        "submission": {
            "bg": "bg-warning/10",
            "icon": "fa-solid fa-file-arrow-up",
            "color": "text-warning",
        },

        "score": {
            "bg": "bg-orange-100",
            "icon": "fa-solid fa-star",
            "color": "text-orange-500",
        },

        "roadmap": {
            "bg": "bg-cyan-100",
            "icon": "fa-solid fa-map",
            "color": "text-cyan-500",
        },

        "system": {
            "bg": "bg-error/10",
            "icon": "fa-solid fa-bell",
            "color": "text-error",
        },

    }

    return mapping.get(
        notification_type,
        mapping["system"]
    )
