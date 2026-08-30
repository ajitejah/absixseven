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
        "common/lesson-create-update.html",
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
        "common/lesson-create-update.html",
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

# ▀▄▀▄ student yang mengikuti pretest
@login_required
def pretest_student_list(request, pretest_id):

    # Pastikan pretest memang milik teacher yang sedang login
    # melalui QuestionSet.owner
    pretest = get_object_or_404(
        Pretest,
        id=pretest_id,
        question_set__owner=request.user,
    )

    # Daftar student yang memiliki Attempt pada pretest ini
    attempts = (
        Attempt.objects
        .filter(pretest=pretest)
        .select_related(
            "student",
            "student__user",
            "student__level",
        )
        .order_by("-started_at")
    )

    context = {
        "pretest": pretest,
        "attempts": attempts,
    }

    return render(
        request,
        "teacher/pretest-student-list.html",
        context,
    )

@login_required
def pretest_student_result(request, pretest_id, attempt_id):

    attempt = get_object_or_404(
        Attempt.objects.select_related(
            "pretest",
            "pretest__question_set",
            "pretest__question_set__lesson",
            "student",
            "student__user",
        ),
        id=attempt_id,
        pretest__question_set__owner=request.user,
    )

    answers = (
        attempt.answers
        .select_related(
            "question",
            "selected_option",
        )
        .prefetch_related(
            "question__choices",
            "question__pairs",
        )
        .order_by(
            "question__order",
            "question__id",
        )
    )

    if request.method == "POST":

        with transaction.atomic():

            for answer in answers:

                # Hanya Essay yang dinilai manual
                if answer.question.question_type != "ESSAY":
                    continue

                score_key = f"score_{answer.id}"
                score_value = request.POST.get(score_key)

                if score_value in (None, ""):
                    continue

                try:
                    score = float(score_value)
                except (TypeError, ValueError):
                    continue

                # Batasi nilai 0 sampai point soal
                score = max(
                    0,
                    min(score, answer.question.point)
                )

                answer.score = score
                answer.is_correct = score > 0
                answer.save(
                    update_fields=[
                        "score",
                        "is_correct",
                    ]
                )

            # ==========================================
            # HITUNG ULANG ATTEMPT
            # ==========================================

            all_answers = attempt.answers.select_related("question")

            total_question = all_answers.count()

            correct_answer = 0
            wrong_answer = 0
            blank_answer = 0
            total_score = 0
            total_point = 0

            essay_ungraded = False

            for answer in all_answers:

                question = answer.question

                total_point += question.point
                total_score += answer.score

                # ESSAY
                if question.question_type == "ESSAY":

                    if (
                        answer.essay_answer
                        and answer.score == 0
                        and not answer.is_correct
                    ):
                        essay_ungraded = True

                    if answer.score > 0:
                        correct_answer += 1
                    elif not answer.essay_answer:
                        blank_answer += 1
                    else:
                        wrong_answer += 1

                # MCQ / MATCHING
                else:

                    if answer.is_correct:
                        correct_answer += 1
                    elif (
                        not answer.selected_option
                        and not answer.matching_answer
                    ):
                        blank_answer += 1
                    else:
                        wrong_answer += 1

            # ==========================================
            # NILAI AKHIR
            # ==========================================

            if total_point > 0:
                final_score = (
                    total_score / total_point
                ) * 100
            else:
                final_score = 0

            # Cek apakah masih ada essay yang belum dinilai
            ungraded_essay = all_answers.filter(
                question__question_type="ESSAY",
                essay_answer__isnull=False,
            ).exclude(
                essay_answer=""
            ).filter(
                score=0,
                is_correct=False,
            ).exists()

            if ungraded_essay:
                status = Attempt.Status.SUBMITTED
            else:
                status = Attempt.Status.SCORED

            attempt.total_question = total_question
            attempt.correct_answer = correct_answer
            attempt.wrong_answer = wrong_answer
            attempt.blank_answer = blank_answer
            attempt.score = final_score
            attempt.status = status

            attempt.save(
                update_fields=[
                    "total_question",
                    "correct_answer",
                    "wrong_answer",
                    "blank_answer",
                    "score",
                    "status",
                ]
            )

        return redirect(
            "teacher_pretest:pretest_student_result",
            pretest_id=pretest_id,
            attempt_id=attempt.id,
        )

    context = {
        "pretest": attempt.pretest,
        "attempt": attempt,
        "answers": answers,
    }

    return render(
        request,
        "teacher/pretest-student-result.html",
        context,
    )

