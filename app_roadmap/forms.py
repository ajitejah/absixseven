from django import forms
from .models import Roadmap, Node, Assignment, Submission


# ▀▄▀▄ base style
BASE_INPUT_CLASS    = "form-input w-full rounded-lg border border-slate-300 px-3 py-2 pl-4"
CHECKBOX_CLASS      = "form-checkbox is-outline size-5 rounded-full  bg-white border-slate-400/70 before:bg-primary checked:border-primary hover:border-primary focus:border-primary dark:border-navy-400 dark:before:bg-accent dark:checked:border-accent dark:hover:border-accent dark:focus:border-accent"

# ▀▄▀▄ roadmap form
class RoadmapForm(forms.ModelForm):
    class Meta:
        model = Roadmap
        fields = [
            'name', 'description', 'cover', 'level',
            'release', 'expired', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASS,
                'style': 'padding-left: 2.5rem;',
                'placeholder': 'Nama roadmap'
            }),
            'description': forms.Textarea(attrs={
                'class': BASE_INPUT_CLASS,
                'rows': 3,
                'placeholder': 'Deskripsi roadmap'
            }),
            'level': forms.Select(attrs={
                'class': BASE_INPUT_CLASS
            }),
            'release': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': BASE_INPUT_CLASS
            }),
            'expired': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': BASE_INPUT_CLASS
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': CHECKBOX_CLASS
            })
        }

    def save(self, commit=True):
        roadmap = super().save(commit=False)

        if not roadmap.cover:
            roadmap.cover = 'user/photos/default.jpg'

        if commit:
            roadmap.save()

        return roadmap

# ▀▄▀▄ node form
class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = [
            'roadmap', 'name', 'description',
            'duration', 'is_locked'
        ]
        widgets = {
            'roadmap': forms.Select(attrs={
                'class': BASE_INPUT_CLASS
            }),
            'name': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Nama node'
            }),
            'description': forms.Textarea(attrs={
                'class': BASE_INPUT_CLASS,
                'rows': 3
            }),
            'duration': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Menit'
            }),
            'is_locked': forms.CheckboxInput(attrs={
                'class': 'form-switch h-5 w-10 rounded-full bg-slate-300 before:rounded-full before:bg-slate-50 checked:!bg-success checked:before:bg-white dark:bg-navy-900 dark:before:bg-navy-300 dark:checked:before:bg-white'
            })
        }

# ▀▄▀▄ assignment form
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'title', 'description',
            'attachment', 'duration',
            'release', 'expired', 'is_active'
        ]
        widgets = { 
            'title': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Judul tugas'
            }),
            'description': forms.Textarea(attrs={
                'class': BASE_INPUT_CLASS,
                'rows': 3
            }),
            'duration': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASS
            }),
            'release': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': BASE_INPUT_CLASS
            }),
            'expired': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': BASE_INPUT_CLASS
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }

# ▀▄▀▄ submission form
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': BASE_INPUT_CLASS
            })
        }

# ▀▄▀▄ scoring form
class SubmissionScoreForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Nilai'
            }),
            'feedback': forms.Textarea(attrs={
                'class': BASE_INPUT_CLASS,
                'rows': 3,
                'placeholder': 'Feedback'
            })
        }