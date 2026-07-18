from django.shortcuts import render
from datetime import time

# Create your views here.
from django.contrib import messages
from django.shortcuts import redirect, render
from collections import OrderedDict
from app_setting.models import Setting
from app_tracking.models import Rule
from datetime import datetime, timedelta
 
def rule(request):

    # Selalu gunakan satu Rule saja
    rule, created = Rule.objects.get_or_create(
        pk=1,
        defaults={
            "name": "Tracking Rule"
        }
    )
 
    if request.method == "POST":

        rule.name = request.POST.get(
            "name",
            "Tracking Rule"
        )

        rule.minimum_score = int(
            request.POST.get(
                "minimum_score",
                75
            )
        )

        # ----------------------------------
        # JSON TAG
        # ----------------------------------

        def parse_days(value):
            if not value:
                return []

            return [
                x.strip()
                for x in value.split(",")
                if x.strip()
            ]

        rule.day_to_evaluate = parse_days( request.POST.get("day_to_evaluate") )
        rule.day_to_serve = parse_days( request.POST.get("day_to_serve") )
        rule.day_to_work = parse_days( request.POST.get("day_to_work") )
        rule.day_to_correct = parse_days( request.POST.get("day_to_correct") )

        # ----------------------------------
        # TIME
        # ----------------------------------

        def parse_time(value):
            if not value:
                return None

            hour, minute = map(int, value.split(":"))

            return time(
                hour,
                minute
            )

        rule.start_time_to_evaluate = parse_time(request.POST.get("start_time_to_evaluate")) 
        rule.end_time_to_evaluate   = parse_time(request.POST.get("end_time_to_evaluate")) 
        rule.start_time_to_serve    = parse_time(request.POST.get("start_time_to_serve")) 
        rule.end_time_to_serve      = parse_time(request.POST.get("end_time_to_serve")) 
        rule.start_time_to_work     = parse_time(request.POST.get("start_time_to_work")) 
        rule.end_time_to_work       = parse_time(request.POST.get("end_time_to_work")) 
        rule.start_time_to_correct  = parse_time(request.POST.get("start_time_to_correct"))
        rule.end_time_to_correct    = parse_time(request.POST.get("end_time_to_correct"))

        # ----------------------------------
        # LIMIT
        # ----------------------------------

        rule.limit_assignment = int(
            request.POST.get(
                "limit_assignment",
                60
            )
        )

        rule.is_active = (
            request.POST.get("is_active")
            == "on"
        )

        rule.save()

        messages.success(
            request,
            "Tracking Rule berhasil diperbarui."
        )

    return render(
        request, "admin/setting-rule.html", {
            "title": "Tracking Rule",
            "rule": rule, 
        }
    )

def web(request):

    if request.method == "POST": 
        settings = Setting.objects.filter(group="WEB") 
        for item in settings: 
            if item.type in ["image", "video"]:

                if str(item.id) in request.FILES:
                    file = request.FILES[str(item.id)]

                    if item.type == "image":
                        item.image = file
                    else:
                        item.video = file

            else:

                item.value = request.POST.get(
                    str(item.id),
                    item.value
                )

            item.save()

        messages.success(
            request,
            "Pengaturan berhasil disimpan."
        )

        return redirect(request.path)

    context = {

        "seo_settings":
            Setting.objects.filter(
                group="WEB",
                section="SEO"
            ),

        "branding_settings":
            Setting.objects.filter(
                group="WEB",
                section="BRANDING"
            ),

        "contact_settings":
            Setting.objects.filter(
                group="WEB",
                section="CONTACT"
            ),

        "social_settings":
            Setting.objects.filter(
                group="WEB",
                section="SOCIAL"
            ),

        "analytics_settings":
            Setting.objects.filter(
                group="WEB",
                section="ANALYTICS"
            ),

    }

    return render(
        request,
        "admin/setting-web.html",
        context,
    )


def content(request):

    if request.method == "POST":

        settings = Setting.objects.filter(group="CONTENT")

        for item in settings:

            # Upload Image / Video
            if item.type in ["image", "video"]:

                uploaded_file = request.FILES.get(str(item.id))

                if uploaded_file:

                    if item.type == "image":
                        item.image = uploaded_file

                    elif item.type == "video":
                        item.video = uploaded_file

            # Text / Textarea / Icon
            else:

                item.value = request.POST.get(
                    str(item.id),
                    item.value
                )

            item.save()

        messages.success(
            request,
            "Pengaturan konten berhasil disimpan."
        )

        return redirect(request.path)

    settings = (
        Setting.objects
        .filter(group="CONTENT", is_active=True)
        .order_by("order")
    )

    sections = OrderedDict()

    for item in settings:

        if item.section not in sections:
            sections[item.section] = []

        sections[item.section].append(item)

    context = {
        "sections": sections,
    }

    return render(
        request,
        "admin/setting-content.html",
        context,
    )