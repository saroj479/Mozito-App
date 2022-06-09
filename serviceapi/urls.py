from django.contrib import admin
from django.urls import path, include
from serviceapi.views import index, ProviderDetail, ProviderList, GeoPolygonDetail, GeoPolygonList, query

urlpatterns = [
    path('', index),
    path('new_providers/', ProviderList.as_view()),
    path('providers/<int:pk>/', ProviderDetail.as_view()),
    path('new_polygons/', GeoPolygonList.as_view()),
    path('polygons/<int:pk>/', GeoPolygonDetail.as_view()),
    path('query/', query),
]
