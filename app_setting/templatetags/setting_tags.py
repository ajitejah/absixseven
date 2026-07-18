from django import template
from app_setting.services import SettingService
from django.utils import timezone

from app_tracking.models import Rule

register = template.Library()


@register.simple_tag
def get_setting(group, section, key, default=""):
    return SettingService.get(group, section, key, default)

@register.simple_tag
def web_setting(section, key, default=""):
    return SettingService.get("WEB", section, key, default)


@register.simple_tag
def content_setting(section, key, default=""):
    return SettingService.get("CONTENT", section, key, default)

def _today():
    return timezone.localtime().strftime("%A")


def _now():
    return timezone.localtime().time()


def _check(days, start_time, end_time):

    print("TODAY :", _today())
    print("NOW   :", _now())
    print("START :", start_time)
    print("END   :", end_time)
    
    if not days:
        return False

    if _today() not in days:
        return False

    if not start_time or not end_time:
        return False

    now = _now()

    # Rentang normal
    if start_time <= end_time:
        return start_time <= now <= end_time

    # Rentang melewati tengah malam
    return now >= start_time or now <= end_time


def _rule():
    return Rule.objects.first()


@register.filter
def at_evaluation_time(value=None):
    rule = _rule()

    if not rule:
        return False

    return _check(
        rule.day_to_evaluate,
        rule.start_time_to_evaluate,
        rule.end_time_to_evaluate,
    )


@register.filter
def at_work_time(value=None):
    rule = _rule()

    if not rule:
        return False

    return _check(
        rule.day_to_work,
        rule.start_time_to_work,
        rule.end_time_to_work,
    )


@register.filter
def at_serve_time(value=None):
    rule = _rule()

    if not rule:
        return False

    return _check(
        rule.day_to_serve,
        rule.start_time_to_serve,
        rule.end_time_to_serve,
    )


@register.filter
def at_correct_time(value=None):
    rule = _rule()

    if not rule:
        return False

    return _check(
        rule.day_to_correct,
        rule.start_time_to_correct,
        rule.end_time_to_correct,
    )

@register.simple_tag
def start_evaluation_time():
    rule = _rule()
    return rule.start_time_to_evaluate if rule else None


@register.simple_tag
def start_work_time():
    rule = _rule()
    return rule.start_time_to_work if rule else None


@register.simple_tag
def start_serve_time():
    rule = _rule()
    return rule.start_time_to_serve if rule else None


@register.simple_tag
def start_correct_time():
    rule = _rule()
    return rule.start_time_to_correct if rule else None


@register.simple_tag
def end_evaluation_time():
    rule = _rule()
    return rule.end_time_to_evaluate if rule else None


@register.simple_tag
def end_work_time():
    rule = _rule()
    return rule.end_time_to_work if rule else None


@register.simple_tag
def end_serve_time():
    rule = _rule()
    return rule.end_time_to_serve if rule else None


@register.simple_tag
def end_correct_time():
    rule = _rule()
    return rule.end_time_to_correct if rule else None

@register.filter
def below_minimum_score(score):

    rule = _rule()

    print("RULE =", rule.minimum_score)
    print("SCORE =", score, type(score))

    if score in (None, "", False):
        return False

    result = float(score) < float(rule.minimum_score)

    print("RESULT =", result)

    return result