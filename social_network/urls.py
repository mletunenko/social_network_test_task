from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views
from social_network import views

urlpatterns = [
    path('registration/', views.user_registration),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

router = SimpleRouter()
router.register(r'post', views.PostViewSet, basename='post')
urlpatterns = urlpatterns + router.urls
