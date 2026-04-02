from django.urls import path
from . import views_admin

urlpatterns = [

    path("login-admin/", views_admin.admin_login),

    path("painel/", views_admin.painel),

    path("logout-admin/", views_admin.admin_logout),

    path("booking/<int:id>/", views_admin.booking_detail),

]