from . import views, viewsOfIndex
from django.urls import path

urlpatterns = [
    # index 페이지에서 사용
    path('index/genre_chart/', viewsOfIndex.genre_chart, name='genre-chart'),
    path('index/price_chart/', viewsOfIndex.price_by_location_chart, name='price-chart'),
    path('index/author_top_chart/', viewsOfIndex.author_top_chart, name='author-chart'),
    path('index/review_score_chart/', viewsOfIndex.review_score_chart, name='review-chart'),

    # genre 페이지에서 사용

    # location 페이지에서 사용
]
