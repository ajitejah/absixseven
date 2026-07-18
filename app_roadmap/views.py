import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from app_auth.models import Level, Student
from app_guidance.models import ParentActivityLog
from app_guidance.service import log_parent_activity
from app_roadmap.forms import NodeForm, RoadmapForm
from app_roadmap.models import Roadmap
from django.http import JsonResponse
from django.views.decorators.http import require_POST 
from app_tracking.models import Foul, Rule
from app_tracking.service import get_correct_schedule

from app_scoring.models import Evaluation  
from .models import Assignment, Roadmap, Node, Submission
from .forms import AssignmentForm, NodeForm
from django.db.models import Count, Max

@login_required
def level_list(request):

    levels = (
        Level.objects
        .annotate(total_students=Count("student"))
        .order_by("id")
    )

    context = {
        "title": "Level",
        "levels": levels,
    }

    return render(request, "admin/common/level.html", context,)

# ▀▄▀▄ menampilkan daftar roadmap
def roadmap_list(request):
    user = request.user

    # 👨‍🎓 STUDENT → semua roadmap aktif
    if hasattr(user, 'student'):

        roadmaps = Roadmap.objects.filter(
            is_active=True
        ).order_by('-created_at')

        for roadmap in roadmaps:

            evaluation = Evaluation.objects.filter(
                roadmap=roadmap,
                student=user.student
            ).first()

            roadmap.evaluation = evaluation

        return render(request, 'student/roadmap.html', {
            'roadmaps': roadmaps
        })
     
    # 👨‍👩‍👧 PARENT
    if hasattr(user, "parent"):

        roadmaps = (
            Roadmap.objects.filter(
                is_active=True,
                evaluations__student__parent=user.parent,
            )
            .distinct()
            .order_by("-created_at")
        )

        # Ambil semua evaluation milik anak-anak parent ini
        evaluations = (
            Evaluation.objects.filter(
                student__parent=user.parent
            )
            .select_related("student__user", "roadmap")
        )

        # roadmap_id -> evaluation
        evaluation_map = {
            e.roadmap_id: e
            for e in evaluations
        }

        # Tempelkan student & evaluation ke roadmap
        for roadmap in roadmaps:
            roadmap.evaluation = evaluation_map.get(roadmap.id)
            roadmap.student = (
                roadmap.evaluation.student
                if roadmap.evaluation
                else None
            )

        return render(request, "common/roadmap.html", {
            "roadmaps": roadmaps,
        })
    
    # 🛠️ ADMIN → semua roadmap
    if user.is_superuser or user.is_staff:
        roadmaps = Roadmap.objects.all().order_by('-created_at')
        return render(request, 'common/roadmap.html', {
            'roadmaps': roadmaps
        })

    # 👨‍🏫 TEACHER → hanya miliknya
    roadmaps = Roadmap.objects.filter(owner=user).order_by('-created_at') 

    return render(request, 'common/roadmap.html', {
        'roadmaps': roadmaps, 
    })

# ▀▄▀▄ fungsi create ROADMAP
@login_required
def roadmap_create(request):
    if request.method == 'POST':
        form = RoadmapForm(request.POST, request.FILES)

        if form.is_valid():
            roadmap = form.save()

            messages.success(request, 'Roadmap berhasil dibuat') 

        else:
            messages.error(request, 'Form tidak valid')

    else:
        form = RoadmapForm()

    return render(request, 'common/roadmap-create.html', {
        'form': form,
        'title': 'Create Roadmap'
    })

# ▀▄▀▄ fungsi update ROADMAP
@login_required
def roadmap_update(request, id):
    roadmap = get_object_or_404(Roadmap, id=id)

    if request.method == "POST":
        form = RoadmapForm(request.POST, request.FILES, instance=roadmap)

        if form.is_valid():
            form.save()
            messages.success(request, "Roadmap berhasil diperbarui.") 
            return redirect("teacher_roadmap:roadmap_list")
    else:
        form = RoadmapForm(instance=roadmap)

    return render(request, "common/roadmap-update.html", {
        "title": "Update Roadmap",
        "form": form,
        "roadmap": roadmap,
    })

