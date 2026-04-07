"""
URL configuration for tespinjam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("write/", views.write_data, name="write_data"),
    path("delete/<str:product_id>/", views.delete_user, name="delete_user"),
    path("update-datein/", views.update_datein_view, name="update_datein"),
    path("sync-forms/", views.sync_forms_view, name="sync_forms"),
    path("", views.product_list, name="product_list"),
    path("delete_entry/", views.delete_entry, name="delete_entry"),
    path("download-csv/", views.download_csv, name="download_csv"),
]
