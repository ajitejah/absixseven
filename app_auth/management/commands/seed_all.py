from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone

from app_auth.models import User, Student, Teacher, Parent, Admin, Level
from app_roadmap.models import Roadmap, Node, Assignment, StudentProgress, Submission
from app_scoring.models import Evaluation, Score
from app_screening.models import PlacementQuestion, PlacementOption

fake = Faker()

class Command(BaseCommand):
    help = "Seed all LMS data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding started...")

        User.objects.filter(is_superuser=False).delete() 
        
        
        # =========================
        # 1. LEVEL
        # =========================
        levels = []
        for i in range(3):
            lvl = Level.objects.create(
                name=f"Level {i+1}",
                description=fake.text(),
                icon="fa-star"
            )
            levels.append(lvl)

        # =========================
        # 2. USERS
        # =========================
        students = []
        teachers = []
        parents = []

        for i in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.unique.email(),
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

            role = random.choice(["student", "teacher", "parent", "admin"])

            if role == "student":
                student = Student.objects.create(
                    user=user,
                    grade=str(random.randint(1, 12)),
                    address=fake.address(),
                    birth=fake.date_of_birth(),
                    level=random.choice(levels),
                )
                students.append(student)

            elif role == "teacher":
                teacher = Teacher.objects.create(
                    user=user,
                    major=fake.job()
                )
                teachers.append(teacher)

            elif role == "parent":
                parent = Parent.objects.create(
                    user=user,
                    position=fake.job()
                )
                parents.append(parent)

            else:
                Admin.objects.create(
                    user=user,
                    position="Admin"
                )

        # =========================
        # 3. ROADMAP
        # =========================
        roadmaps = []
        for i in range(3):
            roadmap = Roadmap.objects.create(
                name=fake.sentence(nb_words=3),
                description=fake.text(),
                level=random.choice(levels),
                owner=random.choice([t.user for t in teachers]) if teachers else None,
                is_active=True
            )
            roadmaps.append(roadmap)

        # =========================
        # 4. NODE
        # =========================
        nodes = []
        for roadmap in roadmaps:
            for i in range(5):
                node = Node.objects.create(
                    roadmap=roadmap,
                    name=f"Node {i+1}",
                    description=fake.text(),
                    order=i + 1,
                    duration=random.randint(10, 60),
                    is_locked=False
                )
                nodes.append(node)

        # =========================
        # 5. ASSIGNMENT
        # =========================
        assignments = []
        for node in nodes:
            for i in range(2):
                a = Assignment.objects.create(
                    node=node,
                    title=fake.sentence(nb_words=4),
                    description=fake.text(),
                    duration=random.randint(10, 90),
                    release=timezone.now(),
                    expired=None,
                    is_active=True
                )
                assignments.append(a)

        # =========================
        # 6. STUDENT PROGRESS
        # =========================
        for student in students:
            for node in nodes:
                StudentProgress.objects.get_or_create(
                    student=student,
                    node=node,
                    defaults={
                        "is_completed": random.choice([True, False]),
                        "completed_at": timezone.now() if random.choice([True, False]) else None
                    }
                )

        # =========================
        # 7. SUBMISSION
        # =========================
        submissions = []
        for student in students:
            for assignment in assignments:
                sub = Submission.objects.create(
                    student=student,
                    assignment=assignment,
                    score=random.uniform(60, 100),
                    feedback=fake.sentence()
                )
                submissions.append(sub)

        # =========================
        # 8. EVALUATION
        # =========================
        evaluations = []
        for student in students:
            for roadmap in roadmaps:
                eval_obj = Evaluation.objects.create(
                    student=student,
                    roadmap=roadmap,
                    average=random.uniform(60, 100),
                    progress=random.uniform(0, 100),
                    rank=random.randint(1, 50),
                    predict=random.uniform(60, 100),
                    confirmed=random.choice([True, False])
                )
                evaluations.append(eval_obj)

        # =========================
        # 9. SCORE
        # =========================
        for eval_obj in evaluations:
            student = eval_obj.student

            student_submissions = Submission.objects.filter(student=student)

            for sub in student_submissions:
                Score.objects.create(
                    evaluation=eval_obj,
                    submission=sub,
                    assignment=sub.assignment,
                    score=sub.score,
                    feedback=sub.feedback
                )

            # update average
            eval_obj.update_average()

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))

        

        self.stdout.write("Seeding Placement Questions...")

        PlacementOption.objects.all().delete()
        PlacementQuestion.objects.all().delete()

        questions = [

            {
                "question": "Ibukota Indonesia adalah?",
                "options": [
                    ("Jakarta", 10),
                    ("Bandung", 0),
                    ("Surabaya", 0),
                    ("Medan", 0),
                ]
            },

            {
                "question": "2 + 3 × 4 = ?",
                "options": [
                    ("14", 10),
                    ("20", 0),
                    ("24", 0),
                    ("10", 0),
                ]
            },

            {
                "question": "Planet terbesar di tata surya adalah?",
                "options": [
                    ("Jupiter", 10),
                    ("Mars", 0),
                    ("Venus", 0),
                    ("Bumi", 0),
                ]
            },

            {
                "question": "Siapa proklamator Indonesia?",
                "options": [
                    ("Soekarno dan Mohammad Hatta", 10),
                    ("Soeharto dan Habibie", 0),
                    ("Jenderal Sudirman dan Soekarno", 0),
                    ("Kartini dan Hatta", 0),
                ]
            },

            {
                "question": "Bahasa Inggris dari kata 'Buku' adalah?",
                "options": [
                    ("Book", 10),
                    ("Pen", 0),
                    ("Table", 0),
                    ("Chair", 0),
                ]
            },

            {
                "question": "Organ tubuh yang berfungsi memompa darah adalah?",
                "options": [
                    ("Jantung", 10),
                    ("Paru-paru", 0),
                    ("Hati", 0),
                    ("Ginjal", 0),
                ]
            },

            {
                "question": "75% sama dengan pecahan?",
                "options": [
                    ("3/4", 10),
                    ("1/2", 0),
                    ("1/4", 0),
                    ("2/3", 0),
                ]
            },

            {
                "question": "Benua terbesar di dunia adalah?",
                "options": [
                    ("Asia", 10),
                    ("Afrika", 0),
                    ("Eropa", 0),
                    ("Amerika", 0),
                ]
            },

            {
                "question": "Siapa penemu lampu pijar?",
                "options": [
                    ("Thomas Edison", 10),
                    ("Albert Einstein", 0),
                    ("Isaac Newton", 0),
                    ("Nikola Tesla", 0),
                ]
            },

            {
                "question": "Hasil dari 12² adalah?",
                "options": [
                    ("144", 10),
                    ("124", 0),
                    ("132", 0),
                    ("164", 0),
                ]
            },

            {
                "question": "Gas yang paling banyak terdapat di atmosfer bumi adalah?",
                "options": [
                    ("Nitrogen", 10),
                    ("Oksigen", 0),
                    ("Karbon Dioksida", 0),
                    ("Helium", 0),
                ]
            },

            {
                "question": "Apa kepanjangan dari CPU?",
                "options": [
                    ("Central Processing Unit", 10),
                    ("Central Program Unit", 0),
                    ("Computer Process Unit", 0),
                    ("Computer Program Utility", 0),
                ]
            },

            {
                "question": "Jika semua A adalah B dan semua B adalah C, maka?",
                "options": [
                    ("Semua A adalah C", 10),
                    ("Semua C adalah A", 0),
                    ("Sebagian A adalah C", 0),
                    ("Tidak dapat ditentukan", 0),
                ]
            },

            {
                "question": "Hari Kemerdekaan Indonesia diperingati setiap tanggal?",
                "options": [
                    ("17 Agustus", 10),
                    ("1 Juni", 0),
                    ("28 Oktober", 0),
                    ("10 November", 0),
                ]
            },

            {
                "question": "Negara dengan jumlah penduduk terbanyak di dunia saat ini adalah?",
                "options": [
                    ("India", 10),
                    ("China", 0),
                    ("Amerika Serikat", 0),
                    ("Indonesia", 0),
                ]
            },

        ]

        for q_order, item in enumerate(questions, start=1):

            question = PlacementQuestion.objects.create(
                question=item["question"],
                order=q_order,
                is_active=True
            )

            for o_order, (answer, score) in enumerate(item["options"], start=1):

                PlacementOption.objects.create(
                    question=question,
                    answer=answer,
                    score=score,
                    order=o_order
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {PlacementQuestion.objects.count()} questions and {PlacementOption.objects.count()} options"
            )
        )