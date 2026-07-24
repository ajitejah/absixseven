from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from app_pretest.forms import ChoiceOptionFormSet, LessonForm, MatchingPairFormSet, PretestForm, QuestionForm, QuestionSetForm

from .models import Lesson, Pretest, Question, QuestionSet

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

# ▀▄▀▄ menampilkan seluruh pretest
def pretest(request):
    user = request.user

    pretests = Pretest.objects.all().order_by("title")

    if hasattr(user, 'teacher'):
        return render(
            request,
            "teacher/pretest.html",
            {
                "pretests": pretests,
            },
        )
    
    elif hasattr(user, 'student'):
        return render(
            request,
            "student/pretest.html",
            {
                "pretests": pretests,
            },
        )

# ▀▄▀▄ AJAX informasi Question Set
def question_set_info(request, question_set_id):

    question_set = get_object_or_404(
        QuestionSet,
        pk=question_set_id,
    )

    questions = question_set.questions.all()

    return JsonResponse({

        "success": True, 
        "id": question_set.id, 
        "name": question_set.name, 
        "lesson": question_set.lesson.name, 
        "total_question": questions.count(), 
        "mcq": questions.filter(
            question_type=Question.Type.MULTIPLE_CHOICE,
        ).count(), 
        "essay": questions.filter(
            question_type=Question.Type.ESSAY,
        ).count(), 
        "matching": questions.filter(
            question_type=Question.Type.MATCHING,
        ).count(), 
    })

# ▀▄▀▄ CREATE PRETEST
def pretest_create(request):

    if request.method == "POST": 
        form = PretestForm(request.POST) 
        if form.is_valid(): 
            pretest = form.save(commit=False) 
            pretest.save()

            messages.success(
                request,
                "Pretest berhasil dibuat."
            )

            return redirect(
                "app_pretest:pretest"
            )

    else: 
        form = PretestForm()

    return render(
        request,
        "teacher/pretest-create-update.html",
        {
            "form": form,
            "pretest": None,
        },
    )

# ▀▄▀▄ UPDATE PRETEST
def pretest_update(request, pretest_id):

    pretest = get_object_or_404(
        Pretest,
        pk=pretest_id,
    )

    if request.method == "POST":

        form = PretestForm(
            request.POST,
            instance=pretest,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Pretest berhasil diperbarui."
            )

            return redirect(
                "app_pretest:pretest"
            )

    else:

        form = PretestForm(
            instance=pretest,
        )

    return render(
        request,
        "teacher/pretest-create-update.html",
        {
            "form": form,
            "pretest": pretest,
        },
    )

# ▀▄▀▄ DELETE PRETEST
def pretest_delete(request, pretest_id):

    pretest = get_object_or_404(
        Pretest,
        pk=pretest_id,
    )

    title = pretest.title

    pretest.delete()

    messages.success(
        request,
        f'Pretest "{title}" berhasil dihapus.'
    )

    return redirect(
        "app_pretest:pretest"
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
        "teacher/question-set.html",
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

    return render( request, "teacher/question-set-create-update.html",
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

    return render( request, "teacher/question-set-create-update.html",
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

# ▀▄▀▄ menampilkan tabel daftar question sesuai dengan paketnya/questionset
def question(request, question_set_id):

    question_set = get_object_or_404(
        QuestionSet,
        pk=question_set_id,
    )

    questions = Question.objects.filter(
        question_set=question_set,
    ).order_by(
        "order",
        "id",
    )

    return render(
        request,
        "teacher/question.html",
        {
            "question_set": question_set,
            "questions": questions,
        },
    )
 
# ▀▄▀▄ CREATE QUESTION
def question_create(request, question_set_id):

    question_set = get_object_or_404(
        QuestionSet,
        pk=question_set_id,
    )

    if request.method == "POST":

        form = QuestionForm(
            request.POST,
            request.FILES,
        )

        choice_formset = ChoiceOptionFormSet(
            request.POST,
            prefix="choice",
        )

        matching_formset = MatchingPairFormSet(
            request.POST,
            prefix="matching",
        )

        if form.is_valid():

            with transaction.atomic():

                question = form.save(commit=False)
                question.question_set = question_set
                question.save()

                if question.question_type == Question.Type.MULTIPLE_CHOICE:

                    choice_formset.instance = question

                    if choice_formset.is_valid():
                        choice_formset.save()
                    else:
                        raise Exception(choice_formset.errors)

                elif question.question_type == Question.Type.MATCHING:

                    matching_formset.instance = question

                    if matching_formset.is_valid():
                        matching_formset.save()
                    else:
                        raise Exception(matching_formset.errors)

            messages.success(
                request,
                "Soal berhasil ditambahkan.",
            )

            return redirect(
                "app_pretest:question",
                question_set_id=question_set.id,
            )

    else:

        form = QuestionForm()

        choice_formset = ChoiceOptionFormSet(
            prefix="choice",
        )

        matching_formset = MatchingPairFormSet(
            prefix="matching",
        )

    return render(
        request,
        "teacher/question-create-update.html",
        {
            "form": form,
            "question": None,
            "question_set": question_set,
            "choice_formset": choice_formset,
            "matching_formset": matching_formset,
        },
    )

# ▀▄▀▄ UPDATE QUESTION
def question_update(request, question_set_id, question_id):

    question = get_object_or_404(
        Question,
        pk=question_id,
    )

    if request.method == "POST":

        form = QuestionForm(
            request.POST,
            request.FILES,
            instance=question,
        )

        choice_formset = ChoiceOptionFormSet(
            request.POST,
            instance=question,
            prefix="choice",
        )

        matching_formset = MatchingPairFormSet(
            request.POST,
            instance=question,
            prefix="matching",
        )

        if form.is_valid():

            with transaction.atomic():

                question = form.save()

                if question.question_type == Question.Type.MULTIPLE_CHOICE:

                    choice_formset.instance = question

                    if choice_formset.is_valid():
                        choice_formset.save()
                    else:
                        raise Exception(choice_formset.errors)

                elif question.question_type == Question.Type.MATCHING:

                    matching_formset.instance = question

                    if matching_formset.is_valid():
                        matching_formset.save()
                    else:
                        raise Exception(matching_formset.errors)

            messages.success(
                request,
                "Soal berhasil diperbarui.",
            )

            return redirect(
                "app_pretest:question",
                question_set_id=question.question_set.id, 
            )

    else:

        form = QuestionForm(
            instance=question,
        )

        choice_formset = ChoiceOptionFormSet(
            instance=question,
            prefix="choice",
        )

        matching_formset = MatchingPairFormSet(
            instance=question,
            prefix="matching",
        )

    return render(
        request,
        "teacher/question-create-update.html",
        {
            "form": form,
            "question": question,
            "question_set": question.question_set,
            "choice_formset": choice_formset,
            "matching_formset": matching_formset,
        },
    )

# ▀▄▀▄ fungsi delete question
def question_delete(request, question_id):

    question = get_object_or_404(
        Question,
        pk=question_id,
    )

    question_set_id = question.question_set.id

    question.delete()

    messages.success(
        request,
        "Soal berhasil dihapus.",
    )

    return redirect(
        "app_pretest:question",
        question_set_id=question_set_id,
    )