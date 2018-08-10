from johnjclub import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = True
    bucket_name = settings.AWS_MEDIA_STORAGE_BUCKET_NAME
    custom_domain = settings.AWS_MEDIA_S3_CUSTOM_DOMAIN