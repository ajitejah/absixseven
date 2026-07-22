from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.http import JsonResponse 
from django.template.loader import render_to_string
from app_auth import admin
from app_auth.models import Teacher, User
from app_guidance.service import create_notification, log_parent_activity
from app_roadmap.models import Submission
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, User

from .models import Message, Notification, ParentActivityLog

@login_required
def message_redirect(request):

    latest_message = Message.objects.filter(
        Q(sender=request.user) |
        Q(receiver=request.user)
    ).order_by('-created_at').first()

    # belum ada chat
    if not latest_message:
        return redirect('home')

    # tentukan lawan chat
    if latest_message.sender == request.user:
        chat_user = latest_message.receiver
    else:
        chat_user = latest_message.sender

    if hasattr(request.user, 'teacher'):

        return redirect(
            'teacher_guidance:message_detail',
            user_id=chat_user.id
        )

    elif hasattr(request.user, 'student'):

        return redirect(
            'student_guidance:message_detail',
            user_id=chat_user.id
        )

    elif hasattr(request.user, 'parent'):

        return redirect(
            'parent_guidance:message_detail',
            user_id=chat_user.id
        )
    
     # fallback wajib
    return redirect('/')


# ▀▄▀▄ message
@login_required
def message(request, user_id):
 

    submission_id = request.GET.get("submission")
    print("GET submission =", submission_id)

    submission = None

    if submission_id:
        submission = get_object_or_404(
            Submission.objects.select_related(
                "student__user",
                "assignment__node__roadmap",
            ),
            pk=submission_id,
        )

    # =========================
    # 1. ACTIVE CHAT USER
    # =========================
    chat_user = get_object_or_404(User, id=user_id) 

    # =====================================
    # Auto attach submission (sekali saja)
    # =====================================
    if submission:

        attachment_exists = Message.objects.filter(
            sender=request.user,
            receiver=chat_user,
            submission=submission,
            type=Message.MessageType.SUBMISSION,
        ).exists()

        if not attachment_exists:

            Message.objects.create(
                sender=request.user,
                receiver=chat_user,
                assignment=submission.assignment,
                submission=submission,
                type=Message.MessageType.SUBMISSION,
                content="",   # tidak perlu isi karena akan tampil sebagai card
            )

        log_parent_activity(
            parent=request.user,
            activity_type=ParentActivityLog.ActivityType.ASK,
            title=f"Tanya Guru {submission.assignment.node.roadmap.owner.first_name}",
            description=f"Menayakan tentang jawaban Tugas {submission.assignment.title}"
        )

        create_notification(
            receiver=chat_user,
            sender=request.user,
            notification_type=Notification.NotificationType.CHAT,
            title="Pesan Baru",
            description=f"Orang tua mengirim pesan untuk menanyakan tentang jawaban Tugas {submission.assignment.title}",
            path=f"/teacher/guidance/message/{request.user.id}/"
        )

    # 🔥 update last_seen user yang sedang membuka chat
    request.user.last_seen = timezone.now()
    request.user.save(update_fields=["last_seen"])

    # mark as read (pesan masuk dari lawan chat)
    Message.objects.filter(
        sender=chat_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    # =========================
    # 3. RECEIVER LIST (INBOX / HISTORY INTERAKSI)
    # =========================
    interactions = Message.objects.filter(
        Q(sender=request.user) |
        Q(receiver=request.user)
    ).order_by('-created_at')

    user_map = {}

    for msg in interactions:

        # lawan interaksi (bukan diri sendiri)
        other = msg.receiver if msg.sender == request.user else msg.sender

        # hanya simpan chat terbaru per user
        if other.id not in user_map:
            user_map[other.id] = {
                "user": other,
                "last_message": msg.content,
                "last_time": msg.created_at,
                "photo": other.photo.url if other.photo else None,
            }

    receiver_list = sorted(
        user_map.values(),
        key=lambda x: x["last_time"],
        reverse=True
    )

    # =========================
    # CONTEXT
    # =========================
    context = {
        "chat_user": chat_user, 
        "receiver_list": receiver_list,
        "submission": submission,
    }

    return render(request, "common/message.html", context)

# ▀▄▀▄ json message fetch (load message tanpa refresh page)
@login_required 
def message_fetch(request, user_id):
    print(request.POST)
    chat_user = get_object_or_404(User, id=user_id)

    # ambil last message id dari frontend
    last_id = request.GET.get("last_id")

    messages = (
        Message.objects.select_related(
            "sender",
            "submission__student__user",
            "submission__assignment__node__roadmap",
        )
        .filter(
            Q(sender=request.user, receiver=chat_user)
            | Q(sender=chat_user, receiver=request.user)
        )
        .order_by("created_at")
    )

    # hanya ambil pesan baru
    if last_id:
        messages = messages.filter(id__gt=last_id)

    data = []

    for msg in messages:

        data.append({
            # ==========================
            # Message
            # ==========================
            "id": msg.id,
            "type": msg.type,
            "content": msg.content,
            "created_at": msg.created_at.strftime("%H:%M"),

            # ==========================
            # Sender
            # ==========================
            "sender_id": msg.sender.id,
            "is_me": msg.sender == request.user,
            "photo": (
                request.build_absolute_uri(msg.sender.photo.url)
                if msg.sender.photo else None
            ),

            # ==========================
            # Submission Attachment
            # ==========================
            "submission_id": msg.submission.id if msg.submission else None,

            "student": (
                msg.submission.student.user.get_full_name()
                if msg.submission else ""
            ),

            "assignment": (
                msg.submission.assignment.title
                if msg.submission else ""
            ),

            "roadmap": (
                msg.submission.assignment.node.roadmap.name
                if msg.submission else ""
            ),

            "score": (
                msg.submission.score
                if msg.submission else None
            ),

            "feedback": (
                msg.submission.feedback
                if msg.submission else ""
            ),
        })

    return JsonResponse({
        "messages": data
    })

# ▀▄▀▄ json last seen
@login_required
def last_seen(request):
    request.user.last_seen = timezone.now()
    request.user.save(update_fields=["last_seen"])

    return JsonResponse({"status": "ok"})

# ▀▄▀▄ json info dilihat
@login_required
def presence(request, user_id):

    user = User.objects.get(id=user_id)

    return JsonResponse({
        "user_id": user.id,
        "last_seen": user.last_seen.isoformat() if user.last_seen else None
    })

# ▀▄▀▄ json kirim pesan, create message  
@login_required
def message_send(request, user_id):

    print("===== SEND =====")
    print("METHOD :", request.method)
    print("POST   :", request.POST)

    if request.method != "POST":
        return JsonResponse({"success": False}, status=400)

    chat_user = get_object_or_404(User, id=user_id)

    content = request.POST.get("content", "").strip()

    if not content:
        return JsonResponse({
            "success": False,
            "message": "Pesan kosong"
        }, status=400)

    # ==========================================
    # Ambil submission (jika chat dari submission)
    # ==========================================

    submission = None
    assignment = None

    submission_id = request.POST.get("submission")

    if submission_id:

        submission = get_object_or_404(
            Submission.objects.select_related(
                "assignment",
                "student__user",
                "assignment__node__roadmap"
            ),
            pk=submission_id
        )

        assignment = submission.assignment

        # ==================================================
        # Buat attachment submission (hanya sekali)
        # ==================================================

        attachment_exists = Message.objects.filter(
            sender=request.user,
            receiver=chat_user,
            submission=submission,
            type=Message.MessageType.SUBMISSION
        ).exists()

        if not attachment_exists:

            Message.objects.create(
                sender=request.user,
                receiver=chat_user,
                assignment=assignment,
                submission=submission,
                type=Message.MessageType.SUBMISSION,
                content=f"Submission: {submission.assignment.title}"
            )

    # ==========================================
    # Simpan pesan user
    # ==========================================

    message = Message.objects.create(
        sender=request.user,
        receiver=chat_user,
        assignment=assignment,
        submission=submission,
        type=Message.MessageType.TEXT,
        content=content
    )
 
    if message:
        create_notification(
            receiver=chat_user,
            sender=request.user,
            notification_type=Notification.NotificationType.CHAT,
            title=f"Chat Baru dari {request.user.first_name}",
            description=f"Orang tua mengirim pesan baru",
            path=f"/teacher/guidance/message/{request.user.id}/"
        ) 

    return JsonResponse({
        "success": True,
        "message_id": message.id,
        "content": message.content,
        "created_at": message.created_at.strftime("%H:%M")
    })


@login_required
def log_activity(request):

    activities = ParentActivityLog.objects.filter(
        parent=request.user
    ).order_by("-created_at")

    return render(
        request,
        "parent/log-activity.html",
        {
            "activities": activities
        }
    )

@login_required
def notification(request):

    notifications = Notification.objects.filter(
        receiver=request.user
    ).order_by("-created_at")

    # ====================================
    # Tandai semua notifikasi sudah dibaca
    # ====================================
    Notification.objects.filter(
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    return render(
        request,
        "common/notification.html",
        {
            "notifications": notifications,
        },
    )

@login_required
def notification_redirect(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        receiver=request.user,
    )

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    return redirect(notification.path)