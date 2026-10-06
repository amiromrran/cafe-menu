from django.conf import settings

from .i18n import UI, get_lang


def cafe(request):
    lang = get_lang(request)
    name_en = getattr(settings, "CAFE_NAME_EN", "")
    return {
        "cafe_name": name_en if lang == "en" and name_en else settings.CAFE_NAME,
        "lang": lang,
        "dir": "ltr" if lang == "en" else "rtl",
        "t": UI[lang],
        "other_lang": "fa" if lang == "en" else "en",
    }