# ▀▄▀▄ fungsi menampilkan NODE roadmap
@login_required
def roadmap_explore(request, id):
    roadmap = get_object_or_404(Roadmap, id=id)

    nodes = Node.objects.filter(roadmap=roadmap).order_by('order')

    form = NodeForm(initial={
        'roadmap': roadmap
    })

    return render(request, 'common/roadmap-explore-node.html', {
        'title': 'Update Roadmap',
        'roadmap': roadmap,
        'nodes': nodes,
        'form': form
    })

# ▀▄▀▄ fungsi create NODE di halaman roadmap
@login_required
def node_create(request):
    if request.method == 'POST':
        form = NodeForm(request.POST)

        if form.is_valid():
            node = form.save(commit=False)

            # 🔥 AUTO ORDER
            last_order = Node.objects.filter(
                roadmap=node.roadmap
            ).aggregate(max_order=Max('order'))['max_order'] or 0

            node.order = last_order + 1

            node.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'node': {
                        'id': node.id,
                        'name': node.name,
                        'description': node.description,
                        'is_locked': node.is_locked,
                    }
                })

        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })

    return JsonResponse({'success': False})

# ▀▄▀▄ fungsi update NODE di halaman roadmap
@login_required
def node_update(request, id):
    node = get_object_or_404(Node, id=id)

    if request.method == 'POST':
        form = NodeForm(request.POST, instance=node)

        if form.is_valid():
            node = form.save()

            return JsonResponse({
                'success': True,
                'node': {
                    'id': node.id,
                    'name': node.name,
                    'desc': node.description,
                    'duration': node.duration,
                    'locked': node.is_locked,
                }
            })

        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })

    return JsonResponse({'success': False})

# ▀▄▀▄ fungsi delete NODE di halaman roadmap
@login_required
def node_delete(request, id):
    if request.method == "POST":
        node = get_object_or_404(Node, id=id)
        node.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

# ▀▄▀▄ fungsi menampilkan daftar ASSIGNMENT
@login_required
def assignment_list(request, roadmap_id, node_id):
    roadmap = get_object_or_404(Roadmap, id=roadmap_id)
    node = get_object_or_404(Node, id=node_id, roadmap=roadmap)

    #assignments = Assignment.objects.filter(node=node).order_by('-created_at')
    assignments = Assignment.objects.filter( node=node, referred_fouls__isnull=True ).order_by("-created_at")
    user = request.user
    
    if hasattr(user, 'student'):

        rule = Rule.objects.filter(is_active=True).first()

        for assignment in assignments:
            assignment.correct_schedule = get_correct_schedule(
                assignment.expired,
                rule
            )

        for assignment in assignments:
            
            student = user.student
            
            submission = Submission.objects.filter(
                assignment=assignment,
                student=student
            ).first()

            assignment.student_submission = submission
            assignment.is_submitted = submission is not None 

        return render(request, 'student/submission.html', {
            'title': 'Daftar Assignment',
            'roadmap': roadmap,
            'node': node,
            'assignments': assignments
        })
    else:
        return render(request, 'common/assignment.html', {
            'title': 'Daftar Assignment',
            'roadmap': roadmap,
            'node': node,
            'assignments': assignments,
            'remedial' : False
        })

@login_required
def assignment_remedial_list(request, roadmap_id, node_id):
    roadmap = get_object_or_404(Roadmap, id=roadmap_id)
    node = get_object_or_404(Node, id=node_id, roadmap=roadmap)

    assignments = Assignment.objects.filter( referred_fouls__isnull=False, node=node ).distinct().order_by("-created_at")
    user = request.user
    
    if hasattr(user, 'student'):

        rule = Rule.objects.filter(is_active=True).first()

        for assignment in assignments:
            assignment.correct_schedule = get_correct_schedule(
                assignment.expired,
                rule
            )

        for assignment in assignments:
            
            student = user.student
            
            submission = Submission.objects.filter(
                assignment=assignment,
                student=student
            ).first()

            assignment.student_submission = submission
            assignment.is_submitted = submission is not None 

        return render(request, 'student/submission.html', {
            'title': 'Daftar Assignment',
            'roadmap': roadmap,
            'node': node,
            'assignments': assignments
        })
    else:
        return render(request, 'common/assignment.html', {
            'title': 'Daftar Assignment',
            'roadmap': roadmap,
            'node': node,
            'assignments': assignments,
            'remedial' : True
        })
    
