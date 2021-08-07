from rest_framework import serializers
from .models import Polygon


class PolygonSerializer(serializers.ModelSerializer):
    # provider = serializers.ReadOnlyField(source='provider.id')

    class Meta:
        model = Polygon

        fields = [

            'id', 'name', 'price', 'location', 'provider'
        ]
