from io import BytesIO

import qrcode
from django.conf import settings
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .i18n import LANGS, has_lang
from .models import Item, Menu


def _table(request):
    """شماره میز از آدرس (?table=5). اگر نبود یا نامعتبر بود None."""
    raw = request.GET.get("table", "")
    return int(raw) if raw.isdigit() and len(raw) <= 3 else None


def home(request):
    """مرحله ۱: انتخاب زبان. مرحله ۲: انتخاب منو. (مرحله ۳: آیتم‌ها در menu_detail)"""
    table = _table(request)
    if not has_lang(request):
        names = settings.CAFE_NAME
        if getattr(settings, "CAFE_NAME_EN", ""):
            names += f" · {settings.CAFE_NAME_EN}"
        return render(request, "menu/language.html", {"table": table, "both_names": names})
    return render(request, "menu/home.html", {"menus": Menu.objects.all(), "table": table})


def menu_detail(request, slug):
    menu = get_object_or_404(Menu, slug=slug)
    available = Prefetch("items", queryset=Item.objects.filter(is_available=True))
    categories = [c for c in menu.categories.prefetch_related(available) if c.items.all()]
    return render(request, "menu/menu.html", {"menu": menu, "categories": categories, "table": _table(request)})


def _qr_png(url):
    buffer = BytesIO()
    qrcode.make(url, box_size=10, border=2).save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")


def qr_home(request):
    """QR صفحه اول (انتخاب زبان و منو)؛ با ?table=5 برای میز مشخص."""
    url = request.build_absolute_uri(reverse("home"))
    table = _table(request)
    if table:
        url += f"?table={table}"
    return _qr_png(url)


def qr_code(request, slug):
    """QR مستقیم یک منو؛ با ?table=5 برای میز مشخص."""
    get_object_or_404(Menu, slug=slug)
    url = request.build_absolute_uri(reverse("menu", args=[slug]))
    table = _table(request)
    if table:
        url += f"?table={table}"
    return _qr_png(url)


def set_lang(request, code):
    """زبان را در کوکی ذخیره می‌کند و به صفحه قبلی برمی‌گرداند."""
    target = request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}):
        target = reverse("home")
    response = HttpResponseRedirect(target)
    if code in LANGS:
        age = getattr(settings, "LANG_COOKIE_AGE", 60 * 60 * 24)
        response.set_cookie("lang", code, max_age=age, samesite="Lax")
    return response
