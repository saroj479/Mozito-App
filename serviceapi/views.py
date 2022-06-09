from django.http import HttpResponse
from rest_framework import generics, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shapely.geometry import Polygon, Point

from serviceapi.serializers import ProviderSerializer, GeoSerializer, QuerySerializer
from serviceapi.models import Provider, GeoPolygon
import request


# Create your views here.

def index(request):
    """
    Welcomes the user to the REST API
    """
    return HttpResponse('Welcome to Mozio REST API')


class ProviderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    ProviderDetail uses Django generic classes to Retrieve, Update
     and Delete a already existing Provider
    It uses pk as a URL arg to filter out an individual Provider
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ProviderList(generics.ListCreateAPIView):
    """
    ProviderList uses Django generic classes to Create a new Provider
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class GeoPolygonDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GeoPolygonDetail uses Django generic classes to Retrieve, Update
    and Delete a already existing GeoPolygon (polygon)
    It uses pk as a URL arg to filter out an individual Polygon
    """
    queryset = GeoPolygon.objects.all()
    serializer_class = GeoSerializer


class GeoPolygonList(generics.ListCreateAPIView):
    """
    GeoPolygonList uses Django generic ListCreateAPIView classe
     to Create a new Polygon
    """
    queryset = GeoPolygon.objects.all()
    serializer_class = GeoSerializer


@api_view(['GET'])
def query(request):
    """
    query function outputs the all the polygon information associated with
    a particular latitude and longtitude
    Gets lat (latitude) and long (longitude) from the URL query parameters
    Selects Polygons that contain latitude and longitude
    Returns a polygon which is serialised by QuerySerializer
    """
    lat = request.GET.get('lat', None)
    long = request.GET.get('long', None)

    if lat is None or long is None:
        return HttpResponse('Wrong')

    point = Point(float(lat), float(long))
    selected_poly = []
    queryset = GeoPolygon.objects.all()
    for polygons in queryset:
        poly_coord = polygons.poly
        eval_poly_coord = eval(poly_coord)
        polygon = Polygon(eval_poly_coord)
        if polygon.contains(point):
            selected_poly.append(polygons)

    if len(selected_poly) == 0:
        return Response('No Provider available')

    serializer = QuerySerializer(selected_poly, many=True)
    return Response(serializer.data)


class Query(generics.ListAPIView):
    """
    Class based implementation of query function. Not used
    """
    serializer_class = QuerySerializer

    def queryset(self):
        lat = request.GET.get('lat', None)
        long = request.GET.get('long', None)

        if lat is None or long is None:
            return HttpResponse('Wrong')

        point = Point(float(lat), float(long))
        selected_poly = []
        queryset = GeoPolygon.objects.all()
        for polygons in queryset:
            poly_coord = polygons.poly
            eval_poly_coord = eval(poly_coord)
            polygon = Polygon(eval_poly_coord)
            if polygon.contains(point):
                selected_poly.append(polygons)

        return selected_poly
