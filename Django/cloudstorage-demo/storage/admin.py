# Register your models here.
import os

from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from cloudstorage.settings import MEDIA_ROOT
from cloudstorage.utils import get_filesize_string

from .models import Application, CloudFile, Music

if getattr(settings, "DEBUG", False):
    admin.site.register(Music)


@admin.register(CloudFile)
class CloudFileAdmin(admin.ModelAdmin):
    list_display = (
        "app",
        "file",
        "size",
        "extra_upload_count",
        "uploaded_at",
    )
    list_filter = ("uploaded_at", "app")
    # search_fields = ("file", "app__token")
    date_hierarchy = "uploaded_at"
    ordering = ("-uploaded_at",)

    readonly_fields = (
        "hash",
        "uploaded_at",
    )

    def size(self, obj: CloudFile):
        file_path = MEDIA_ROOT / obj.file.name
        if file_path.exists():
            return get_filesize_string(os.path.getsize(file_path))


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "identity",
        "file_count",
        "is_valid",
        "created_at",
    )
    list_filter = ("is_valid", "created_at")
    search_fields = ("token",)
    ordering = ("-created_at",)
    readonly_fields = (
        "token",
        "created_at",
    )

    def file_count(self, obj):
        return obj.files.count()

    file_count.short_description = _("Files Uploaded")
