from django.conf.urls import url
from django.contrib import admin

from .views import (
    ReviewsCreateAPIView,
    ReviewsDeleteAPIView,
    ReviewsDetailAPIView,
    ReviewsListAPIView,
    ReviewsUpdateAPIView,
    )

urlpatterns = [
    url(r'^$', ReviewsListAPIView.as_view(), name='list'),
    url(r'^create/$', ReviewsCreateAPIView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', ReviewsDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', ReviewsUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', ReviewsDeleteAPIView.as_view(), name='delete'),
]