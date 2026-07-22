from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from app_pretest.forms import LessonForm, QuestionSetForm

from .models import Lesson, Pretest, QuestionSet

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

# ▀▄▀▄ menampilkan form CREATE lesson
def lesson_create(request): 

    if request.method == "POST": 
        form = LessonForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Lesson berhasil ditambahkan."
            )
            return redirect("app_pretest:lesson")
    else:
        form = LessonForm()
    return render(
        request,
        "common/lesson-create.html",
        {
            "form": form,
        },
    )

# ▀▄▀▄ menampilkan laman update lesson
def lesson_update(request, lesson_id):

    lesson = get_object_or_404(Lesson, pk=lesson_id,)

    if request.method == "POST":

        print(request.POST)
        print(request.POST.get("description"))

        form = LessonForm(
            request.POST,
            instance=lesson,
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Lesson berhasil diperbarui."
            )
            return redirect("app_pretest:lesson")
    else:
        form = LessonForm(
            instance=lesson,
        )

    return render(
        request,
        "common/lesson-update.html",
        {
            "lesson": lesson,
            "form": form,
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

# ▀▄▀▄ question list
def question_set(request):

    question_sets = (
        QuestionSet.objects
        .select_related(
            "lesson",
            "owner",
        )
        .all()
    )

    return render(
        request,
        "common/question-set.html",
        {
            "question_sets": question_sets,
        },
    )

# ▀▄▀▄ menampilkan form CREATE question set
def question_set_create(request):

    if request.method == "POST":

        form = QuestionSetForm(request.POST)

        if form.is_valid():

            question_set = form.save(commit=False)
            question_set.owner = request.user
            question_set.save()

            messages.success(
                request,
                "Question Set berhasil ditambahkan."
            )

            return redirect("app_pretest:question_set")

    else:

        form = QuestionSetForm()

    return render( request, "common/question-set-create-update.html",
        { 
            "form": form,
        },
    )


# ▀▄▀▄ menampilkan form UPDATE question set
def question_set_update(request, question_set_id):

    question_set = get_object_or_404(QuestionSet, pk=question_set_id,)

    if request.method == "POST":

        form = QuestionSetForm(
            request.POST,
            instance=question_set,
        )

        if form.is_valid():

            question_set = form.save(commit=False)
            question_set.owner = request.user
            question_set.save()

            messages.success(
                request,
                "Question Set berhasil diperbarui."
            )

            return redirect("app_pretest:question_set")

    else:

        form = QuestionSetForm(
            instance=question_set,
        )

    return render( request, "common/question-set-create-update.html",
        {
            "question_set": question_set,
            "form": form,
        },
    )


# ▀▄▀▄ fungsi DELETE question set
def question_set_delete(request, question_set_id):

    question_set = get_object_or_404(QuestionSet, pk=question_set_id,)

    question_set.delete()

    messages.success(
        request,
        "Question Set berhasil dihapus."
    )

    return redirect("app_pretest:question_set")