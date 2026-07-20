from django.db import models
from app_auth.models import Student, User

# ==========================================
# LESSON
# ========================================== 
class Lesson(models.Model): 
    name            = models.CharField(max_length=255) 
    description     = models.TextField(blank=True)    
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
 
    def __str__(self):
        return self.name

# ==========================================
# QUESTION SET
# ========================================== 
class QuestionSet(models.Model):
    lesson      = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="question_sets")
    owner       = models.ForeignKey( User, on_delete=models.CASCADE, related_name="question_sets" )
    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.lesson.name} - {self.name}"
    
# ==========================================
# PRETEST
# ========================================== 

class Pretest(models.Model):

    class Type(models.TextChoices):
        PRETEST = "PRETEST", "Pretest"
        POSTTEST = "POSTTEST", "Posttest"

    title           = models.CharField(max_length=255) 
    description     = models.TextField(blank=True) 
    pretest_type    = models.CharField(max_length=20, choices=Type.choices, default=Type.PRETEST)
    question_set    = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="pretests" )
    question_count  = models.PositiveIntegerField(default=20, help_text="Jumlah soal yang diambil secara acak.")
    duration        = models.PositiveIntegerField(default=30, help_text="Durasi (menit)")
    release         = models.DateTimeField(null=True, blank=True)
    expired         = models.DateTimeField(null=True, blank=True)
    random_question = models.BooleanField(default=True)
    random_option   = models.BooleanField(default=True)
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
     
    
# ==========================================
# QUESTION
# ========================================== 
class Question(models.Model):

    class Type(models.TextChoices):
        MULTIPLE_CHOICE = "MCQ", "Multiple Choice"
        ESSAY           = "ESSAY", "Essay"
        MATCHING        = "MATCHING", "Matching"

    question_set    = models.ForeignKey( QuestionSet, on_delete=models.CASCADE, related_name="questions" )
    question_type   = models.CharField(max_length=20, choices=Type.choices)  
    question        = models.TextField()
    attachment      = models.FileField(upload_to="pretest/question/", blank=True, null=True)
    point           = models.FloatField(default=1)
    order           = models.PositiveIntegerField(default=1)
    required        = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            "order",
            "id"
        ]

    def __str__(self):
        return self.question[:60]


# ==========================================
# MULTIPLE CHOICE OPTION
# ========================================== 
class ChoiceOption(models.Model): 
    question    = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    option      = models.CharField(max_length=255)
    is_correct  = models.BooleanField(default=False)
    order       = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.option

# ==========================================
# MATCHING PAIR
# ========================================== 
class MatchingPair(models.Model):
    question    = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="pairs")
    left_text   = models.CharField(max_length=255)
    right_text  = models.CharField(max_length=255)
    order       = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.left_text

# ==========================================
# STUDENT ATTEMPT
# ========================================== 
class Attempt(models.Model): 
    class Status(models.TextChoices):
        DRAFT       = "DRAFT", "Draft"
        SUBMITTED   = "SUBMITTED", "Submitted"
        SCORED      = "SCORED", "Scored"

    pretest         = models.ForeignKey(Pretest, on_delete=models.CASCADE, related_name="attempts")
    student         = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="pretest_attempts")
    total_question  = models.PositiveIntegerField(default=0) 
    correct_answer  = models.PositiveIntegerField(default=0) 
    wrong_answer    = models.PositiveIntegerField(default=0) 
    blank_answer    = models.PositiveIntegerField(default=0)
    duration        = models.PositiveIntegerField(default=0)
    score           = models.FloatField(default=0)
    status          = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    started_at      = models.DateTimeField(auto_now_add=True)
    submitted_at    = models.DateTimeField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "pretest",
            "student",
        )

    def __str__(self):
        return f"{self.student.user.first_name} - {self.pretest.title}"


# ==========================================
# STUDENT ANSWER
# ========================================== 
class Answer(models.Model): 
    attempt         = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name="answers")
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)

    # =========================
    # Multiple Choice
    # =========================
    selected_option = models.ForeignKey(ChoiceOption, on_delete=models.SET_NULL, null=True, blank=True)

    # =========================
    # Essay
    # =========================
    essay_answer    = models.TextField(blank=True)

    # =========================
    # Matching
    # Disimpan dalam format JSON
    # contoh:
    # {
    #   "1":"3",
    #   "2":"1",
    #   "3":"2"
    # }
    # =========================

    matching_answer = models.JSONField(null=True,blank=True)
    score           = models.FloatField(default=0)
    is_correct      = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "attempt",
            "question",
        )

    def __str__(self):
        return f"{self.attempt.student.user.first_name} - {self.question.id}"