from django.urls import path, include
from certificate.api.views import *

from .views import create

urlpatterns = [
    #dashboard
    #path("dashboard/", dashboard), #halaman setelah login, menampilkan excel yang sudah di upload
    path("dashboard/new/", create), #halaman form untuk input manual atau upload CSV

    #certificate
    #path("certificate/", data), #halaman menampilkan sertifikat yang sudah jadi
    #path("certificate/detail/<int:id>/", detail), #halaman untuk menampilkan detail sertifikat tertentu
    #path("certificate/delete/<int:id>/", delete), #method untuk menghapus sertifikat tertentu
    path("list-certificate/", certificateViewSet.as_view({"get": "list", "post": "create"})),

]