"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views, viewsOfIndex, viewsOfJenre, viewsOfLocation

urlpatterns = [
    # ... (existing index and genre paths)
    # location 페이지에서 사용
    path('location/', viewsOfLocation.location_page, name='location'),
    path('location/data/', viewsOfLocation.location_data, name='location-data'),
    path('location/gmv-data/', viewsOfLocation.location_gmv_data, name='location-gmv-data'),
    path('location/top3/', viewsOfLocation.location_top3_json, name='location-top3-json'),
    path('location/price-data/', viewsOfLocation.location_price_data, name='location-price-data'),
    path('location/recommend-top3/', viewsOfLocation.location_recommend_top3, name='location-recommend-top3'),
    path('location/heatmap/', viewsOfLocation.location_heatmap, name='location-heatmap'),
]