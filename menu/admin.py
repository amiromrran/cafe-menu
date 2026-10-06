from django.contrib import admin

from .models import Category, Item, Menu

admin.site.site_header = "مدیریت منو"
admin.site.site_title = "مدیریت منو"
admin.site.index_title = "منوها، دسته‌بندی‌ها و آیتم‌ها"


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "order")
    list_editable = ("order",)
    inlines = [CategoryInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "menu", "order")
    list_filter = ("menu",)
    list_editable = ("order",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "order")
    list_filter = ("category__menu", "category", "is_available")
    list_editable = ("price", "is_available", "order")
    search_fields = ("name", "description")
