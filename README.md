# johnj.club
This is the source code for my personal website. It is a fairly standard Django articles-style app, with a few idiomatic inclusions unique to my personal use-case. 

## Getting Started

### Prerequisites

Install Python and Pip:

`sudo apt install python3 pip`

Install Python dependencies:

`pip3 install django Pillow django-storages boto3`

Note that `django-storages` and `boto3` are only required if you intend to use S3 for static and/or media files.

### Installing

Just fork from here. This code is currently not available anywhere else.


### Setup Idiomatic Characteristics

settings.py will need the following settings:

```python
SITE_TITLE: "" # A string used for the <title> tags
IMAGE_THUMBNAIL_SIZE = () # A tuple containing the size, in pixels, thumbnail images for Series, Articles, and so on should be set to.
IMAGE_FULL_SIZE = () # Also a tuple of pixel sizes, used for the larger version of the image in Articles, Series, and Authors.
```
It also expected that all of the following will be true:

1. There is an Article titled "Welcome"
2. There is an Article titled "About Me"
3. There is an Article titled "Portfolio"
4. There is a Seris titled "Wyverns and Whimsy"

All of these, especially #4, are highly idiomatic to my use-case and so may be changed. #1 is found in views.index, and 2-4 are all in context_processors and templates/articles/base.html (in `navDiv`).

### AWS S3

My own instance runs static and media files through AWS. This is not required, but the `storage_backends.py` assumes it to be true. If you wish to use this code and do not wish to use S3, simply don't set it up in `settings.py`. If you do not want to use S3 and also do not want the unnecessary code, do not install `django-storages`, `boto3`, and delete `storage_backends.py`.

## License

This project is licensed under the terms of the MIT license.
