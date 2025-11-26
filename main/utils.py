from deep_translator import GoogleTranslator
from slugify import slugify
import uuid
import unicodedata
import os
import re


def generate_english_slug(text):
    try:
        translated = GoogleTranslator(source='fa', target='en').translate(text)
    except:
        translated = "can not translate"

    final_slug = slugify(translated)
    return final_slug


def clean_filename(file):
    ext = file.name.split(".")[-1]

    # حذف حروف غیر استاندارد
    safe_name = unicodedata.normalize("NFKD", file.name) \
        .encode("ascii", "ignore") \
        .decode("ascii")

    safe_name = safe_name.replace(" ", "-")

    # ساخت اسم یونیک
    new_name = f"{uuid.uuid4().hex}.{ext}"

    file.name = new_name
    return file
