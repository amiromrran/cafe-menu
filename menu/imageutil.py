"""یکدست‌سازی عکس آیتم‌ها: برش مربعی از مرکز، اندازه ثابت و فرمت JPEG."""
import os
from io import BytesIO

from PIL import Image, ImageOps

SIZE = 800  # پیکسل (مربع)


def normalize_bytes(data, size=SIZE):
    img = ImageOps.exif_transpose(Image.open(BytesIO(data)))
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    else:
        img = img.convert("RGB")
    img = ImageOps.fit(img, (size, size), method=Image.LANCZOS, centering=(0.5, 0.5))
    out = BytesIO()
    img.save(out, "JPEG", quality=85, optimize=True, progressive=True)
    return out.getvalue()


def normalize_field_file(field_file):
    """عکس تازه‌آپلودشده را قبل از ذخیره، یکدست می‌کند."""
    from django.core.files.base import ContentFile

    try:
        field_file.seek(0)
        data = field_file.read()
        new_data = normalize_bytes(data)
    except Exception:
        return  # اگر پردازش نشد، همان فایل اصلی ذخیره می‌شود
    name = os.path.splitext(os.path.basename(field_file.name))[0] + ".jpg"
    field_file.save(name, ContentFile(new_data), save=False)
