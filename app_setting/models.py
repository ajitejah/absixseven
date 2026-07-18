from django.db import models


class Setting(models.Model):

    GROUP_CHOICES = (
        ("WEB", "WEB"),
        ("CONTENT", "CONTENT"),
    )

    TYPE_CHOICES = (
        ("text", "Text"),
        ("textarea", "Textarea"),
        ("image", "Image"),
        ("video", "Video"),
        ("icon", "Icon"),
    )

    group = models.CharField(
        max_length=20,
        choices=GROUP_CHOICES,
        db_index=True,
    )

    section = models.CharField(
        max_length=50,
        blank=True,
        default="",
        db_index=True,
        help_text="Contoh: HEADER, ICON1, ROADMAP",
    )

    key = models.CharField(
        max_length=100,
        help_text="Nama key program",
    )

    label = models.CharField(
        max_length=100,
        help_text="Label yang tampil di Admin",
    )

    value = models.TextField(
        blank=True,
        default="",
    )

    image = models.ImageField(
        upload_to="setting/web/",
        blank=True,
        null=True,
    )

    video = models.FileField(
        upload_to="setting/web/",
        blank=True,
        null=True,
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="text",
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "group",
            "section",
            "order",
            "id",
        ]
        unique_together = (
            "group",
            "section",
            "key",
        )

    def __str__(self):
        return f"{self.group} - {self.section} - {self.label}"