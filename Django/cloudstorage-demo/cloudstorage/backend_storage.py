"""
Custom storage backend for media files in django

## Motive
The aim was to distribute the media files across multiple
self-hostable server that I created - https://github.com/FayaLLC/cloudstorage

## NOTE:
This backend is optimized for my own needs but you are free to customize
it to your own liking.

"""

import io
import re
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import httpx
from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

# Settings defaults

DEBUG = getattr(settings, "DEBUG", False)

CLOUD_BASE_URL = getattr(
    settings,
    "CLOUD_STORAGE_BASE_URL",
)
CLOUD_MEDIA_URL = (
    getattr(settings, "CLOUD_STORAGE_MEDIA_URL", None) or "/media/"
)
DEFAULT_MEDIA_URL = getattr(settings, "MEDIA_URL", "/media/")

AUTO_DETECT_LOCAL_FILE = getattr(
    settings, "CLOUD_STORAGE_AUTO_DETECT_LOCAL_FILE", DEBUG
)

API_TOKEN = getattr(settings, "CLOUD_STORAGE_API_TOKEN")

SPLIT_ABSOLUTE_NAME_PATTERN = re.compile(
    r"(https?://[\w\-_:]+)(/[^/]+/)(.+)"
)

if AUTO_DETECT_LOCAL_FILE:
    MEDIA_ROOT = Path(getattr(settings, "MEDIA_ROOT"))
    SITE_ADDRESS = getattr(settings, "SITE_ADDRESS")
    # Accessible host address


@dataclass(frozen=True)
class UploadedFileDetails:
    base_media_url: str
    file: str

    @property
    def name(self) -> str:
        """Return the filename without the base media URL."""
        return self.file.replace(self.base_media_url, "")


@deconstructible
class CloudStorage(Storage):
    """
    Synchronous Django storage backend using CloudStorage API.
    url : https://github.com/FayaLLC/cloudstorage
    """

    RETRY_COUNT = 3
    RETRY_BACKOFF = 1

    def __init__(
        self,
        cloud_base_url=None,
        token: str = None,
        media_url: str | None = None,
        **httpx_kwargs,
    ):
        self.api_base_url = (cloud_base_url or CLOUD_BASE_URL).rstrip(
            "/"
        ) + "/api/v1/"
        self.media_url = media_url or CLOUD_MEDIA_URL
        if not self.media_url.endswith("/"):
            self.media_url += "/"

        self.token = token or API_TOKEN
        self.headers = {
            "User-Agent": "CloudStorage API v0.1.0",
            "Accept": "application/json",
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

        httpx_kwargs.setdefault("timeout", httpx.Timeout(10.0))
        self.client = httpx.Client(
            base_url=self.api_base_url,
            headers=self.headers,
            **httpx_kwargs,
        )

    @property
    def cloud_base_url(self) -> str:
        url = urlsplit(self.api_base_url)
        return f"{url.scheme}://{url.netloc}"

    def _split_absolute_name(self, name: str) -> tuple[str]:
        elements = SPLIT_ABSOLUTE_NAME_PATTERN.match(name)
        return elements.groups()

    def get_name(self, name: str) -> str:
        if name.startswith("http"):
            base_url, media_url, name = self._split_absolute_name(name)

        return name

    def _save(self, name, content):
        """
        Save a file to the cloud via POST /upload.
        Retries on transient network errors or 5xx responses.
        """
        if hasattr(content, "read"):
            file_bytes = content.read()
            content.seek(0)
        else:
            file_bytes = content

        files = {
            "file": (
                name,
                file_bytes,
                getattr(content, "content_type", None),
            )
        }

        for attempt in range(self.RETRY_COUNT):
            try:
                resp = self.client.post("/upload", files=files)
                if resp.status_code >= 500:
                    raise httpx.HTTPStatusError(
                        "Server error",
                        request=resp.request,
                        response=resp,
                    )
                resp.raise_for_status()
                data = UploadedFileDetails(**resp.json())
                return data.name

            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                if attempt < self.RETRY_COUNT - 1:
                    time.sleep(
                        self.RETRY_BACKOFF * (2**attempt)
                    )  # Exponential backoff
                    continue
                raise e

    def delete(self, name):
        """
        Delete a file via DELETE /delete/{filename}.
        Retries on transient network errors or 5xx responses.
        Returns True if deleted, False if not found.
        """
        for attempt in range(self.RETRY_COUNT):
            try:
                resp = self.client.delete(f"/delete/{name}")
                if resp.status_code == 404:
                    return False
                if resp.status_code >= 500:
                    raise httpx.HTTPStatusError(
                        "Server error",
                        request=resp.request,
                        response=resp,
                    )
                resp.raise_for_status()
                return True
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                if attempt < self.RETRY_COUNT - 1:
                    time.sleep(self.RETRY_BACKOFF * (2**attempt))
                    continue
                raise e

    def exists(self, name):
        """
        Check if a file exists via HEAD request (no auth required).
        Returns True if exists, False otherwise.
        """
        try:
            resp = httpx.head(self.url(name), timeout=10.0)
            return resp.status_code == 200
        except httpx.HTTPError:
            return False

    def url(self, name):
        """
        Return the accessible URL for the file.
        Combines cloud base URL with media URL and filename.
        """
        if AUTO_DETECT_LOCAL_FILE:
            local_file = MEDIA_ROOT / name
            if local_file.exists():
                return urljoin(
                    urljoin(SITE_ADDRESS, DEFAULT_MEDIA_URL), name
                )

        return urljoin(self.cloud_base_url + self.media_url, name)

    def _open(self, name, mode="rb"):
        """
        Retrieve file content from the cloud and return a Django
        File object.
        """
        resp = httpx.get(self.url(name), timeout=10.0)
        resp.raise_for_status()
        return File(io.BytesIO(resp.content), name=name)

    def size(self, name) -> int:
        resp = httpx.head(self.url(name), timeout=10.0)
        file_size = resp.headers.get("Content-Length", None)
        if file_size:
            return int(file_size.strip())

    def path(self, name) -> str:
        return self.url(name)


cloud_storage = CloudStorage()
"""CloudStorage with default settings from settings.py"""
