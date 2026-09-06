from django.shortcuts import get_object_or_404, render, redirect
from app_scoring.models import Evaluation
from django.http import JsonResponse
from django.views.decorators.http import require_POST 
from app_roadmap.models import Roadmap
from django.db.models import Avg
import json
 
from django.contrib.auth.decorators import login_required 

from app_pretest.models import Pretest, Attempt 

from django.contrib import messages 

from app_scoring.models import Evaluation, Score
from app_roadmap.models import Submission
  


# ▀▄▀▄ menampilkan daftar evaluasi
def evaluation_list(request):
    user = request.user

    # 🧑‍🎓 STUDENT → hanya lihat evaluasi dirinya
    if hasattr(user, 'student'):

        evaluations = Evaluation.objects.filter(
            student=user.student
        ).select_related(
            'roadmap',
            'student',
        )

    # 🛠️ ADMIN → lihat semua evaluasi
    elif user.is_superuser or user.is_staff:

        evaluations = Evaluation.objects.all().select_related(
            'roadmap',
            'student',
        )

    # 👨‍🏫 TEACHER → hanya evaluasi dari roadmap miliknya
    else:

        evaluations = Evaluation.objects.filter(
            roadmap__owner=user
        ).select_related(
            'roadmap',
            'student',
            'student__user',
        )

    evaluations = evaluations.order_by(
        'confirmed',
        '-id'
    )

    return render(
        request,
        'common/evaluation-list.html',
        {
            'evaluations': evaluations
        }
    )
# ▀▄▀▄ json "confirm" permintaan roadmap/evaluasi
@require_POST
def evaluation_confirm(request):

    # validasi teacher
    if not hasattr(request.user, 'teacher'):
        return JsonResponse({
            'success': False,
            'message': 'Akses ditolak'
        }, status=403)

    evaluation_id = request.POST.get('evaluation_id')

    try:
        evaluation = Evaluation.objects.get(id=evaluation_id)

        evaluation.confirmed = True
        evaluation.save()

        return JsonResponse({
            'success': True,
            'message': 'Evaluasi berhasil dikonfirmasi'
        })

    except Evaluation.DoesNotExist:

        return JsonResponse({
            'success': False,
            'message': 'Evaluasi tidak ditemukan'
        }, status=404)

# ▀▄▀▄ menampilkan laman preview/detail grafik evaluasi
def evaluation_preview(request, evaluation_id): 

    evaluation = get_object_or_404(
        Evaluation.objects.select_related(
            'student',
            'student__user',
            'roadmap'
        ),
        id=evaluation_id
    )

    # =====================================================
    # GRAFIK 1
    # NILAI PER SUBMISSION (BERDASARKAN TANGGAL + TOOLTIP)
    # =====================================================

    submissions = (
        Submission.objects
        .filter(
            student=evaluation.student,
            assignment__node__roadmap=evaluation.roadmap,
            score__isnull=False
        )
        .select_related(
            'assignment',
            'assignment__node'
        )
        .order_by('submitted_at')
    )

    submission_labels = []
    submission_scores = []
    submission_tooltips = []

    for sub in submissions:

        # 📅 X-axis (ringkas saja)
        submission_labels.append(
            sub.submitted_at.strftime('%d %b %Y')
        )

        # 📊 nilai
        submission_scores.append(
            float(sub.score)
        )

        # 🧠 detail untuk tooltip
        submission_tooltips.append(
            f"{sub.assignment.title} - {sub.assignment.node.name}"
        )
        
    # =====================================================
    # GRAFIK 2
    # RATA-RATA PER NODE
    # =====================================================

    node_labels = []
    node_scores = []

    nodes = evaluation.roadmap.nodes.all().order_by('order')

    for node in nodes:

        avg_score = (
            Submission.objects
            .filter(
                student=evaluation.student,
                assignment__node=node,
                score__isnull=False
            )
            .aggregate(avg=Avg('score'))
        )['avg']

        node_labels.append(node.name)

        node_scores.append(
            round(avg_score or 0, 2)
        )

    context = {

        'evaluation': evaluation,

        # line chart 
        'submission_labels': json.dumps(submission_labels),
        'submission_scores': json.dumps(submission_scores),
        'submission_tooltips': json.dumps(submission_tooltips),

        # bar chart
        'node_labels': json.dumps(node_labels),
        'node_scores': json.dumps(node_scores),

        # tabel
        'submissions': submissions,
    }

    return render(
        request,
        'common/evaluation-preview.html',
        context
    )

