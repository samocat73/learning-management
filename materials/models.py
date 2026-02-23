from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=75, verbose_name="Название", help_text="Введите название"
    )
    preview = models.ImageField(
        upload_to="materials/preview",
        verbose_name="Превью",
        help_text="Загрузите превью",
    )
    description = models.TextField(
        help_text="Введите описание", verbose_name="Описание"
    )
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="course",
        null=True,
        blank=True,
    )


class Lesson(models.Model):
    title = models.CharField(
        max_length=75, verbose_name="Название", help_text="Введите название"
    )
    description = models.TextField(
        help_text="Введите описание", verbose_name="Описание"
    )
    preview = models.ImageField(
        upload_to="materials/preview",
        verbose_name="Превью",
        help_text="Загрузите превью",
    )
    link = models.URLField(
        verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео"
    )
    course = models.ForeignKey(
        to=Course, on_delete=models.CASCADE, related_name="lessons"
    )
    owner = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, related_name="lesson"
    )
