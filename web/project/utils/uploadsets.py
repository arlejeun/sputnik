# coding: utf-8
import os
import uuid
from PIL import Image
from flask_uploads import UploadSet, IMAGES, extension, DATA, ALL

# UploadSets

# Set up Flask Uploads
# Constants fir the allowed extension of jar plugins
PLUGINS = tuple('jar'.split())
OPTIONS = tuple('cfg'.split())

#upload_images_dashboards = UploadSet('screenshots', IMAGES)
upload_images = UploadSet('screenshots', IMAGES)
upload_exported_dashboards = UploadSet('definitions', DATA)
upload_exported_templates = UploadSet('definitions', DATA)
upload_exported_options = UploadSet('options', OPTIONS)
upload_jar_plugins = UploadSet('plugins', PLUGINS)



def process_user_avatar(file_storage, upload_set, border):
    """Center clipping, resize and then save the avatar."""
    image = open_image(file_storage)
    image = center_crop(image)
    image = resize_square(image, border)
    ext = extension(file_storage.filename)
    return save_image(image, upload_set, ext)


def open_image(file_storage):
    """Open image from FileStorage."""
    image = Image.open(file_storage.stream)
    # See: https://github.com/smileychris/easy-thumbnails/issues/95
    if image.format == 'JPEG' and image.mode != "RGB":
        image = image.convert("RGB")
    return image


def save_image(image, upload_set, ext):
    """Save image with random filename and original ext."""
    filename = '%s.%s' % (random_filename(), ext)
    dir_path = upload_set.config.destination

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    path = os.path.join(dir_path, filename)
    image.save(path)
    return filename


def center_crop(image):
    w, h = image.size
    if w > h:
        border = h
        avatar_crop_region = ((w - border) / 2, 0, (w + border) / 2, border)
    else:
        border = w
        avatar_crop_region = (0, (h - border) / 2, border, (h + border) / 2)
    return image.crop(avatar_crop_region)


def resize_square(image, border):
    return image.resize((border, border), Image.ANTIALIAS)


def random_filename():
    return str(uuid.uuid4())