from django.urls import path
from .views import (PolygonCreateView, PolygonDetailView,
                    get_polygons_with_specified_point)

urlpatterns = [
    path('create/', PolygonCreateView.as_view()),
    path('get/<pk>/', PolygonDetailView.as_view()),
    path('search-point/', get_polygons_with_specified_point)

]
