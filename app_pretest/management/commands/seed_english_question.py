
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from app_pretest.models import (
    Lesson,
    QuestionSet,
    Question,
    ChoiceOption,
    MatchingPair,
)

User = get_user_model()


class Command(BaseCommand):

    help = "Seed 20 soal Bahasa Inggris"

    def handle(self, *args, **kwargs):

        # =====================================================
        # OWNER
        # =====================================================

        owner = User.objects.get(pk=8)

        # =====================================================
        # LESSON
        # =====================================================

        lesson, _ = Lesson.objects.get_or_create(
            name="Bahasa Inggris",
            defaults={
                "description": "Pelajaran Bahasa Inggris"
            }
        )

        # =====================================================
        # QUESTION SET
        # =====================================================

        question_set, created = QuestionSet.objects.get_or_create(
            lesson=lesson,
            owner=owner,
            name="Bank Soal Bahasa Inggris Dasar",
            defaults={
                "description": "20 soal Bahasa Inggris dasar",
                "is_active": True,
            },
        )

        # =====================================================
        # HAPUS SOAL LAMA
        # =====================================================

        if not created:

            self.stdout.write(
                self.style.WARNING(
                    "Question Set sudah ada. Menghapus soal lama..."
                )
            )

            question_set.questions.all().delete()

        order = 1

        # =====================================================
        # HELPER MULTIPLE CHOICE
        # =====================================================

        def mcq(question_text, options, correct):

            nonlocal order

            q = Question.objects.create(
                question_set=question_set,
                question_type=Question.Type.MULTIPLE_CHOICE,
                question=question_text,
                point=1,
                order=order,
                required=True,
            )

            for i, option in enumerate(options, start=1):

                ChoiceOption.objects.create(
                    question=q,
                    option=option,
                    is_correct=(option == correct),
                    order=i,
                )

            order += 1

        # =====================================================
        # HELPER ESSAY
        # =====================================================

        def essay(question_text):

            nonlocal order

            Question.objects.create(
                question_set=question_set,
                question_type=Question.Type.ESSAY,
                question=question_text,
                point=5,
                order=order,
                required=True,
            )

            order += 1

        # =====================================================
        # HELPER MATCHING
        # =====================================================

        def matching(question_text, pairs):

            nonlocal order

            q = Question.objects.create(
                question_set=question_set,
                question_type=Question.Type.MATCHING,
                question=question_text,
                point=4,
                order=order,
                required=True,
            )

            for i, pair in enumerate(pairs, start=1):

                MatchingPair.objects.create(
                    question=q,
                    left_text=pair[0],
                    right_text=pair[1],
                    order=i,
                )

            order += 1

        # =====================================================
        # 10 MULTIPLE CHOICE
        # =====================================================

        mcq(
            "Choose the correct greeting.",
            [
                "Good morning",
                "Good night",
                "Goodbye",
                "See you",
            ],
            "Good morning",
        )

        mcq(
            "What is the plural form of 'child'?",
            [
                "Childs",
                "Childes",
                "Children",
                "Childrens",
            ],
            "Children",
        )

        mcq(
            "She ___ a student.",
            [
                "am",
                "is",
                "are",
                "be",
            ],
            "is",
        )

        mcq(
            "They ___ football every Sunday.",
            [
                "plays",
                "play",
                "playing",
                "played",
            ],
            "play",
        )

        mcq(
            "The opposite of 'big' is ...",
            [
                "Tall",
                "Small",
                "Long",
                "Heavy",
            ],
            "Small",
        )

        mcq(
            "I have ___ apple.",
            [
                "a",
                "an",
                "the",
                "some",
            ],
            "an",
        )

        mcq(
            "Which one is a color?",
            [
                "Blue",
                "Table",
                "Chair",
                "Book",
            ],
            "Blue",
        )

        mcq(
            "What does 'library' mean?",
            [
                "Rumah sakit",
                "Perpustakaan",
                "Sekolah",
                "Pasar",
            ],
            "Perpustakaan",
        )

        mcq(
            "We use our eyes to ...",
            [
                "Hear",
                "Smell",
                "See",
                "Taste",
            ],
            "See",
        )

        mcq(
            "Which sentence is correct?",
            [
                "He go to school.",
                "He goes to school.",
                "He going to school.",
                "He gone to school.",
            ],
            "He goes to school.",
        )

        # =====================================================
        # 5 ESSAY
        # =====================================================

        essay(
            "Introduce yourself in English using at least five sentences."
        )

        essay(
            "Write a short paragraph about your favorite hobby in English."
        )

        essay(
            "Describe your school using simple English sentences."
        )

        essay(
            "Write five daily activities that you usually do from morning until evening."
        )

        essay(
            "Explain why learning English is important for students."
        )

        # =====================================================
        # 5 MATCHING
        # =====================================================

        matching(
            "Match the English words with their Indonesian meanings.",
            [
                ("Book", "Buku"),
                ("Table", "Meja"),
                ("Chair", "Kursi"),
                ("Door", "Pintu"),
            ],
        )

        matching(
            "Match the pronouns with their meanings.",
            [
                ("I", "Saya"),
                ("You", "Kamu"),
                ("We", "Kami/Kita"),
                ("They", "Mereka"),
            ],
        )

        matching(
            "Match the animals with their Indonesian names.",
            [
                ("Cat", "Kucing"),
                ("Dog", "Anjing"),
                ("Bird", "Burung"),
                ("Fish", "Ikan"),
            ],
        )

        matching(
            "Match the days with their Indonesian names.",
            [
                ("Monday", "Senin"),
                ("Tuesday", "Selasa"),
                ("Wednesday", "Rabu"),
                ("Thursday", "Kamis"),
            ],
        )

        matching(
            "Match the occupations with their meanings.",
            [
                ("Teacher", "Guru"),
                ("Doctor", "Dokter"),
                ("Farmer", "Petani"),
                ("Police", "Polisi"),
            ],
        )

        # =====================================================
        # INFORMASI HASIL
        # =====================================================

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS("=" * 50)
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Seed Bahasa Inggris berhasil dibuat."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Lesson       : {lesson.name}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Question Set : {question_set.name}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Owner        : {owner}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total Soal   : {question_set.questions.count()}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS("=" * 50)
        )