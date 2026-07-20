from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Lesson, Pretest

# ▀▄▀▄ menampilkan seluruh lesson
def lesson(request):

    lessons = Lesson.objects.all().order_by("name")

    return render(
        request,
        "common/lesson.html",
        {
            "lessons": lessons,
        },
    )

 # ▀▄▀▄ laman create lesson
def lesson_create(request):

    if request.method == "POST":

        Lesson.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description", ""),
        )

        messages.success(request, "Lesson berhasil ditambahkan.")

        return redirect("app_pretest:lesson")

    return render(
        request,
        "admin/lesson-create.html",
    )

# ▀▄▀▄ menampilkan laman update lesson
def lesson_update(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        pk=lesson_id,
    )

    if request.method == "POST":

        lesson.name = request.POST.get("name")
        lesson.description = request.POST.get("description", "")
        lesson.save()

        messages.success(request, "Lesson berhasil diperbarui.")

        return redirect("app_pretest:lesson")

    return render(
        request,
        "admin/lesson-update.html",
        {
            "lesson": lesson,
        },
    )

# ▀▄▀▄ fungsi delete lesson
def lesson_delete(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        pk=lesson_id,
    )

    lesson.delete()

    messages.success(request, "Lesson berhasil dihapus.")

    return redirect("app_pretest:lesson")

# ▀▄▀▄ menampilkan seluruh lesson
def pretest(request):

    pretests = Pretest.objects.all().order_by("title")

    return render(
        request,
        "common/pretest.html",
        {
            "pretests": pretests,
        },
    )