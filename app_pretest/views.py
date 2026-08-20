from django.contrib import messages
from django.db.models import Prefetch
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from app_pretest.forms import ChoiceOptionFormSet, LessonForm, MatchingPairFormSet, PretestForm, QuestionForm, QuestionSetForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from .models import Answer, Attempt, Lesson, Pretest, Question, QuestionSet
from django.db import transaction
from django.utils import timezone  
import random

from app_pretest.models import ( 
    Question,
    ChoiceOption,
    MatchingPair,
)

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

    # ▀▄ TEACHER / ADMIN 
    if hasattr(user, 'teacher') or hasattr(user, 'admin'):

        pretests = (
            Pretest.objects
            .all()
            .order_by("title")
        )

        return render(
            request,
            "teacher/pretest.html",
            {
                "pretests": pretests,
            },
        )

    # ▀▄ STUDENT 
    elif hasattr(user, 'student'):

        pretests = (
            Pretest.objects
            .select_related(
                "question_set",
                "question_set__lesson",
            )
            .prefetch_related(
                Prefetch(
                    "attempts",
                    queryset=Attempt.objects.filter(
                        student=user.student,
                    ),
                    to_attr="student_attempts",
                )
            )
            .order_by("title")
        )

        return render(
            request,
            "student/pretest.html",
            {
                "pretests": pretests,
                "now" : timezone.now(),
            },
        )

# ▀▄▀▄ preent start
@login_required
def pretest_start(request, pretest_id): 

    user = request.user

    pretest = get_object_or_404(
        Pretest.objects.select_related(
            "question_set",
            "question_set__lesson",
        ),
        pk=pretest_id,
        is_active=True,
    )

    attempt, created = Attempt.objects.get_or_create(
        student=user.student,
        pretest=pretest,
        defaults={
            "status": Attempt.Status.DRAFT,
            "started_at": timezone.now(),
        },
    )

    if attempt.status == Attempt.Status.SUBMITTED:
        return redirect(
            "student_pretest:pretest_result",
            attempt.pk,
        )

    # ▀▄ ambil soal
    questions = list(
        Question.objects.filter(
            question_set=pretest.question_set
        ).prefetch_related(
            "choices",
            "pairs",
        ).order_by(
            "order",
            "id",
        )
    )

    # ▀▄ RANDOM SOAL 
    if pretest.random_question: 
        random.shuffle(questions)
    else:
        questions.sort(key=lambda q: (q.order, q.id))

    # ▀▄ BATASI JUMLAH SOAL 
    questions = questions[:pretest.question_count]

    # ▀▄ RANDOM PILIHAN   
    for question in questions:

        # ▀▄ ---------- MCQ ---------- 
        choices = list(
            question.choices.all()
        )

        if pretest.random_option:
            random.shuffle(choices)
        else:
            choices.sort(key=lambda c: c.order)

        question.random_choices = choices

        # ▀▄ ---------- MATCHING ---------- 
        pairs = list(
            question.pairs.all()
        )

        # ▀▄ pasangan untuk sisi kiri
        if pretest.random_option:
            random.shuffle(pairs)
        else:
            pairs.sort(key=lambda p: p.order)

        question.random_pairs = pairs

        # ▀▄ OPTIONS DRAG DROP  
        options = list(
            question.pairs.all()
        )

        if pretest.random_option:
            random.shuffle(options)
        else:
            options.sort(key=lambda p: p.order)

        question.random_options = options

    # ▀▄ SUBMIT PRETEST 
    if request.method == "POST":

        student = request.user.student

        with transaction.atomic():

            attempt, created = Attempt.objects.get_or_create(
                pretest=pretest,
                student=student,
            )

            # ▀▄ jika submit ulang
            attempt.answers.all().delete()

            total_question = 0
            blank_answer = 0

            questions = Question.objects.filter(
                question_set=pretest.question_set
            ).prefetch_related(
                "pairs"
            )

            for question in questions:

                total_question += 1

                # ▀▄ MULTIPLE CHOICE 
                if question.question_type == Question.Type.MULTIPLE_CHOICE:

                    option_id = request.POST.get(
                        f"question_{question.id}"
                    )

                    Answer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_option_id=option_id if option_id else None,
                    )

                    if not option_id:
                        blank_answer += 1

                # ▀▄ ESSAY 
                elif question.question_type == Question.Type.ESSAY:

                    essay = request.POST.get(
                        f"question_{question.id}",
                        ""
                    ).strip()

                    Answer.objects.create(
                        attempt=attempt,
                        question=question,
                        essay_answer=essay,
                    )

                    if essay == "":
                        blank_answer += 1

                # ▀▄ MATCHING 
                elif question.question_type == Question.Type.MATCHING:

                    matching = {}

                    for pair in question.pairs.all():
                        value = request.POST.get(
                            f"question_{question.id}_pair_{pair.id}"
                        )

                        if value:
                            matching[str(pair.id)] = value

                    Answer.objects.create(
                        attempt=attempt,
                        question=question,
                        matching_answer=matching,
                    )

                    if len(matching) == 0:
                        blank_answer += 1

            attempt.total_question = total_question
            attempt.blank_answer = blank_answer
            attempt.status = Attempt.Status.SUBMITTED
            attempt.submitted_at = timezone.now()

            attempt.save()

        # ▀▄ redirect ke halaman pretest result
        return redirect(
            "student_pretest:pretest_result",
            attempt.pk,
        )

    context = {
        "pretest": pretest,
        "questions": questions,
        "attempt": attempt,
    }

    return render(
        request,
        "student/pretest-start.html",
        context,
    )

