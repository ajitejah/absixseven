import json

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from app_auth.models import User
from app_screening.models import PlacementQuestion

# ▀▄▀▄ fungsi reset semua password akun
def reset_all_passwords(request):
    # 🔐 simple security key (ubah sesuai kebutuhan kamu)
    secret = request.GET.get("key")

    if secret != "reset123":
        return HttpResponse("Unauthorized", status=401)

    users = User.objects.all()

    for user in users:
        user.set_password("default")
        user.save()

    return HttpResponse("All passwords have been reset to 'default'")

# ▀▄▀▄ menampilkan laman home
def home(request): 

    return render(request, 'visitor/home.html')

# ▀▄▀▄ menampilkan laman screening
def screening(request):

    questions = PlacementQuestion.objects.prefetch_related('options').order_by('?')[:5]

    data = []

    for q in questions:
        data.append({
            "id": q.id,
            "question": q.question,
            "word": q.question,  # kalau kamu belum punya field arabic word, bisa pakai ini dulu
            "options": [
                {
                    "id": opt.id,
                    "text": opt.answer,
                    "score": opt.score
                }
                for opt in q.options.all().order_by('order')
            ]
        })

    return render(request, 'visitor/screening.html', {
        "questions_json": json.dumps(data)
    })

# ▀▄▀▄ menampilkan laman dashboard admin
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

# ▀▄▀▄ menampilkan laman dashboard teacher
def teacher_dashboard(request):
    return render(request, 'teacher/dashboard.html')

# ▀▄▀▄ menampilkan laman dashboard student
def student_dashboard(request):
    return render(request, 'student/dashboard.html')

# ▀▄▀▄ menampilkan laman dashboard parent/orang-tua
def parent_dashboard(request):
    return render(request, 'parent/dashboard.html')