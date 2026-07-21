from django import forms

from .models import Lesson


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
                    "placeholder": "Masukkan nama pelajaran",
                    "maxlength": 255,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-textarea w-full",
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