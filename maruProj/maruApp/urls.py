from . import views, viewsOfIndex, viewsOfJenre, viewsOfLocation
from django.urls import path

urlpatterns = [
    # index 페이지에서 사용
    path('index/genre_chart/', viewsOfIndex.genre_chart, name='genre-chart'),
    path('index/price_chart/', viewsOfIndex.price_by_location_chart, name='price-chart'),
    path('index/author_top_chart/', viewsOfIndex.author_top_chart, name='author-chart'),
    path('index/review_score_chart/', viewsOfIndex.review_score_chart, name='review-chart'),


    # genre 페이지에서 사용
    path('genre/', viewsOfJenre.genre_page, name='genre'),
    path('genre/data/', viewsOfJenre.genre_data, name='genre-data'),
    path('genre/gmv-data/', viewsOfJenre.genre_gmv_data, name='genre-gmv-data'),
    path('genre/top3/', viewsOfJenre.genre_top3_json, name='genre-top3-json'),
    path('genre/price-data/', viewsOfJenre.genre_price_data, name='genre-price-data'),
    path('genre/recommend-top3/', viewsOfJenre.genre_recommend_top3, name='genre-recommend-top3'),
    path('genre/heatmap/', viewsOfJenre.genre_heatmap, name='genre-heatmap'),


    # location 페이지에서 사용
    path('location/', viewsOfLocation.location_page, name='location'),
    path('location/data/', viewsOfLocation.location_data, name='location-data'),
    path('location/gmv-data/', viewsOfLocation.location_gmv_data, name='location-gmv-data'),
    path('location/top3/', viewsOfLocation.location_top3_json, name='location-top3-json'),
    path('location/price-data/', viewsOfLocation.location_price_data, name='location-price-data'),
    path('location/recommend-top3/', viewsOfLocation.location_recommend_top3, name='location-recommend-top3'),
    path('location/heatmap/', viewsOfLocation.location_heatmap, name='location-heatmap'),
]
