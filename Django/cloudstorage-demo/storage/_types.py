from typing import Annotated

from django.http.request import HttpRequest
from ninja import UploadedFile
from ninja.params.functions import File

from storage.models import Application


class StorageRequestType(HttpRequest):
    auth: Application


UploadedFileType = Annotated[
    UploadedFile, File(description="File to be stored")
]
