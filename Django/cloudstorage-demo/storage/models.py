# Create your models here.
import os
from uuid import uuid4

from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _


def generate_document_filepath(
    instance: "CloudFile", filename: str
) -> str:
    filename, extension = os.path.splitext(filename)
    return f"{instance.app.identity}/{filename}{extension}"


class Application(models.Model):
    identity = models.CharField(
        help_text=_("Token name"),
        null=True,
        blank=False,
        max_length=40,
        unique=True,
    )
    token = models.UUIDField(
        help_text=_("Request bearer flag"), default=uuid4
    )
    is_valid = models.BooleanField(
        default=True, help_text=_("Whether this token is still valid")
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text=_("Date entered")
    )

    def __str__(self):
        return str(self.identity)


class CloudFile(models.Model):
    file = models.FileField(upload_to=generate_document_filepath)
    hash = models.TextField(
        null=True,
        blank=True,
        help_text=_("Hash value of the file"),
        db_index=True,
        unique=True,
    )
    app = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="files",
        help_text=_("Sending application"),
    )
    extra_upload_count = models.IntegerField(
        default=0,
        blank=False,
        null=False,
        help_text=_("Number of extra times file has been uploaded"),
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    @property
    def url(self):
        return self.file.url

    @property
    def can_delete(self):
        return self.extra_upload_count == 0

    def delete_file(self):
        if self.can_delete:
            storage, path = self.file.storage, self.file.path
            storage.delete(path)

    def delete(self, *args, **kwargs):
        if self.can_delete:
            return super().delete(*args, **kwargs)
        else:
            self.extra_upload_count -= 1
            self.save()

    async def adelete(self, *args, **kwargs):
        if self.can_delete:
            return await super().adelete(*args, **kwargs)
        else:
            self.extra_upload_count -= 1
            await self.asave()


# NOTE: Just for testing the cloud itself

from cloudstorage.backend_storage import CloudStorage  # noqa: E402

cloud_storage = CloudStorage(token="4c077326-e157-469d-9cda-a8d7b6618075")


class Music(models.Model):
    cover_photo = models.FileField(storage=cloud_storage)
    audio = models.FileField(storage=cloud_storage)
