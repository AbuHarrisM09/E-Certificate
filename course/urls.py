from django.urls import path
from .views import create, data, detail, edit, delete
from course.api.views import *

app_name = 'course'


urlpatterns = [
    #course
    path("course/", data), #menampilkan data course
    path("course/new/", create), #menambahkan course baru
    path("course/detail/<int:id>/", detail, name='detail_course'), #melihat detail course
    path("course/edit/<int:id>/", edit, name='update_course'), #mengedit course
    path("course/delete/<int:id>/", delete, name='delete_course'), #menghapus course
    path("list-course/", courseViewSet.as_view({"get": "list", "post": "create"})),
]