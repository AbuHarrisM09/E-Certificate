from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ECertificate.api.auth.apiviews import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("auth/login/", LoginView.as_view(), name='login'),
    path("auth/logout/", LogoutView.as_view(), name='logout'),
    
    path("", include("certificate.urls")),
    path("", include("course.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
