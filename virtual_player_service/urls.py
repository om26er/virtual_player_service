from django.conf.urls import include, url
from django.contrib import admin

from player import urls as service_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(service_urls)),
]
