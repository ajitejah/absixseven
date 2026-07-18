from app_setting.models import Setting


class SettingService:

    @staticmethod
    def get(group, section="", key="", default=None):
        try:
            setting = Setting.objects.get(
                group=group,
                section=section,
                key=key,
                is_active=True,
            )

            if setting.type == "image":
                return setting.image

            if setting.type == "video":
                return setting.video

            return setting.value

        except Setting.DoesNotExist:
            return default

    @staticmethod
    def web(key, default=None):
        return SettingService.get("WEB", "", key, default)

    @staticmethod
    def content(section, key, default=None):
        return SettingService.get("CONTENT", section, key, default)