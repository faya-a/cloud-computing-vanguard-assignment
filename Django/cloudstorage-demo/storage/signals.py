from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from storage.models import CloudFile
from storage.utils import compute_file_hash


@receiver(pre_delete, sender=CloudFile)
def cloudfile_completely_delete_file(
    sender, instance: CloudFile, **kwargs
):
    instance.delete_file()


@receiver(pre_save, sender=CloudFile)
def generate_file_hash(sender, instance: CloudFile, **kwargs):
    if not instance.hash:
        instance.hash = compute_file_hash(instance.file)
