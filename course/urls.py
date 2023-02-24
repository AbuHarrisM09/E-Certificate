from django.urls import path
#from .views import create, data, detail, edit, delete
from course.api.views import *

urlpatterns = [
    #course
    #path("course/", data), #menampilkan data course
    #path("course/new/", create), #menambahkan course baru
    #path("course/detail/<int:id>/", detail), #melihat detail course
    #path("course/edit/<int:id>/", edit), #mengedit course
    #path("course/delete/<int:id>/", delete), #menghapus course
    path("list-course/", courseViewSet.as_view({"get": "list", "post": "create"})),
]