# ▀▄▀▄ pretest result
@login_required
def pretest_result(request, pretest_id):
    pretest = get_object_or_404(
        Pretest.objects.select_related(
            "question_set",
            "question_set__lesson",
        ),
        pk=pretest_id,
        is_active=True,
    )

    attempt = get_object_or_404(
        Attempt.objects.select_related(
            "student",
            "student__user",
            "pretest",
            "pretest__question_set",
            "pretest__question_set__lesson",
        ).prefetch_related(
            "answers",
            "answers__question",
            "answers__selected_option",
        ),
        pretest=pretest,
        student=request.user.student,
    )

    return render(
        request,
        "student/pretest-result.html",
        {
            "pretest": pretest,
            "attempt": attempt,
        },
    )

# ▀▄▀▄ answer save 
@login_required
@require_POST
def answer_save(request, attempt_id):

    student = request.user.student

    # ==========================================
    # AMBIL ATTEMPT
    # ==========================================
    attempt = get_object_or_404(
        Attempt,
        pk=attempt_id,
        student=student,
        status=Attempt.Status.DRAFT,
    )

    # ==========================================
    # AMBIL QUESTION
    # ==========================================
    question_id = request.POST.get("question_id")

    if not question_id:
        return JsonResponse(
            {
                "success": False,
                "message": "Question ID tidak ditemukan.",
            },
            status=400,
        )

    question = get_object_or_404(
        Question,
        pk=question_id,
    )

    # ==========================================
    # VALIDASI QUESTION
    # HARUS MILIK PRETEST ATTEMPT
    # ==========================================
    if question.question_set_id != attempt.pretest.question_set_id:
        return JsonResponse(
            {
                "success": False,
                "message": "Question tidak termasuk dalam pretest.",
            },
            status=400,
        )

    # ==========================================
    # DEFAULT ANSWER
    # ==========================================
    defaults = {
        "selected_option_id": None,
        "essay_answer": "",
        "matching_answer": {},
    }

    # ==========================================
    # MULTIPLE CHOICE
    # ==========================================
    if question.question_type == Question.Type.MULTIPLE_CHOICE:

        option_id = request.POST.get("option_id")

        if option_id:
            defaults["selected_option_id"] = option_id

    # ==========================================
    # ESSAY
    # ==========================================
    elif question.question_type == Question.Type.ESSAY:

        defaults["essay_answer"] = request.POST.get(
            "essay_answer",
            "",
        ).strip()

    # ==========================================
    # MATCHING
    # ==========================================
    elif question.question_type == Question.Type.MATCHING:

        matching_raw = request.POST.get(
            "matching_answer",
            "{}",
        )

        try:
            matching_answer = json.loads(matching_raw)

        except (json.JSONDecodeError, TypeError):
            return JsonResponse(
                {
                    "success": False,
                    "message": "Format matching answer tidak valid.",
                },
                status=400,
            )

        if not isinstance(matching_answer, dict):
            return JsonResponse(
                {
                    "success": False,
                    "message": "Matching answer harus berupa object.",
                },
                status=400,
            )

        defaults["matching_answer"] = matching_answer

    # ==========================================
    # TIPE QUESTION TIDAK DIKENAL
    # ==========================================
    else:
        return JsonResponse(
            {
                "success": False,
                "message": "Tipe question tidak didukung.",
            },
            status=400,
        )

    # ==========================================
    # SAVE / UPDATE ANSWER
    # ==========================================
    answer, created = Answer.objects.update_or_create(
        attempt=attempt,
        question=question,
        defaults=defaults,
    )

    # ==========================================
    # RESPONSE
    # ==========================================
    return JsonResponse(
        {
            "success": True,
            "created": created,
            "answer_id": answer.id,
            "attempt_id": attempt.id,
            "question_id": question.id,
        }
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