# ▀▄▀▄ fungsi create ASSIGNMENT
@login_required
def assignment_create(request, roadmap_id, node_id):
    
    roadmap = get_object_or_404(Roadmap, id=roadmap_id)
    node = get_object_or_404(Node, id=node_id, roadmap=roadmap)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.node = node
            assignment.save()
            messages.success(request, 'Assignment berhasil dibuat') 
        else:
            messages.error(request, 'Assignment gagal dibuat') 
            
    else:
        form = AssignmentForm()

    return render(request, 'common/assignment-create.html', {
        'title': 'Tambah Assignment',
        'roadmap': roadmap,
        'node': node,
        'form': form
    })

# ▀▄▀▄ ungsi create ASSIGNMENT REMEDIAL
@login_required
def assignment_remedial_create(request, roadmap_id, node_id, submission_id):

    submission = get_object_or_404(
        Submission.objects.select_related(
            "assignment",
            "assignment__node",
            "student",
        ),
        id=submission_id,
    )

    original_assignment = submission.assignment
    node                = original_assignment.node
    roadmap             = node.roadmap

    # Jangan buat dua kali
    if Foul.objects.filter(
        assignment=original_assignment,
        student=submission.student,
        foul_type=Foul.Type.LOW_SCORE,
    ).exists():

        messages.warning(request, "Remedial sudah pernah dibuat.")
        return redirect(
            "teacher_roadmap:submission_list",
            roadmap.id,
            node.id,
            original_assignment.id,
        )

    if request.method == "POST":

        form = AssignmentForm(request.POST, request.FILES)

        if form.is_valid():

            remedial = form.save(commit=False)
            remedial.node = node
            remedial.save()

            Foul.objects.create(

                student=submission.student,
                teacher=request.user.teacher,

                assignment=original_assignment,
                refer=remedial,

                foul_type=Foul.Type.LOW_SCORE,
                overcome_type=Foul.Overcome.REMEDIAL,

                schedule=remedial.release,
                status=Foul.Status.OPEN,

                description=f"Remedial untuk nilai {submission.score}"

            )

            messages.success(request, "Assignment remedial berhasil dibuat.")

            return redirect(
                "teacher_roadmap:assignment_list",
                roadmap.id,
                node.id,
                remedial.id,
            )

    else:

        form = AssignmentForm(
            initial={
                "title": f"Remedial - {original_assignment.title}",
                "description": original_assignment.description,
            }
        )

    return render(
        request, "common/assignment-create.html",
        {
            "title": "Create Remedial",
            "form": form,
            "submission": submission,
            "roadmap": roadmap,
            "node": node,
            "assignment": original_assignment,
        },
    )

# ▀▄▀▄ fungsi update ASSIGNMENT
@login_required
def assignment_update(request, roadmap_id, node_id, assignment_id):
    roadmap = get_object_or_404(Roadmap, id=roadmap_id)
    node = get_object_or_404(Node, id=node_id, roadmap=roadmap)

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        node=node
    )

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)

        if form.is_valid():
            form.save()
            return redirect('teacher_roadmap:assignment_list', roadmap_id=roadmap.id, node_id=node.id)
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'common/assignment-update.html', {
        'title': 'Update Assignment',
        'roadmap': roadmap,
        'node': node,
        'assignment': assignment,
        'form': form
    })

# ▀▄▀▄ fungsi delete ASSIGNMENT
@login_required
def assignment_delete(request, roadmap_id, node_id, assignment_id):
    roadmap = get_object_or_404(Roadmap, id=roadmap_id)
    node = get_object_or_404(Node, id=node_id, roadmap=roadmap)

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        node=node
    )

    if request.method == 'POST':
        assignment.delete()
        return redirect('admin_assignment_list', roadmap_id=roadmap.id, node_id=node.id)

    return render(request, 'admin/assignment-delete.html', {
        'roadmap': roadmap,
        'node': node,
        'assignment': assignment
    })

