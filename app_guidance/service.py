from . models import ParentActivityLog, Notification


def log_parent_activity(
    parent,
    activity_type,
    title,
    description=""
):
    ParentActivityLog.objects.create(
        parent=parent,
        activity_type=activity_type,
        title=title,
        description=description,
    ) 


def create_notification(
    *,
    receiver,
    notification_type,
    title,
    path,
    sender=None,
    description="",
):
    """
    Membuat notifikasi untuk user.

    Contoh:
        create_notification(
            receiver=teacher,
            sender=request.user,
            notification_type=Notification.NotificationType.CHAT,
            title="Pesan Baru",
            description="Orang tua mengirim pesan.",
            path="/teacher/guidance/message/10/"
        )
    """

    return Notification.objects.create(
        sender=sender,
        receiver=receiver,
        notification_type=notification_type,
        title=title,
        description=description,
        path=path,
    )