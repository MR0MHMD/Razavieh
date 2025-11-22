from deep_translator import GoogleTranslator
from slugify import slugify


def generate_english_slug(text):
    try:
        translated = GoogleTranslator(source='fa', target='en').translate(text)
    except:
        translated = "can not translate"  # اگر ترجمه قطع شد همان فارسی را استفاده کن

    final_slug = slugify(translated)
    return final_slug
