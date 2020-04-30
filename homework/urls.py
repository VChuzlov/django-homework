from django.conf.urls import url
from django.contrib import admin

from homework.views import IndexView

urlpatterns = [
    url(r'^', IndexView.as_view()),
]
