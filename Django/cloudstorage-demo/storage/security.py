from django.core.exceptions import ValidationError
from ninja.security import HttpBearer

from storage.models import Application


class StorageHttpBearer(HttpBearer):
    async def authenticate(self, request, token):
        try:
            app = await Application.objects.filter(
                token=token, is_valid=True
            ).afirst()

            return app

        except ValidationError:
            return None
