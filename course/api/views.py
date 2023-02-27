from rest_framework import viewsets
from certificate.models import course
from .serializers import courseSerializer


class courseViewSet(viewsets.ModelViewSet):
    queryset = course.objects.all()
    serializer_class = courseSerializer