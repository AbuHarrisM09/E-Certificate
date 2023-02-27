from rest_framework import viewsets
from certificate.models import certificate
from .serializers import certificateSerializer

class certificateViewSet(viewsets.ModelViewSet):
    queryset = certificate.objects.all()
    serializer_class = certificateSerializer