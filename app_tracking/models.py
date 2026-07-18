from django.db import models

from app_auth.models import Student, Teacher
from app_roadmap.models import Assignment

# ==========================================================
# TRACKING RULE
# ==========================================================
class Rule(models.Model):

    name = models.CharField(max_length=100, default="Tracking Rule")
    minimum_score = models.PositiveIntegerField(default=75)

    # Hari guru melakukan evaluasi
    day_to_evaluate     = models.JSONField(default=list, blank=True)
    start_time_to_evaluate    = models.TimeField(null=True, blank=True)
    end_time_to_evaluate    = models.TimeField(null=True, blank=True)
    
    # Hari guru memberikan tugas recovery/remedial
    day_to_serve    = models.JSONField(default=list, blank=True)
    start_time_to_serve   = models.TimeField(null=True,blank=True)
    end_time_to_serve   = models.TimeField(null=True,blank=True)

    # Hari siswa boleh memperbaiki tugas
    day_to_work     = models.JSONField(default=list,blank=True)
    start_time_to_work    = models.TimeField(null=True, blank=True)
    end_time_to_work    = models.TimeField(null=True, blank=True)

    # Hari siswa boleh memperbaiki tugas
    day_to_correct  = models.JSONField(default=list,blank=True)
    start_time_to_correct = models.TimeField(null=True, blank=True)
    end_time_to_correct = models.TimeField(null=True, blank=True)

    # Maksimum tugas yang diberikan
    limit_assignment = models.PositiveIntegerField(default=60)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


# ==========================================================
# TRACKING Foul/Pelanggaran Yang DIlakukan Siswa
# ==========================================================

class Foul(models.Model):

    class Type(models.TextChoices):
        ABSENT          = "ABSENT", "Absent" # geser jadwal tugas
        NOT_SUBMITTED   = "NOT_SUBMITTED", "Not Submitted" # geser jadwal tugas
        LOW_SCORE       = "LOW_SCORE", "Low Score" # dibuatkan soal remedial
        LATE_SUBMISSION = "LATE_SUBMISSION", "Late Submission"
        OTHER           = "OTHER", "Other"

    class Priority(models.TextChoices):
        LOW     = "LOW", "Low"
        MEDIUM  = "MEDIUM", "Medium"
        HIGH    = "HIGH", "High"

    class Status(models.TextChoices): #status tindakan teacher
        OPEN        = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED    = "RESOLVED", "Resolved"
        CLOSED      = "CLOSED", "Closed"

    class Overcome(models.TextChoices):
        REMEDIAL            = "REMEDIAL", "Remedial"
        EXTRA_ASSIGNMENT    = "EXTRA_ASSIGNMENT", "Extra Assignment"
        REMINDER            = "REMINDER", "Reminder"
        COUNSELING          = "COUNSELING", "Counseling"
        CALL_PARENT         = "CALL_PARENT", "Call Parent"
        OTHER               = "OTHER", "Other"

    student     = models.ForeignKey(Student, on_delete=models.CASCADE,)
    teacher     = models.ForeignKey(Teacher, on_delete=models.CASCADE,)
    assignment  = models.ForeignKey(Assignment, on_delete=models.SET_NULL, related_name="fouls", null=True, blank=True)
    refer       = models.ForeignKey(Assignment, on_delete=models.SET_NULL, related_name="referred_fouls", null=True, blank=True)
    
    foul_type   = models.CharField( max_length=30, choices=Type.choices )
    priority    = models.CharField( max_length=10, choices=Priority.choices, default=Priority.MEDIUM )
    status      = models.CharField( max_length=20, choices=Status.choices, default=Status.OPEN )
    
    overcome_type   = models.CharField( max_length=30, choices=Overcome.choices )
    attachment  = models.FileField(upload_to='tracking/', blank=True, null=True)
    
    schedule    = models.DateTimeField( null=True, blank=True )
    resolved_at = models.DateTimeField( null=True, blank=True )
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-schedule", "-created_at"]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.foul_type}"

 