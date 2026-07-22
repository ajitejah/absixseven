from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app_auth.models import User
from app_guidance.models import Notification
from app_guidance.service import create_notification
from .forms import UserCreateForm, UserUpdateForm
from .models import Level, Teacher, Student, Parent 
from django.contrib.auth import get_user_model
from django.db import transaction 

from app_auth.forms import StudentParentForm 
from app_auth.forms import (
    UserUpdateForm,
    AdminForm,
    TeacherForm,
    ParentForm,
)

User = get_user_model() 

# ▀▄▀▄ auth login
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # ================= ROLE CHECK =================
            if hasattr(user, 'admin'):
                return redirect('admin_dashboard')

            elif hasattr(user, 'teacher'):
                return redirect('teacher_dashboard')

            elif hasattr(user, 'student'):
                return redirect('student_dashboard')

            elif hasattr(user, 'parent'):
                return redirect('parent_dashboard')

            # fallback
            return redirect('/')

        else:
            messages.error(request, 'Email atau password salah')

    return render(request, 'auth/login.html')

# ▀▄▀▄ auth logout
def logout_view(request):
    logout(request)
    return redirect('login')

# ▀▄▀▄ auth register - register dengan jenis usernya 
def register_view(request):
    levels = Level.objects.all()

    session_level_id = request.session.get('placement_level_id')
    session_auto_level = None

    if session_level_id:
        session_auto_level = Level.objects.filter(id=session_level_id).first()

    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES) 
        role = request.POST.get('role')

        # ================= VALIDASI ROLE =================
        if not role:
            messages.error(request, 'Pilih role terlebih dahulu')
            return render(request, 'auth/register.html', {'form': form})

        if form.is_valid():
            user = form.save()

            try:
                # ================= CREATE ROLE =================
                if role == 'teacher':
                    major = request.POST.get('major')
                    if not major:
                        raise ValueError("Major wajib diisi")

                    Teacher.objects.create(
                        user=user,
                        major=major
                    )

                elif role == 'student':
                    grade = request.POST.get('grade')
                    level_id = request.POST.get('level')
                    address = request.POST.get('address')
                    birth = request.POST.get('birth')

                    if not all([grade, level_id, address, birth]):
                        raise ValueError("Semua field student wajib diisi")

                    try:
                        level = Level.objects.get(id=level_id)
                    except Level.DoesNotExist:
                        raise ValueError("Level tidak valid")

                    Student.objects.create(
                        user=user,
                        grade=grade,
                        level=level,  
                        address=address,
                        birth=birth
                    )

                    request.session.pop('placement_level_id', None)
                    request.session.pop('placement_score', None)

                elif role == 'parent':
                    position = request.POST.get('position')
                    if not position:
                        raise ValueError("Position wajib diisi")

                    Parent.objects.create(
                        user=user,
                        position=position
                    )

                else:
                    raise ValueError("Role tidak valid")

                messages.success(request, 'Registrasi berhasil')
                return redirect('login')

            except Exception as e:
                # rollback kalau gagal create role
                user.delete()
                messages.error(request, str(e))

        else:
            messages.error(request, 'Form tidak valid')

    else:
        form = UserCreateForm()

    return render(request, 'auth/register.html', 
                  {
                    'form': form, 
                    'levels' : levels,
                    "auto_level": session_auto_level,
                    "auto_role": "student" if session_auto_level else None
                })

# ▀▄▀▄ update profil user
def profile_update_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = UserUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'auth/profile.html', {'form': form})

# ▀▄▀▄ delete user
def delete_user_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Akun berhasil dihapus')
        return redirect('register')

    return render(request, 'auth/delete_confirm.html')

# ▀▄▀▄ reset password
def reset_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password berhasil direset')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Email tidak ditemukan')

    return render(request, 'auth/reset.html')

# ▀▄▀▄ list user
def user_list(request):
    users = User.objects.select_related(
        'admin', 'teacher', 'parent', 'student'
    ).all().order_by('-id')

    return render(request, 'admin/user.html', {
        'users': users
    })

# ▀▄▀▄ detail user
@login_required
def user_detail(request, id):
    user = get_object_or_404(
        User.objects.select_related(
            'teacher',
            'student__level',   # 🔥 biar level ikut ke-load
            'parent',
            'admin'
        ),
        id=id
    )

    teacher = getattr(user, 'teacher', None)
    student = getattr(user, 'student', None)
    parent = getattr(user, 'parent', None)
    admin_profile = getattr(user, 'admin', None)

    # 🔥 ROLE DETECTION (lebih ringkas)
    role = (
        'Admin' if admin_profile else
        'Teacher' if teacher else
        'Student' if student else
        'Parent' if parent else
        'User'
    )

    return render(request, 'admin/user-detail.html', {
        'user': user,
        'teacher': teacher,
        'student': student,
        'parent': parent,
        'admin_profile': admin_profile,
        'role': role
    })

