# -*- coding: utf-8 -*-

import os
import Image

def get_thumbnail_url(image_url, size=150):
    thumbs_part = 'thumbs_' + str(size)
    image_url_parts = image_url.rsplit('/', 1)
    return image_url_parts[0] + '/' + thumbs_part + '/' + image_url_parts[1]

def get_thumbnail_path(image_path, size=150):
    thumbs_dir = 'thumbs_' + str(size)
    dirname, filename = os.path.split(image_path)
    dirname = os.path.join(dirname, thumbs_dir)
    if not os.path.exists(dirname):
        os.mkdir(dirname, 0755)
    return os.path.join(dirname, filename)

def create_thumbnail(image_path, width = 150, height = 190):
    thumb_path = get_thumbnail_path(image_path, width)
    delete_thumbnail(image_path, width)
    img = Image.open(image_path)
    img.thumbnail((width, height), Image.ANTIALIAS)
    img.save(thumb_path)

def delete_thumbnail(image_path, size=150):
    thumb_path = get_thumbnail_path(image_path, size)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)