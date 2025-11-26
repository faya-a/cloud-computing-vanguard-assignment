# cloudstorage

```sh
curl -X POST http://127.0.0.1:8000/storage/upload/ \
  -F "file=@db.sqlite3" -H "Authorization: Bearer 0578d2ea-40b1-4ebe-a976-b0ebbb22e817"
```

## Settings.py

```py
# CLOUDSTORAGE
CLOUD_STORAGE_BASE_URL = "http://localhost:8000"
CLOUD_STORAGE_MEDIA_URL = "/media/"
CLOUD_STORAGE_ABSOLUTE_URL_AS_NAME = True
CLOUD_STORAGE_API_TOKEN = "6631379b-c9e5-4881-92b7-4873d953a1a3"
```