from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "web"
urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("login/", views.login_page, name="login"),
    path("user/<id>/", views.user_profile_page, name="user_profile"),
    path("logout/", views.logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)