# ▀▄▀▄ preent start  
@login_required
def pretest_start(request, pretest_id):

    student = request.user.student

    # =========================================================
    # AMBIL PRETEST
    # =========================================================

    pretest = get_object_or_404(
        Pretest.objects.select_related(
            "question_set",
            "question_set__lesson",
        ),
        pk=pretest_id,
        is_active=True,
    )

    # =========================================================
    # AMBIL / BUAT ATTEMPT
    # =========================================================

    attempt, created = Attempt.objects.get_or_create(
        student=student,
        pretest=pretest,
        defaults={
            "status": Attempt.Status.DRAFT,
            "started_at": timezone.now(),
        },
    )

    # =========================================================
    # JIKA SUDAH SUBMITTED
    # =========================================================

    if attempt.status == Attempt.Status.SUBMITTED:
        return redirect(
            "student_pretest:pretest_result",
            attempt.pk,
        )

    # =========================================================
    # AMBIL SEMUA QUESTION
    # =========================================================

    questions_queryset = (
        Question.objects
        .filter(
            question_set=pretest.question_set
        )
        .prefetch_related(
            "choices",
            "pairs",
        )
        .order_by(
            "order",
            "id",
        )
    )

    all_questions = list(
        questions_queryset
    )

    # =========================================================
    # ATTEMPT BARU
    # GENERATE RANDOM + SIMPAN ORDER
    # =========================================================

    if created:

        # -----------------------------------------------------
        # RANDOM QUESTION
        # -----------------------------------------------------

        if pretest.random_question:
            random.shuffle(all_questions)

        else:
            all_questions.sort(
                key=lambda q: (
                    q.order,
                    q.id,
                )
            )

        # -----------------------------------------------------
        # BATASI JUMLAH SOAL
        # -----------------------------------------------------

        selected_questions = all_questions[
            :pretest.question_count
        ]

        # -----------------------------------------------------
        # SIMPAN QUESTION ORDER
        # -----------------------------------------------------

        attempt.question_order = [
            question.id
            for question in selected_questions
        ]

        # -----------------------------------------------------
        # SIAPKAN ORDER PILIHAN
        # -----------------------------------------------------

        choice_order = {}
        matching_order = {}

        for question in selected_questions:

            # =================================================
            # MULTIPLE CHOICE
            # =================================================

            if (
                question.question_type
                == Question.Type.MULTIPLE_CHOICE
            ):

                choices = list(
                    question.choices.all()
                )

                if pretest.random_option:
                    random.shuffle(choices)

                else:
                    choices.sort(
                        key=lambda choice: (
                            choice.order,
                            choice.id,
                        )
                    )

                choice_order[
                    str(question.id)
                ] = [
                    choice.id
                    for choice in choices
                ]

            # =================================================
            # MATCHING
            # =================================================

            elif (
                question.question_type
                == Question.Type.MATCHING
            ):

                pairs = list(
                    question.pairs.all()
                )

                if pretest.random_option:
                    random.shuffle(pairs)

                else:
                    pairs.sort(
                        key=lambda pair: (
                            pair.order,
                            pair.id,
                        )
                    )

                matching_order[
                    str(question.id)
                ] = [
                    pair.id
                    for pair in pairs
                ]

        # -----------------------------------------------------
        # SIMPAN KE ATTEMPT
        # -----------------------------------------------------

        attempt.choice_order = choice_order
        attempt.matching_order = matching_order
        attempt.total_question = len(
            selected_questions
        )

        attempt.save(
            update_fields=[
                "question_order",
                "choice_order",
                "matching_order",
                "total_question",
            ]
        )

    # =========================================================
    # ATTEMPT LAMA
    # CONTINUE PRETEST
    # =========================================================

    else:

        question_ids = (
            attempt.question_order or []
        )

        # -----------------------------------------------------
        # SAFETY FALLBACK
        # Untuk Attempt lama yang belum mempunyai
        # question_order
        # -----------------------------------------------------

        if not question_ids:

            if pretest.random_question:
                random.shuffle(all_questions)

            selected_questions = all_questions[
                :pretest.question_count
            ]

            attempt.question_order = [
                question.id
                for question in selected_questions
            ]

            attempt.total_question = len(
                selected_questions
            )

            attempt.save(
                update_fields=[
                    "question_order",
                    "total_question",
                ]
            )

        else:

            # -------------------------------------------------
            # BUAT MAP QUESTION
            # -------------------------------------------------

            question_map = {
                question.id: question
                for question in questions_queryset
            }

            selected_questions = []

            # -------------------------------------------------
            # SUSUN SESUAI ORDER ATTEMPT
            # -------------------------------------------------

            for question_id in question_ids:

                question = question_map.get(
                    question_id
                )

                if question:
                    selected_questions.append(
                        question
                    )

    # =========================================================
    # LOAD ORDER PILIHAN
    # =========================================================

    choice_order = (
        attempt.choice_order or {}
    )

    matching_order = (
        attempt.matching_order or {}
    )

    # =========================================================
    # LOAD ANSWER YANG SUDAH DISIMPAN
    # =========================================================

    answers = (
        attempt.answers
        .select_related(
            "selected_option"
        )
        .filter(
            question__in=selected_questions
        )
    )

    answer_map = {
        answer.question_id: answer
        for answer in answers
    }

    # =========================================================
    # SIAPKAN DATA QUESTION
    # =========================================================

    for question in selected_questions:

        # =====================================================
        # LOAD ANSWER
        # =====================================================

        question.answer = answer_map.get(
            question.id
        )

        # =====================================================
        # MULTIPLE CHOICE
        # =====================================================

        if (
            question.question_type
            == Question.Type.MULTIPLE_CHOICE
        ):

            choices = list(
                question.choices.all()
            )

            saved_order = choice_order.get(
                str(question.id),
                []
            )

            # -------------------------------------------------
            # GUNAKAN ORDER YANG TERSIMPAN
            # -------------------------------------------------

            if saved_order:

                choice_map = {
                    choice.id: choice
                    for choice in choices
                }

                ordered_choices = []

                for choice_id in saved_order:

                    choice = choice_map.get(
                        choice_id
                    )

                    if choice:
                        ordered_choices.append(
                            choice
                        )

                # -------------------------------------------------
                # JIKA ADA CHOICE BARU
                # TAMBAHKAN DI BELAKANG
                # -------------------------------------------------

                existing_ids = {
                    choice.id
                    for choice in ordered_choices
                }

                for choice in choices:

                    if choice.id not in existing_ids:
                        ordered_choices.append(
                            choice
                        )

                choices = ordered_choices

            else:

                choices.sort(
                    key=lambda choice: (
                        choice.order,
                        choice.id,
                    )
                )

            question.random_choices = choices

        # =====================================================
        # ESSAY
        # =====================================================

        elif (
            question.question_type
            == Question.Type.ESSAY
        ):

            # Jawaban sudah tersedia melalui:
            #
            # question.answer.essay_answer
            #
            # Tidak perlu proses tambahan.

            pass

        # =====================================================
        # MATCHING
        # =====================================================

        elif (
            question.question_type
            == Question.Type.MATCHING
        ):

            pairs = list(
                question.pairs.all()
            )

            saved_order = matching_order.get(
                str(question.id),
                []
            )

            # -------------------------------------------------
            # GUNAKAN ORDER YANG TERSIMPAN
            # -------------------------------------------------

            if saved_order:

                pair_map = {
                    pair.id: pair
                    for pair in pairs
                }

                ordered_pairs = []

                for pair_id in saved_order:

                    pair = pair_map.get(
                        pair_id
                    )

                    if pair:
                        ordered_pairs.append(
                            pair
                        )

                # -------------------------------------------------
                # JIKA ADA PAIR BARU
                # TAMBAHKAN DI BELAKANG
                # -------------------------------------------------

                existing_ids = {
                    pair.id
                    for pair in ordered_pairs
                }

                for pair in pairs:

                    if pair.id not in existing_ids:
                        ordered_pairs.append(
                            pair
                        )

                pairs = ordered_pairs

            else:

                pairs.sort(
                    key=lambda pair: (
                        pair.order,
                        pair.id,
                    )
                )

            # -------------------------------------------------
            # LEFT SIDE
            # -------------------------------------------------

            question.random_pairs = pairs

            # -------------------------------------------------
            # DRAG & DROP OPTIONS
            # -------------------------------------------------

            question.random_options = pairs

            # -------------------------------------------------
            # LOAD MATCHING ANSWER
            # -------------------------------------------------

            if question.answer:

                question.saved_matching_answer = (
                    question.answer.matching_answer
                    or {}
                )

            else:

                question.saved_matching_answer = {}

    # =========================================================
    # CONTEXT
    # =========================================================

    context = {
        "pretest": pretest,
        "questions": selected_questions,
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