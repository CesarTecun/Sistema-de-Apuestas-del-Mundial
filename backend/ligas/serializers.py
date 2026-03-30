from rest_framework import serializers
from .models import Liga

class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = '__all__'
