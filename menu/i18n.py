"""ترجمه رابط سایت (فارسی و انگلیسی).

متن‌های ثابت سایت در UI هستند. نام و توضیح منو، دسته‌بندی و آیتم‌ها از فیلدهای
*_en مدل‌ها خوانده می‌شود (در پنل ادمین پر می‌شوند).
برای افزودن زبان جدید: یک کلید به LANGS و UI اضافه کنید.
"""
from django.conf import settings

LANGS = ("fa", "en")


def get_lang(request):
    code = request.COOKIES.get("lang")
    return code if code in LANGS else getattr(settings, "DEFAULT_LANG", "fa")


def has_lang(request):
    """آیا کاربر قبلاً زبان را انتخاب کرده است؟"""
    return request.COOKIES.get("lang") in LANGS


UI = {
    "fa": {
        "digital_menu": "منوی دیجیتال",
        "table": "میز",
        "theme": "تغییر حالت روشن و تاریک",
        "back": "بازگشت به صفحه اول",
        "switch": "EN",
        "switch_aria": "Switch to English",
        "hello_1": "خوش آمدید.",
        "hello_2": "چه چیزی میل دارید؟",
        "pick_menu": "یکی از منوها را انتخاب کنید.",
        "no_menus": "هنوز منویی ساخته نشده. از پنل ادمین یک منو بسازید یا دستور",
        "no_menus_end": "را اجرا کنید.",
        "categories": "دسته‌بندی‌ها",
        "search_in": "جستجو در",
        "search": "جستجو",
        "view_list": "نمایش لیستی",
        "view_grid": "نمایش شبکه‌ای",
        "unit": "هزار تومان",
        "close": "بستن",
        "no_items": "هنوز آیتمی برای این منو ثبت نشده است.",
        "not_found": "آیتمی با این نام پیدا نشد. عبارت دیگری را امتحان کنید.",
    },
    "en": {
        "digital_menu": "Digital menu",
        "table": "Table",
        "theme": "Switch light / dark theme",
        "back": "Back to the start page",
        "switch": "فا",
        "switch_aria": "تغییر زبان به فارسی",
        "hello_1": "Welcome.",
        "hello_2": "What would you like?",
        "pick_menu": "Pick a menu to get started.",
        "no_menus": "No menu yet. Create one in the admin or run",
        "no_menus_end": "",
        "categories": "Categories",
        "search_in": "Search in",
        "search": "Search",
        "view_list": "List view",
        "view_grid": "Grid view",
        "unit": "Toman",
        "close": "Close",
        "no_items": "No items have been added to this menu yet.",
        "not_found": "No items match your search. Try another word.",
    },
}
