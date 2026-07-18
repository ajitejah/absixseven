from app_setting.models import Setting

def get_setting(group, section, key, default=""):
    try:
        setting = Setting.objects.get(
            group=group,
            section=section,
            key=key,
            is_active=True,
        )
        if setting.type == "image":
            return setting.image
        elif setting.type == "video":
            return setting.video
        return setting.value
    except Setting.DoesNotExist:
        return default