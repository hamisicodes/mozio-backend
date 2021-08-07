from rest_framework.views import APIView
from rest_framework import status
from .serializers import PolygonSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from django.contrib.gis.geos import Point
from .models import Polygon
import jwt


class PolygonCreateView(APIView):
    """An endpoint that allows a provider to create a polygon """
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        data = request.data
        data['provider'] = payload['id']

        serializer = PolygonSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class PolygonDetailView(APIView):
    """Get a polygon by its pk"""
    def get(self, request, format=None, **kwargs):
        id = kwargs.get('pk')
        polygon = Polygon.objects.filter(id=id).first()
        serializer = PolygonSerializer(polygon)

        return Response(serializer.data)


@api_view(['GET'])
def get_polygons_with_specified_point(request):
    """returns a list of all polygons that include the given lat/lng"""
    try:
        latitude = float(request.data.get('latitude', ''))
        longitude = float(request.data.get('longitude', ''))
    except ValueError:
        return Response({'Error': 'Please pass the latitude and longitude'},
                        status=status.HTTP_404_NOT_FOUND)
    user_location = Point(longitude, latitude, srid=4326)

    valid_polygons = []
    for polygon in Polygon.objects.all().iterator():
        if polygon.location.contains(user_location):
            valid_polygons.append(polygon)

    serializer = PolygonSerializer(valid_polygons, many=True)
    return Response(serializer.data)
