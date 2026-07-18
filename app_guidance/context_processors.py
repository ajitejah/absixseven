from app_guidance.models import Notification


def notification_context(request):

    if not request.user.is_authenticated:
        return {}

    qs = Notification.objects.filter(
        receiver=request.user
    ).order_by("-created_at")

    return {
        "notifications": qs[:10],
        "unread_notifications": qs.filter(
            is_read=False
        ).count(),
    }