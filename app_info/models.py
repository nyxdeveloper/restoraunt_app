from django.db import models
import os


def faq_img_path(instance, filename):
    return os.path.join("faq", instance.title, filename)


class FAQ(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to=faq_img_path, blank=True)
    href = models.TextField(blank=True, default="")
    description = models.TextField(blank=True, default="")

    def __str__(self): return self.title

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ["title"]
