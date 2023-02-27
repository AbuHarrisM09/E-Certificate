from rest_framework import serializers
from certificate.models import certificate


class certificateSerializer(serializers.ModelSerializer):
    unique_code = serializers.CharField(read_only=True)

    class Meta:
        model = certificate
        fields = '__all__'
