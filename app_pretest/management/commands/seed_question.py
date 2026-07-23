# app_pretest/management/commands/seed_math_question.py

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
    help = "Seed 20 soal Matematika"

    def handle(self, *args, **kwargs):

        owner = User.objects.get(pk=8)

        lesson, _ = Lesson.objects.get_or_create(
            name="Matematika",
            defaults={
                "description": "Pelajaran Matematika"
            }
        )

        question_set, created = QuestionSet.objects.get_or_create(
            lesson=lesson,
            owner=owner,
            name="Bank Soal Matematika Dasar",
            defaults={
                "description": "20 soal matematika dasar",
                "is_active": True,
            },
        )

        if not created:
            self.stdout.write(
                self.style.WARNING(
                    "Question Set sudah ada. Menghapus soal lama..."
                )
            )

            question_set.questions.all().delete()

        order = 1

        # =====================================================
        # Helper Multiple Choice
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
        # Helper Essay
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
        # Helper Matching
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
        # MULAI SOAL
        # =====================================================

        # lanjut bagian 2...
                # =====================================================
        # 10 MULTIPLE CHOICE
        # =====================================================

        mcq(
            "Hasil dari 25 + 17 adalah ...",
            ["40", "42", "43", "45"],
            "42",
        )

        mcq(
            "12 × 8 = ...",
            ["84", "96", "88", "108"],
            "96",
        )

        mcq(
            "100 ÷ 5 = ...",
            ["25", "15", "20", "10"],
            "20",
        )

        mcq(
            "Bilangan prima di bawah ini adalah ...",
            ["21", "27", "29", "35"],
            "29",
        )

        mcq(
            "3/4 sama dengan ... %",
            ["70", "75", "80", "85"],
            "75",
        )

        mcq(
            "Keliling persegi dengan panjang sisi 8 cm adalah ...",
            ["16 cm", "24 cm", "32 cm", "64 cm"],
            "32 cm",
        )

        mcq(
            "Luas persegi panjang dengan panjang 12 cm dan lebar 5 cm adalah ...",
            ["50 cm²", "55 cm²", "60 cm²", "65 cm²"],
            "60 cm²",
        )

        mcq(
            "Nilai x jika x + 15 = 42 adalah ...",
            ["25", "26", "27", "28"],
            "27",
        )

        mcq(
            "FPB dari 12 dan 18 adalah ...",
            ["4", "6", "8", "12"],
            "6",
        )

        mcq(
            "KPK dari 6 dan 8 adalah ...",
            ["12", "18", "24", "48"],
            "24",
        )

                # =====================================================
        # 5 ESSAY
        # =====================================================

        essay(
            "Jelaskan langkah-langkah mencari FPB dari dua bilangan menggunakan metode faktorisasi prima."
        )

        essay(
            "Hitung luas segitiga yang memiliki alas 12 cm dan tinggi 8 cm. Jelaskan cara perhitungannya."
        )

        essay(
            "Sebutkan minimal empat sifat yang dimiliki oleh bangun datar persegi."
        )

        essay(
            "Hitung hasil dari 345 + 278 dan jelaskan proses penyelesaiannya."
        )

        essay(
            "Apa yang dimaksud dengan pecahan senilai? Berikan dua contoh."
        )

        # =====================================================
        # 5 MATCHING
        # =====================================================

        matching(
            "Cocokkan bangun datar dengan jumlah sisinya.",
            [
                ("Segitiga", "3 sisi"),
                ("Persegi", "4 sisi"),
                ("Segilima", "5 sisi"),
                ("Segienam", "6 sisi"),
            ],
        )

        matching(
            "Cocokkan operasi matematika dengan hasilnya.",
            [
                ("7 × 8", "56"),
                ("9 × 6", "54"),
                ("12 ÷ 3", "4"),
                ("15 + 5", "20"),
            ],
        )

        matching(
            "Cocokkan nama bangun ruang dengan jumlah sisinya.",
            [
                ("Kubus", "6 sisi"),
                ("Balok", "6 sisi"),
                ("Tabung", "3 sisi"),
                ("Kerucut", "2 sisi"),
            ],
        )

        matching(
            "Cocokkan pecahan dengan bentuk desimalnya.",
            [
                ("1/2", "0.5"),
                ("1/4", "0.25"),
                ("3/4", "0.75"),
                ("1/5", "0.2"),
            ],
        )

        matching(
            "Cocokkan satuan panjang berikut.",
            [
                ("1 meter", "100 cm"),
                ("1 kilometer", "1000 meter"),
                ("1 cm", "10 mm"),
                ("1 dm", "10 cm"),
            ],
        )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("=" * 50)
        )
        self.stdout.write(
            self.style.SUCCESS("Seed Matematika berhasil dibuat.")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Lesson       : {lesson.name}")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Question Set : {question_set.name}")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Owner        : {owner}")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Total Soal   : {question_set.questions.count()}")
        )
        self.stdout.write(
            self.style.SUCCESS("=" * 50)
        )