# ▀▄▀▄ json load chart di laman preview/detail
def evaluation_chart(request, evaluation_id):
    try:
        evaluation = Evaluation.objects.get(id=evaluation_id)

        labels = []
        scores = []

        for item in evaluation.scores.order_by('created_at'):
            labels.append(
                item.created_at.strftime('%d %b %Y')
            )
            scores.append(item.score)

        return JsonResponse({
            'success': True,
            'labels': labels,
            'scores': scores,
            'student': (
                f"{evaluation.student.user.first_name} "
                f"{evaluation.student.user.last_name}"
            ),
            'roadmap': evaluation.roadmap.name
        })

    except Evaluation.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Evaluation tidak ditemukan'
        }, status=404)

# ▀▄▀▄ json create evaluation/permintaan join roadmap
@require_POST
def evaluation_create(request, roadmap_id):

    if not hasattr(request.user, 'student'):
        return JsonResponse({
            'success': False,
            'message': 'Hanya siswa yang dapat mengikuti roadmap'
        })

    roadmap = Roadmap.objects.get(id=roadmap_id)

    evaluation, created = Evaluation.objects.get_or_create(
        roadmap=roadmap,
        student=request.user.student,
        confirmed=False,
    )

    return JsonResponse({
        'success': True,
        'created': created
    }) 

@login_required
def evaluation_upper_create(request, pretest_id):

    # Hanya student
    if not hasattr(request.user, 'student'):
        messages.error(request, 'Only students can access this roadmap.')
        return redirect('student_pretest:pretest')

    pretest = get_object_or_404(
        Pretest,
        id=pretest_id
    )

    # Pastikan student memang sudah mengerjakan Pretest
    attempt = get_object_or_404(
        Attempt,
        pretest=pretest,
        student=request.user.student,
        status=Attempt.Status.SCORED,
    )

    # Validasi score untuk Upper Roadmap
    if (
        pretest.curriculum == "IGCSE"
        and attempt.score != 9
    ) or (
        pretest.curriculum == "IBDP"
        and attempt.score != 7
    ):
        messages.error(
            request,
            'You are not eligible for this roadmap.'
        )
        return redirect(
            'student_pretest:pretest_result',
            pretest_id=pretest.id
        )

    # Pastikan Upper Roadmap tersedia
    if not pretest.upper_roadmap:
        messages.error(
            request,
            'Upper roadmap is not available.'
        )
        return redirect(
            'student_pretest:pretest_result',
            pretest_id=pretest.id
        )

    roadmap = pretest.upper_roadmap

    # Buat Evaluation atau gunakan yang sudah ada
    evaluation, created = Evaluation.objects.get_or_create(
        roadmap=roadmap,
        student=request.user.student,
        defaults={
            'confirmed': True,
        }
    )

    # Jika Evaluation sudah ada tetapi belum dikonfirmasi
    if not evaluation.confirmed:
        evaluation.confirmed = True
        evaluation.save(update_fields=['confirmed'])

    return redirect(
        'student_roadmap:roadmap_explore',
        id=roadmap.id
    )

@login_required
def evaluation_lower_create(request, pretest_id):

    # Hanya student
    if not hasattr(request.user, 'student'):
        messages.error(
            request,
            'Only students can access this roadmap.'
        )
        return redirect('student_pretest:pretest')

    pretest = get_object_or_404(
        Pretest,
        id=pretest_id
    )

    # Pastikan student memang sudah mengerjakan Pretest
    attempt = get_object_or_404(
        Attempt,
        pretest=pretest,
        student=request.user.student,
        status=Attempt.Status.SCORED,
    )

    # Validasi score untuk Lower Roadmap
    if (
        pretest.curriculum == "IGCSE"
        and attempt.score != 8
    ) or (
        pretest.curriculum == "IBDP"
        and attempt.score != 6
    ):
        messages.error(
            request,
            'You are not eligible for this roadmap.'
        )
        return redirect(
            'student_pretest:pretest_result',
            pretest_id=pretest.id
        )

    # Pastikan Lower Roadmap tersedia
    if not pretest.lower_roadmap:
        messages.error(
            request,
            'Lower roadmap is not available.'
        )
        return redirect(
            'student_pretest:pretest_result',
            pretest_id=pretest.id
        )

    roadmap = pretest.lower_roadmap

    # Buat Evaluation atau gunakan yang sudah ada
    evaluation, created = Evaluation.objects.get_or_create(
        roadmap=roadmap,
        student=request.user.student,
        defaults={
            'confirmed': True,
        }
    )

    # Jika Evaluation sudah ada tetapi belum dikonfirmasi
    if not evaluation.confirmed:
        evaluation.confirmed = True
        evaluation.save(update_fields=['confirmed'])

    return redirect(
        'student_roadmap:roadmap_explore',
        id=roadmap.id
    )