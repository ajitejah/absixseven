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

# ▀▄▀▄ Form Level
class LevelForm(forms.ModelForm, StyledFormMixin):

    class Meta:
        model = Level
        fields = [
            "name",
            "description", 
            "icon",
            "minimum_score",
            "maximum_score",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Level Name",
            }),

            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Description",
            }), 

            "icon": forms.TextInput(attrs={
                "placeholder": "fa-solid fa-medal",
            }),



            "minimum_score": forms.NumberInput(attrs={
                "min": 0,
                "placeholder": "0",
                "class": BASE_INPUT_CLASS,
            }),

            "maximum_score": forms.NumberInput(attrs={
                "min": 0,
                "placeholder": "100",
                "class": BASE_INPUT_CLASS,
            }), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

    def clean(self):
        cleaned = super().clean()

        minimum = cleaned.get("minimum_score")
        maximum = cleaned.get("maximum_score")

        if (
            minimum is not None
            and maximum is not None
            and minimum > maximum
        ):
            raise forms.ValidationError(
                "Minimum Score tidak boleh lebih besar dari Maximum Score."
            )

        return cleaned

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

# ▀▄▀▄ Form Update User
class UserUpdateForm(forms.ModelForm, StyledFormMixin):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "gender",
            "photo",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "First Name",
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Last Name",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Email",
            }),
            "gender": forms.Select(attrs={
                "class": BASE_INPUT_CLASS,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

# ▀▄▀▄ Form Admin
class AdminForm(forms.ModelForm, StyledFormMixin):

    class Meta:
        model = Admin
        fields = ["position"]

        widgets = {
            "position": forms.TextInput(attrs={
                "placeholder": "Position",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()


# ▀▄▀▄ Form Teacher
class TeacherForm(forms.ModelForm, StyledFormMixin):

    class Meta:
        model = Teacher
        fields = ["major"]

        widgets = {
            "major": forms.TextInput(attrs={
                "placeholder": "Major",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

# ▀▄▀▄ Form Parent
class ParentForm(forms.ModelForm, StyledFormMixin):

    class Meta:
        model = Parent
        fields = ["position"]

        widgets = {
            "position": forms.TextInput(attrs={
                "placeholder": "Position",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

# ▀▄▀▄ Form Student
class StudentForm(forms.ModelForm, StyledFormMixin):

    class Meta:
        model = Student
        fields = [
            "grade",
            "level",
            "address",
            "birth",
            "parent",
        ]

        widgets = {
            "grade": forms.TextInput(attrs={
                "placeholder": "Grade",
            }),
            "level": forms.Select(attrs={
                "class": BASE_INPUT_CLASS,
            }),
            "address": forms.Textarea(attrs={
                "placeholder": "Address",
                "rows": 3,
            }),
            "birth": forms.DateInput(attrs={
                "type": "date",
                "class": BASE_INPUT_CLASS,
            }),
            "parent": forms.Select(attrs={
                "class": BASE_INPUT_CLASS,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["level"].queryset = Level.objects.all()
        self.fields["level"].empty_label = "Pilih Level"
        self.fields["level"].label_from_instance = (
            lambda obj: f"{obj.name} - {obj.description}"
        )

        self.fields["parent"].queryset = Parent.objects.select_related("user")
        self.fields["parent"].empty_label = "Pilih Orang Tua"

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
            "class": BASE_INPUT_CLASS,
            'style': 'padding-left: 2.5rem;',
        })
    )

    email = forms.EmailField(
        label="Email Orang Tua",
        required=False,
        widget=forms.EmailInput(attrs={
            "placeholder": "Masukkan email orang tua",
            "class": BASE_INPUT_CLASS,
            'style': 'padding-left: 2.5rem;',
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