import asyncio
import hashlib

from django.conf import settings
from django.db.models import FileField

from storage._types import StorageRequestType, UploadedFileType
from storage.models import CloudFile

media_url = getattr(settings, "MEDIA_URL", "/media/")


def remove_media_url(filename: str) -> str:
    return filename.replace(media_url, "")


def compute_file_hash(
    file: UploadedFileType | FileField,
    chunk_size=8192,
):
    if isinstance(file, FileField):
        file = file.file

    hasher = hashlib.sha256()
    for chunk in file.chunks(chunk_size):
        hasher.update(chunk)

    return hasher.hexdigest()


async def save_file_or_get_instance(
    request: StorageRequestType, file: UploadedFileType
) -> CloudFile:
    file_hash = compute_file_hash(file)

    existing_file = await CloudFile.objects.filter(
        hash=file_hash
    ).afirst()

    if existing_file:
        existing_file.extra_upload_count += 1
        await existing_file.asave()

        return existing_file

    new_file = await CloudFile.objects.acreate(
        hash=file_hash, app=request.auth
    )

    new_file.file.name = file.name

    await asyncio.to_thread(new_file.file.save, file.name, file, True)

    return new_file


async def update_existing_file(
    existing_file: CloudFile, new_file: UploadedFileType
) -> CloudFile:
    await asyncio.to_thread(existing_file.delete_file)

    existing_file.file.name = new_file.name

    await asyncio.to_thread(
        existing_file.file.save, new_file.name, new_file, True
    )

    return existing_file


async def delete_cloud_file_completely(cloud_file: CloudFile):
    await asyncio.to_thread(cloud_file.delete_file)
    delete_report = await cloud_file.adelete()
    return delete_report
