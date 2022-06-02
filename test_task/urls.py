from django.urls import include, path

urlpatterns = [
    path('', include('social_network.urls')),
]
