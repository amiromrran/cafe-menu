from django.db import models

from .imageutil import normalize_field_file


class Menu(models.Model):
    """یک منوی اصلی، مثلاً «منوی کافه» یا «منوی رستوران»."""

    title = models.CharField("عنوان", max_length=80)
    slug = models.SlugField("آدرس (انگلیسی)", unique=True, help_text="مثلاً cafe یا restaurant")
    icon = models.CharField("ایموجی", max_length=8, blank=True, default="🍽️")
    subtitle = models.CharField("توضیح کوتاه", max_length=140, blank=True)
    title_en = models.CharField("عنوان (انگلیسی)", max_length=80, blank=True, default="")
    subtitle_en = models.CharField("توضیح کوتاه (انگلیسی)", max_length=140, blank=True, default="")
    order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "منو"
        verbose_name_plural = "منوها"

    def __str__(self):
        return self.title


class Category(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="categories", verbose_name="منو")
    title = models.CharField("عنوان", max_length=80)
    title_en = models.CharField("عنوان (انگلیسی)", max_length=80, blank=True, default="")
    icon = models.CharField("ایموجی", max_length=8, blank=True)
    order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return f"{self.menu.title} / {self.title}"


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items", verbose_name="دسته‌بندی")
    name = models.CharField("نام", max_length=100)
    description = models.TextField("توضیحات", blank=True)
    name_en = models.CharField("نام (انگلیسی)", max_length=100, blank=True, default="")
    description_en = models.TextField("توضیحات (انگلیسی)", blank=True, default="")
    price = models.PositiveIntegerField("قیمت (هزار تومان)")
    image = models.ImageField("عکس", upload_to="items/", blank=True, help_text="هر اندازه‌ای باشد، خودکار مربعی ۸۰۰×۸۰۰ می‌شود؛ سوژه را وسط کادر بگیرید.")
    is_available = models.BooleanField("موجود است", default=True)
    order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "آیتم"
        verbose_name_plural = "آیتم‌ها"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # هر عکسی که آپلود شود مربعی ۸۰۰×۸۰۰ و JPEG می‌شود تا همه یکدست باشند
        if self.image and not self.image._committed:
            normalize_field_file(self.image)
        super().save(*args, **kwargs)
