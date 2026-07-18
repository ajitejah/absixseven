from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Level, User, Admin, Teacher, Parent, Student


# =========================
# BASE STYLE (GLOBAL)
# =========================
BASE_INPUT_CLASS = "form-input peer w-full rounded-lg border border-slate-300 bg-transparent px-3 py-2 placeholder:text-slate-400/70"


class StyledFormMixin:
    def apply_style(self):
        for name, field in self.fields.items():
            # skip checkbox/file optional styling berbeda
            if isinstance(field.widget, forms.CheckboxInput):
                continue

            field.widget.attrs.update({
                'class': BASE_INPUT_CLASS
            })

# ▀▄▀▄ form create user
class UserCreateForm(UserCreationForm, StyledFormMixin):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'photo', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter Email'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Enter Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm Password'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

# ▀▄▀▄ form untuk update/preview user
class UserUpdateForm(UserChangeForm, StyledFormMixin):
    password = None

    class Meta:
        model = User
        fields = ['email', 'gender', 'photo']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter Email'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

# ▀▄▀▄ form admin
class AdminForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Admin
        fields = ['position']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

# ▀▄▀▄ form teacher
class TeacherForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Teacher
        fields = ['major']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

# ▀▄▀▄ form parent
class ParentForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Parent
        fields = ['position']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

# ▀▄▀▄ form student
class StudentForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Student
        fields = ['grade', 'level', 'address', 'birth', 'parent']

        widgets = {
            'grade': forms.TextInput(attrs={
                'placeholder': 'Grade'
            }),
            'level': forms.Select(attrs={
                'class': BASE_INPUT_CLASS
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Address',
                'rows': 3
            }),
            'birth': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASS
            }),
            'parent': forms.Select(attrs={
                'class': BASE_INPUT_CLASS
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 OPTIMASI: ambil level dari database
        self.fields['level'].queryset = Level.objects.all()

        # 🔥 OPTIONAL: label kosong
        self.fields['level'].empty_label = "Pilih Level"

        # 🔥 OPTIONAL: tampilkan name + description
        self.fields['level'].label_from_instance = lambda obj: f"{obj.name} - {obj.description}"

        self.apply_style()

# ▀▄▀▄ form student parent
class StudentParentForm(forms.Form, StyledFormMixin):

    mode = forms.CharField(
        initial="existing",
        widget=forms.HiddenInput()
    )

    parent = forms.ModelChoiceField(
        label="Orang Tua Terdaftar",
        queryset=Parent.objects.none(),
        required=False,
        empty_label="Pilih Orang Tua",
        widget=forms.Select(attrs={
            "class": BASE_INPUT_CLASS
        })
    )

    email = forms.EmailField(
        label="Email Orang Tua",
        required=False,
        widget=forms.EmailInput(attrs={
            "placeholder": "Masukkan email orang tua",
            "class": BASE_INPUT_CLASS
        })
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["parent"].queryset = (
            Parent.objects
            .select_related("user")
            .order_by("user__first_name", "user__last_name")
        )

        self.fields["parent"].label_from_instance = (
            lambda obj:
            obj.user.get_full_name()
            if obj.user.get_full_name()
            else obj.user.email
        )

        self.apply_style()

    def clean(self):

        cleaned = super().clean()

        mode = cleaned.get("mode")

        if mode == "existing":

            if not cleaned.get("parent"):
                self.add_error(
                    "parent",
                    "Silakan pilih orang tua."
                )

        elif mode == "create":

            if not cleaned.get("email"):
                self.add_error(
                    "email",
                    "Email wajib diisi."
                )

        return cleaned