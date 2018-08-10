from johnjclub import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Default storage for media files. Used to save media to AWS S3.

    DEFAULT_FILE_STORAGE in settings should be set to use this class,
    and settings also needs to have MEDIAFILES_LOCATION, 
    AWS_MEDIA_STORAGE_BUCKET_NAME, and AWS_MEDIA_S3_CUSTOM_DOMAIN set to
    appropriate values.
    """

    location = settings.MEDIAFILES_LOCATION
    file_overwrite = True
    bucket_name = settings.AWS_MEDIA_STORAGE_BUCKET_NAME
    custom_domain = settings.AWS_MEDIA_S3_CUSTOM_DOMAIN