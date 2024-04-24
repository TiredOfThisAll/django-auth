from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "api"
urlpatterns = [
    path("login/send-code/", views.send_code, name="send_code"),
    path("login/verify-code/", views.verify_code, name="verify_code"),
    path("login/add-user/", views.create_user, name="create_user"),
    path("login/verificate-user/", views.verificate_user, name="verificate_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("user/<id>/", views.get_user_by_id, name="get_user_by_id"),
    path("user/<id>/apply-invite-code/", views.apply_invite_code, name="apply_invite_code"),
    path("user/<id>/get-invited-users/", views.get_invited_users, name="get_invited_users"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
