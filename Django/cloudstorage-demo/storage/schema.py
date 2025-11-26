from ninja import ModelSchema, Schema

from storage.models import CloudFile
from storage.utils import media_url


class CloudFileOut(ModelSchema):
    base_media_url: str = media_url

    class Meta:
        model = CloudFile

        fields = ["file"]


class ProcessReport(Schema):
    succeeded: bool = True
    message: str = "Action completed successfully"
