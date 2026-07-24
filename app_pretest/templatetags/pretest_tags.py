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


# ▀▄▀▄ daftar pretest
@register.simple_tag
def pretest_url(user):

    if hasattr(user, "admin"):
        return "/admin/pretest/"

    elif hasattr(user, "teacher"):
        return "/teacher/pretest/"

    return "#"


# ▀▄▀▄ create pretest
@register.simple_tag
def pretest_create_url(user):

    if hasattr(user, "admin"):
        return "/admin/pretest/create/"

    elif hasattr(user, "teacher"):
        return "/teacher/pretest/create/"

    return "#"


# ▀▄▀▄ update pretest
@register.simple_tag
def pretest_update_url(user, pretest):

    if hasattr(user, "admin"):
        return f"/admin/pretest/{pretest.id}/update/"

    elif hasattr(user, "teacher"):
        return f"/teacher/pretest/{pretest.id}/update/"

    return "#"


# ▀▄▀▄ delete pretest
@register.simple_tag
def pretest_delete_url(user, pretest):

    if hasattr(user, "admin"):
        return f"/admin/pretest/{pretest.id}/delete/"

    elif hasattr(user, "teacher"):
        return f"/teacher/pretest/{pretest.id}/delete/"

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

@register.simple_tag
def question_set_create_url(user):

    if hasattr(user, "admin"):
        return "/admin/pretest/question-set/create"

    elif hasattr(user, "teacher"):
        return "/teacher/pretest/question-set/create"

    return "#"

@register.simple_tag
def question_set_update_url(user, question_set):

    if hasattr(user, "admin"):
        return f"/admin/pretest/question-set/{question_set.id}/update"

    elif hasattr(user, "teacher"):
        return f"/teacher/pretest/question-set/{question_set.id}/update"

    return "#"

@register.simple_tag
def question_url(user, question_set):

    if hasattr(user, "admin"):
        return f"/admin/pretest/question-set/{question_set.id}/question"

    elif hasattr(user, "teacher"):
        return f"/teacher/pretest/question-set/{question_set.id}/question"

    return "#"


@register.simple_tag
def question_create_url(user, question_set):

    if hasattr(user, "admin"):
        return f"/admin/pretest/question-set/{question_set.id}/question/create"

    elif hasattr(user, "teacher"):
        return f"/teacher/pretest/question-set/{question_set.id}/question/create"

    return "#"


@register.simple_tag
def question_update_url(user, question):

    if hasattr(user, "admin"):
        return f"/admin/pretest/question/{question.id}/update"

    elif hasattr(user, "teacher"):
        return f"/teacher/pretest/question/{question.id}/update"

    return "#"


@register.simple_tag
def question_delete_url(user, question):

    if hasattr(user, "admin"):
        return f"/admin/pretest/question/{question.id}/delete"

    elif hasattr(user, "teacher"):
        return f"/teacher/pretest/question/{question.id}/delete"

    return "#"


@register.simple_tag
def question_set_info_url(user, question_set_id=0):

    if hasattr(user, "admin"):
        return f"/admin/pretest/question-set/{question_set_id}/info"

    elif hasattr(user, "teacher"):
        return f"/teacher/pretest/question-set/{question_set_id}/info"

    return "#"