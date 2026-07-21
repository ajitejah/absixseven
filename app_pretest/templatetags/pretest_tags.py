from django import template

register = template.Library()


@register.simple_tag
def lesson_url(user):

    if hasattr(user, "admin"):
        return "/admin/pretest/lesson/"

    elif hasattr(user, "teacher"):
        return "/teacher/pretest/lesson/"

    return "#"


@register.simple_tag
def lesson_create_url(user):

    if hasattr(user, "admin"):
        return "/admin/pretest/lesson/create/"

    elif hasattr(user, "teacher"):
        return "/teacher/pretest/lesson/create/"

    return "#"


@register.simple_tag
def lesson_update_url(user, lesson):

    if hasattr(user, "admin"):
        return f"/admin/pretest/lesson/{lesson.id}/update/"

    elif hasattr(user, "teacher"):
        return f"/teacher/pretest/lesson/{lesson.id}/update/"

    return "#"


@register.simple_tag
def lesson_delete_url(user, lesson):

    if hasattr(user, "admin"):
        return f"/admin/pretest/lesson/{lesson.id}/delete/"

    elif hasattr(user, "teacher"):
        return f"/teacher/pretest/lesson/{lesson.id}/delete/"

    return "#"


@register.simple_tag
def pretest_url(user):

    if hasattr(user, "admin"):
        return "/admin/pretest/"

    elif hasattr(user, "teacher"):
        return "/teacher/pretest/"

    return "#"

@register.simple_tag
def question_set_url(user):

    if hasattr(user, "admin"):
        return "/admin/pretest/question-set"

    elif hasattr(user, "teacher"):
        return "/teacher/pretest/question-set"

    return "#"