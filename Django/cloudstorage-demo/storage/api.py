from typing import Annotated

from ninja import NinjaAPI
from ninja.params.functions import Path
from ninja.throttling import AnonRateThrottle, AuthRateThrottle
from starlette import status

from storage._types import StorageRequestType, UploadedFileType
from storage.models import CloudFile
from storage.schema import CloudFileOut, ProcessReport
from storage.security import StorageHttpBearer
from storage.utils import (
    delete_cloud_file_completely,
    remove_media_url,
    save_file_or_get_instance,
    update_existing_file,
)

api = NinjaAPI(
    title="CloudStorage",
    version="0.1.0",
    auth=StorageHttpBearer(),
    description=("Host file in the cloud"),
    throttle=[AuthRateThrottle("100/h"), AnonRateThrottle("100/h")],
)


@api.exception_handler(CloudFile.DoesNotExist)
def cloud_file_no_existing_handler(
    request: StorageRequestType, exc: Exception
):
    return api.create_response(
        request,
        data=ProcessReport(
            succeeded=False,
            message=(
                "The requested file to perfom operation against "
                "does not exist."
            ),
        ),
        status=status.HTTP_404_NOT_FOUND,
    )


@api.post(
    "/upload", response=CloudFileOut, description="Upload file to cloud"
)
async def upload_cloud_file(
    request: StorageRequestType, file: UploadedFileType
) -> CloudFileOut:
    response = await save_file_or_get_instance(request, file)

    return response


@api.patch(
    "/update/{path:filename}",
    response=CloudFileOut,
    description="Update existing file",
)
async def update_existing_cloud_file(
    request: StorageRequestType,
    filename: Annotated[str, Path(description="Existing filename")],
    file: UploadedFileType,
) -> CloudFileOut:
    existing_file = await CloudFile.objects.aget(
        file=remove_media_url(filename), app=request.auth
    )
    response = await update_existing_file(existing_file, new_file=file)
    return response


@api.delete(
    "/delete/{path:filename}",
    response=ProcessReport,
    description=("Delete a file given its's filename"),
)
async def delete_cloud_file(
    request: StorageRequestType,
    filename: Annotated[str, Path(description="Existing filename")],
) -> ProcessReport:
    target_file = await CloudFile.objects.aget(
        file=remove_media_url(filename), app=request.auth
    )

    await delete_cloud_file_completely(target_file)

    return ProcessReport(message="File deleted successfully")
