from django.db import models
from app_auth.models import User
from app_roadmap.models import Assignment, Submission 

class Message(models.Model):

    class MessageType(models.TextChoices):
        TEXT = "text", "Text"
        SUBMISSION = "submission", "Submission"

    type = models.CharField(
        max_length=20,
        choices=MessageType.choices,
        default=MessageType.TEXT
    )

    sender      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    assignment  = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    submission  = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True, blank=True)
    content     = models.TextField()
    is_read     = models.BooleanField(default=False)
    react       = models.CharField(max_length=50, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)


class ParentActivityLog(models.Model):

    class ActivityType(models.TextChoices):
        REACTION    = "reaction", "Memberi reaksi emoji."
        ASK         = "ask", "Bertanya kepada guru via Chat." 

    parent          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="parent_activities")
    activity_type   = models.CharField(max_length=30, choices=ActivityType.choices)
    title           = models.CharField(max_length=255)
    description     = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):

    class NotificationType(models.TextChoices):
        CHAT               = "chat", "Chat Baru"
        PARENT_ACTIVITY    = "parent_activity", "Aktivitas Parent"
        ASSIGNMENT         = "assignment", "Assignment Baru"
        SUBMISSION         = "submission", "Submission Baru"
        SCORE              = "score", "Nilai Baru"
        ROADMAP            = "roadmap", "Roadmap Baru"
        SYSTEM             = "system", "Sistem"

    sender      = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_notifications" )
    receiver    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_read     = models.BooleanField(default=False)  
    path        = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def icon(self):
        return {
            "chat": "💬",
            "parent_activity": "👨‍👩‍👦",
            "assignment": "📝",
            "submission": "📤",
            "score": "⭐",
            "roadmap": "🗺️",
        }.get(self.notification_type, "🔔")
    
    def color(self):
        return {
            "chat": "info",
            "parent_activity": "warning",
            "assignment": "primary",
            "submission": "success",
            "score": "secondary",
            "roadmap": "purple",
        }.get(self.notification_type, "slate")