from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("m/<slug:slug>/", views.menu_detail, name="menu"),
    path("qr/", views.qr_home, name="qr_home"),
    path("qr/<slug:slug>/", views.qr_code, name="qr"),
    path("lang/<slug:code>/", views.set_lang, name="set_lang"),
]
