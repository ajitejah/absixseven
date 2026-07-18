from django.db import models

from app_auth.models import User


# ▀▄▀▄ roadmap
class Roadmap(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover       = models.ImageField(upload_to='roadmap/covers/', blank=True, null=True)
    release     = models.DateTimeField(null=True, blank=True)
    expired     = models.DateTimeField(null=True, blank=True)
    level       = models.ForeignKey('app_auth.Level', on_delete=models.SET_NULL, null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    owner = models.ForeignKey( User, on_delete=models.CASCADE, related_name='roadmaps', null=True, blank=True )
    created_at  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# ▀▄▀▄ node/checkpoint
class Node(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order       = models.PositiveIntegerField()
    duration    = models.PositiveIntegerField(help_text="Durasi dalam menit", null=True, blank=True)
    is_locked   = models.BooleanField(default=False)
    roadmap     = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='nodes')
    created_at  = models.DateTimeField(auto_now_add=True)
     
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.roadmap.name} - {self.name}"

# ▀▄▀▄ assignment
class Assignment(models.Model):
    node        = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='assignments')
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    attachment  = models.FileField(upload_to='assignments/', blank=True, null=True)
    duration    = models.PositiveIntegerField(help_text="Durasi dalam menit", null=True, blank=True)
    release     = models.DateTimeField(null=True, blank=True)
    expired     = models.DateTimeField(null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ▀▄▀▄ student progress per node
class StudentProgress(models.Model):
    student         = models.ForeignKey( 'app_auth.Student', on_delete=models.CASCADE)
    node            = models.ForeignKey(Node, on_delete=models.CASCADE)
    is_completed    = models.BooleanField(default=False)
    completed_at    = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'node')

    def __str__(self):
        return f"{self.student.user.email} - {self.node.name}"


# ▀▄▀▄ daftar submission siswa
class Submission(models.Model):
    file            = models.FileField(upload_to='submissions/')
    url             = models.URLField(blank=True)
    score           = models.FloatField(null=True, blank=True)
    feedback        = models.TextField(blank=True)

    # ===== REACTION =====
    reaction        = models.CharField(max_length=10, blank=True, default="")
    reacted_at      = models.DateTimeField(null=True, blank=True)

    submitted_at    = models.DateTimeField(auto_now_add=True)

    assignment      = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student         = models.ForeignKey('app_auth.Student', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.user.email} - {self.assignment.title}"