# ▀▄▀▄ delete user
@login_required
def user_delete(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        try:
            user.delete()
            messages.success(request, f'User "{user.username}" berhasil dihapus')
        except Exception as e:
            messages.error(request, f'Gagal menghapus user: {str(e)}')

        return redirect('admin_user_list')

    messages.warning(request, 'Akses tidak valid')
    return redirect('admin_user_list')

# ▀▄▀▄ menampilkan form UPDATE user
@login_required
def user_update(request): 

    user = request.user 
    admin_profile = getattr(user, "admin", None)
    teacher = getattr(user, "teacher", None)
    parent = getattr(user, "parent", None)
    student = getattr(user, "student", None)

    if request.method == "POST": 
        user_form = UserUpdateForm(
            request.POST,
            request.FILES,
            instance=user,
        ) 
        admin_form = AdminForm(
            request.POST,
            instance=admin_profile,
            prefix="admin",
        ) if admin_profile else None

        teacher_form = TeacherForm(
            request.POST,
            instance=teacher,
            prefix="teacher",
        ) if teacher else None

        parent_form = ParentForm(
            request.POST,
            instance=parent,
            prefix="parent",
        ) if parent else None

        valid = user_form.is_valid()

        if admin_form:
            valid = valid and admin_form.is_valid()

        if teacher_form:
            valid = valid and teacher_form.is_valid()

        if parent_form:
            valid = valid and parent_form.is_valid()

        if valid:

            user_form.save()

            if admin_form:
                admin_form.save()

            if teacher_form:
                teacher_form.save()

            if parent_form:
                parent_form.save()

            messages.success(
                request,
                "Profil berhasil diperbarui."
            )

            return redirect("user_update")

    else:

        user_form = UserUpdateForm(instance=user)

        admin_form = (
            AdminForm(instance=admin_profile, prefix="admin")
            if admin_profile else None
        )

        teacher_form = (
            TeacherForm(instance=teacher, prefix="teacher")
            if teacher else None
        )

        parent_form = (
            ParentForm(instance=parent, prefix="parent")
            if parent else None
        )

    return render(
        request,
        "admin/user-update.html",
        {
            "title": "Profil Saya",

            "user_form": user_form,

            "admin_form": admin_form,
            "teacher_form": teacher_form,
            "parent_form": parent_form,

            "student": student,
        },
    )

# ▀▄▀▄ menampilkan form Hubungan orang tua dan Siswa
@login_required
@transaction.atomic
def student_own_parent(request, student_id):

    student = get_object_or_404(
        Student.objects.select_related("user"),
        user_id=student_id
    )

    if request.method == "POST": 
        form                = StudentParentForm(request.POST) 
        parent_password     = request.POST.get('parent_password') or ''

        if form.is_valid(): 
            mode = form.cleaned_data["mode"] 
            if mode == "existing": 
                student.parent = form.cleaned_data["parent"] 
                user_parent = student.parent.user
            else: 
                email = form.cleaned_data["email"] 
                if User.objects.filter(email=email).exists(): 
                    form.add_error(
                        "email",
                        "Email sudah terdaftar."
                    ) 
                else: 
                    first_name = email.split("@")[0] 
                    user_parent = User.objects.create_user(
                        photo="/user/photos/default.jpg",
                        username=email,
                        email=email,
                        first_name=first_name,
                        password=parent_password,
                    ) 
                    parent = Parent.objects.create(
                        user=user_parent,
                        position=""
                    )
                    student.parent = parent 
                    
            if not form.errors:
                student.save()
                messages.success(
                    request,
                    "Orang tua berhasil dihubungkan."
                ) 
                create_notification(
                        receiver=user_parent,
                        sender=request.user,
                        notification_type=Notification.NotificationType.SYSTEM,
                        title="Hubungan Orang Tua dan Siswa",
                        description=f"Admin telah menghubungkan Anda ke Siswa {student.user.get_full_name()}",
                        path="/"
                    )
                create_notification(
                        receiver=student.user,
                        sender=request.user,
                        notification_type=Notification.NotificationType.SYSTEM,
                        title="Hubungan Orang Tua dan Siswa",
                        description=f"Admin telah menghubungkan Anda ke Orang Tua {user_parent.get_full_name()}",
                        path="/"
                    )
                return redirect(
                    "admin_user_list"
                )
    else:
        form = StudentParentForm(
            initial={
                "mode": "existing",
                "parent": student.parent
            }
        )
    return render(
        request,
        "admin/user-student-own-parent.html",
        {
            "student": student,
            "form": form
        }
    )