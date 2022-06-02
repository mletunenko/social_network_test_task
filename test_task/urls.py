from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', include('social_network.urls')),
    path('admin/', admin.site.urls),
]