def submission_list(request, roadmap_id, node_id, assignment_id):

    # ambil data
    roadmap = get_object_or_404(Roadmap, id=roadmap_id) 
    node = get_object_or_404(Node, id=node_id)
    assignment = get_object_or_404(Assignment, id=assignment_id) 
    # ambil semua submission berdasarkan assignment
    submissions = Submission.objects.filter(
        assignment=assignment
    ).select_related('student', 'student__user')
 
    REACTIONS = [
        ("👍", "Bagus"),
        ("👌", "Mantap"),
        ("👏", "Hebat"),
        ("🙌", "Keren"),
        ("💪", "Tetap Semangat"),
        ("🚀", "Lanjutkan"),
        ("🔥", "Luar Biasa"),
        ("⭐", "Bintang"),
        ("🌟", "Membanggakan"),
        ("✨", "Istimewa"),
        ("🎉", "Selamat"),
        ("🎯", "Tepat Sasaran"),
        ("🏅", "Prestasi"),
        ("🥇", "Terbaik"),
        ("🏆", "Juara"),
        ("❤️", "Ayah/Bunda Bangga"),
        ("🥰", "Membanggakan Hati"),
        ("😊", "Senang Melihatnya"),
        ("🤗", "Peluk Virtual"),
        ("💖", "Terima Kasih Sudah Berusaha"),
        ("📚", "Rajin Belajar"),
        ("🧠", "Kerja Keras Terlihat"),
        ("📈", "Terus Meningkat"),
        ("🌱", "Terus Berkembang"),
        ("🌈", "Masa Depan Cerah"),
        ("💯", "Nilai Sempurna"),
        ("🎓", "Calon Orang Hebat"),
        ("🤲", "Semoga Allah Memberkahi"),
        ("🕌", "Barakallahu Fiik"),
        ("☀️", "Semangat Hari Ini"),
    ]

    context = {
        'roadmap'       : roadmap,
        'node'          :node,
        'assignment'    : assignment,
        'submissions'   : submissions,
        'reactions'     : REACTIONS,
    }

    return render(request, 'common/assignment-submission-list.html', context)

def score_save(request):

    if request.method != "POST":
        return redirect(request.META.get("HTTP_REFERER", "/"))

    submission = get_object_or_404(
        Submission,
        pk=request.POST.get("submission_id"),
    )

    submission.score = float(request.POST.get("score"))
    submission.feedback = request.POST.get("feedback", "")
    submission.save(update_fields=["score", "feedback"])

    messages.success(
        request,
        "Nilai berhasil disimpan."
    )

    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
@require_POST
def submission_reaction_update(request):

    print("BODY :", request.body)

    try:
        data = json.loads(request.body)

        print("DATA :", data)

        submission_id = data.get("submission")
        emoji = data.get("reaction")

        print("SUBMISSION :", submission_id)
        print("EMOJI :", emoji)

        submission = Submission.objects.get(id=submission_id)

        submission.reaction = emoji
        submission.save(update_fields=["reaction"])

        log_parent_activity(
            parent=request.user,
            activity_type=ParentActivityLog.ActivityType.REACTION,
            title="Memberi reaksi 😊",
            description="Memberikan reaksi pada Submission Matematika."
        )

        return JsonResponse({
            "success": True,
            "reaction": emoji
        })

    except Exception as e:
        import traceback
        traceback.print_exc()

        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)
    
# ▀▄▀▄ fungsi create SUBMISSION
@login_required
def submission_create(request, assignment_id):

    
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Method tidak diizinkan"
        })

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id
    )

    student = get_object_or_404(
        Student,
        user=request.user
    )

    # Cek sudah submit
    if Submission.objects.filter(
        assignment=assignment,
        student=student
    ).exists():
        return JsonResponse({
            "success": False,
            "message": "Anda sudah mengirim jawaban"
        })

    submission_type = request.POST.get("submission_type")

    if submission_type == "upload":

        uploaded_file = request.FILES.get("submission_file")

        if not uploaded_file:
            return JsonResponse({
                "success": False,
                "message": "File wajib diunggah"
            })

        Submission.objects.create(
            assignment=assignment,
            student=student,
            file=uploaded_file
        )

    elif submission_type == "url":

        submission_url = request.POST.get("submission_url", "").strip()

        if not submission_url:
            return JsonResponse({
                "success": False,
                "message": "URL wajib diisi"
            })

        Submission.objects.create(
            assignment=assignment,
            student=student,
            url=submission_url
        )

    else:
        return JsonResponse({
            "success": False,
            "message": "Tipe pengiriman tidak valid"
        })

    return JsonResponse({
        "success": True,
        "message": "Jawaban berhasil dikirim"
    })