from django import forms

from .models import Lesson, QuestionSet


class LessonForm(forms.ModelForm):

    class Meta:
        model = Lesson

        fields = [
            "name",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input w-full ml-4",
                    'style': 'padding-left: 2.5rem;',
                    "placeholder": "Masukkan nama pelajaran",
                    "maxlength": 255,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-textarea w-full",
                    'style': 'padding-left: 2.5rem;',
                    "placeholder": "Deskripsi pelajaran (opsional)",
                    "rows": 4,
                }
            ),
        }

        labels = {
            "name": "Lesson",
            "description": "Description",
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        queryset = Lesson.objects.filter(name__iexact=name)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError("Lesson sudah ada.")

        return name
    

class QuestionSetForm(forms.ModelForm):

    class Meta:
        model = QuestionSet

        fields = [
            "lesson",
            "name",
            "description",
            "is_active",
        ]

        widgets = {
            "lesson": forms.Select(
                attrs={
                    "class": "form-select w-full",
                    'style': 'padding-left: 2.5rem;',
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-input w-full",
                    'style': 'padding-left: 2.5rem;',
                    "placeholder": "Masukkan nama Question Set",
                    "maxlength": 255,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-textarea w-full",
                    'style': 'padding-left: 2.5rem;',
                    "placeholder": "Deskripsi Question Set (opsional)",
                    "rows": 4,
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    'style': 'padding-left: 2.5rem;',
                    "class": "form-checkbox h-5 w-5 rounded border-slate-400",
                }
            ),
        }

        labels = {
            "lesson": "Lesson",
            "name": "Question Set",
            "description": "Description",
            "is_active": "Active",
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        queryset = QuestionSet.objects.filter(
            lesson=self.cleaned_data["lesson"],
            name__iexact=name,
        )

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(
                "Question Set dengan nama tersebut sudah ada pada Lesson ini."
            )

        return name