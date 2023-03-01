from rest_framework import serializers
from course.models import course


class courseSerializer(serializers.ModelSerializer):
    class Meta:
        model = course
        fields = '__all__'