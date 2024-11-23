from django.urls import path
from . import views
from .views import RouteDetailView, ProductListView

urlpatterns = [
    path('', views.home_page, name='home page'),
    path('routes/', views.route_view, name='add route page'),
    path('route/<int:pk>/', RouteDetailView.as_view(), name='route detail'),
    path('allroutes', ProductListView.as_view(), name='routes list'),
]
