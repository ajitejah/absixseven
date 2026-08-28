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
    help = "Seed 20 soal Biologi"

    def handle(self, *args, **kwargs):

        # =====================================================
        # OWNER
        # =====================================================

        owner = User.objects.get(pk=8)

        # =====================================================
        # LESSON
        # =====================================================

        lesson, _ = Lesson.objects.get_or_create(
            name="Biologi",
            defaults={
                "description": "Pelajaran Biologi",
            }
        )

        # =====================================================
        # QUESTION SET
        # =====================================================

        question_set, created = QuestionSet.objects.get_or_create(
            lesson=lesson,
            owner=owner,
            name="QS Biology Dasar",
            defaults={
                "description": "20 soal biologi dasar",
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
            "Organel sel yang berfungsi sebagai tempat berlangsungnya respirasi sel adalah ...",
            [
                "Nukleus",
                "Mitokondria",
                "Ribosom",
                "Lisosom",
            ],
            "Mitokondria",
        )

        mcq(
            "Proses fotosintesis pada tumbuhan terutama berlangsung di organel ...",
            [
                "Mitokondria",
                "Kloroplas",
                "Nukleus",
                "Vakuola",
            ],
            "Kloroplas",
        )

        mcq(
            "Bagian sel yang berfungsi mengatur seluruh aktivitas sel adalah ...",
            [
                "Membran sel",
                "Sitoplasma",
                "Nukleus",
                "Dinding sel",
            ],
            "Nukleus",
        )

        mcq(
            "Zat hijau daun yang berperan penting dalam proses fotosintesis disebut ...",
            [
                "Hemoglobin",
                "Klorofil",
                "Melanin",
                "Keratin",
            ],
            "Klorofil",
        )

        mcq(
            "Organ pernapasan utama pada manusia adalah ...",
            [
                "Jantung",
                "Paru-paru",
                "Lambung",
                "Ginjal",
            ],
            "Paru-paru",
        )

        mcq(
            "Pembuluh darah yang membawa darah keluar dari jantung disebut ...",
            [
                "Vena",
                "Arteri",
                "Kapiler",
                "Venula",
            ],
            "Arteri",
        )

        mcq(
            "Unit struktural dan fungsional terkecil penyusun makhluk hidup adalah ...",
            [
                "Jaringan",
                "Organ",
                "Sel",
                "Sistem organ",
            ],
            "Sel",
        )

        mcq(
            "Hasil utama proses fotosintesis yang digunakan tumbuhan sebagai sumber energi adalah ...",
            [
                "Protein",
                "Glukosa",
                "Lemak",
                "Vitamin",
            ],
            "Glukosa",
        )

        mcq(
            "Jaringan tumbuhan yang berfungsi mengangkut air dan mineral dari akar ke daun adalah ...",
            [
                "Floem",
                "Xilem",
                "Epidermis",
                "Parenkim",
            ],
            "Xilem",
        )

        mcq(
            "Organ yang berfungsi menyaring darah dan menghasilkan urine adalah ...",
            [
                "Hati",
                "Jantung",
                "Ginjal",
                "Paru-paru",
            ],
            "Ginjal",
        )

        # =====================================================
        # 5 ESSAY
        # =====================================================

        essay(
            "Jelaskan pengertian sel dan mengapa sel disebut sebagai unit struktural dan fungsional terkecil makhluk hidup."
        )

        essay(
            "Jelaskan proses fotosintesis pada tumbuhan serta bahan-bahan yang diperlukan dalam proses tersebut."
        )

        essay(
            "Jelaskan perbedaan fungsi pembuluh xilem dan floem pada tumbuhan."
        )

        essay(
            "Jelaskan fungsi jantung dan bagaimana darah diedarkan ke seluruh tubuh manusia."
        )

        essay(
            "Jelaskan hubungan antara sistem pernapasan dan sistem peredaran darah dalam memenuhi kebutuhan oksigen tubuh."
        )

        # =====================================================
        # 5 MATCHING
        # =====================================================

        matching(
            "Cocokkan organel sel dengan fungsi yang tepat.",
            [
                ("Nukleus", "Mengatur aktivitas sel"),
                ("Mitokondria", "Menghasilkan energi"),
                ("Ribosom", "Sintesis protein"),
                ("Kloroplas", "Tempat fotosintesis"),
            ],
        )

        matching(
            "Cocokkan organ tubuh manusia dengan fungsinya.",
            [
                ("Jantung", "Memompa darah"),
                ("Paru-paru", "Pertukaran gas"),
                ("Ginjal", "Menyaring darah"),
                ("Lambung", "Mencerna makanan"),
            ],
        )

        matching(
            "Cocokkan bagian tumbuhan dengan fungsi yang tepat.",
            [
                ("Akar", "Menyerap air dan mineral"),
                ("Batang", "Menopang dan mengangkut zat"),
                ("Daun", "Tempat utama fotosintesis"),
                ("Bunga", "Alat reproduksi"),
            ],
        )

        matching(
            "Cocokkan jenis jaringan tumbuhan dengan fungsinya.",
            [
                ("Xilem", "Mengangkut air dan mineral"),
                ("Floem", "Mengangkut hasil fotosintesis"),
                ("Epidermis", "Melindungi permukaan tumbuhan"),
                ("Meristem", "Tempat pertumbuhan"),
            ],
        )

        matching(
            "Cocokkan sistem organ manusia dengan fungsi utamanya.",
            [
                ("Sistem pencernaan", "Mencerna makanan"),
                ("Sistem pernapasan", "Pertukaran oksigen dan karbon dioksida"),
                ("Sistem peredaran darah", "Mengedarkan zat ke seluruh tubuh"),
                ("Sistem ekskresi", "Mengeluarkan zat sisa"),
            ],
        )

        # =====================================================
        # INFORMASI HASIL SEED
        # =====================================================

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS("=" * 50)
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Seed Biologi berhasil dibuat."
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