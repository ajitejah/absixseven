from django import forms
from .models import ChoiceOption, Lesson, MatchingPair, Question, QuestionSet 
from django.forms import inlineformset_factory

# ▀▄▀▄ form lesson/mapel
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
    
# ▀▄▀▄ form question set/paket soal
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
    
# ▀▄▀▄ form question
class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question

        fields = [
            "question_type",
            "question",
            "attachment",
            "point",
            "order",
            "required",
        ]

        widgets = {

            "question_type": forms.Select(
                attrs={
                    "class": "form-select w-full",
                    "style": "padding-left:2.5rem;",
                }
            ),

            "question": forms.Textarea(
                attrs={
                    "class": "form-textarea w-full",
                    "placeholder": "Masukkan pertanyaan",
                    "rows": 4,
                }
            ),

            "attachment": forms.ClearableFileInput(
                attrs={
                    "class": "form-input w-full",
                }
            ),

            "point": forms.NumberInput(
                attrs={
                    "class": "form-input w-full",
                    "style": "padding-left:2.5rem;",
                    "min": 0,
                    "step": 0.5,
                }
            ),

            "order": forms.NumberInput(
                attrs={
                    "class": "form-input w-full",
                    "style": "padding-left:2.5rem;",
                    "min": 1,
                }
            ),

            "required": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox h-5 w-5 rounded border-slate-400",
                }
            ),
        }

        labels = {
            "question_type": "Jenis Soal",
            "question": "Pertanyaan",
            "attachment": "Lampiran",
            "point": "Point",
            "order": "Urutan",
            "required": "Wajib Dijawab",
        }


# ▀▄▀▄ form untuk jenis question: choice option
class ChoiceOptionForm(forms.ModelForm):

    class Meta:
        model = ChoiceOption

        fields = [
            "option",
            "is_correct",
            "order",
        ]

        widgets = {

            "option": forms.TextInput(
                attrs={
                    "class": "form-input w-full",
                    "placeholder": "Pilihan jawaban",
                }
            ),

            "is_correct": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox h-5 w-5 rounded border-slate-400",
                }
            ),

            "order": forms.NumberInput(
                attrs={
                    "class": "form-input w-24",
                    "min": 1,
                }
            ),
        }


# ▀▄▀▄ form untuk jenis question: matching
class MatchingPairForm(forms.ModelForm):

    class Meta:
        model = MatchingPair

        fields = [
            "left_text",
            "right_text",
            "order",
        ]

        widgets = {

            "left_text": forms.TextInput(
                attrs={
                    "class": "form-input w-full",
                    "placeholder": "Kolom kiri",
                }
            ),

            "right_text": forms.TextInput(
                attrs={
                    "class": "form-input w-full",
                    "placeholder": "Kolom kanan",
                }
            ),

            "order": forms.NumberInput(
                attrs={
                    "class": "form-input w-24",
                    "min": 1,
                }
            ),
        }

ChoiceOptionFormSet = inlineformset_factory(
    Question,
    ChoiceOption,
    form=ChoiceOptionForm,
    extra=4,
    min_num=2,
    validate_min=True,
    can_delete=True,
)

MatchingPairFormSet = inlineformset_factory(
    Question,
    MatchingPair,
    form=MatchingPairForm,
    extra=4,
    min_num=2,
    validate_min=True,
    can_delete=True,
)