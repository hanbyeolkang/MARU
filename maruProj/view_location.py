import io 
import json
import os
import re
import random
from collections import Counter

import matplotlib 
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd
from django.conf import settings
from django.http import JsonResponse, HttpResponse 
from django.shortcuts import render
from django.db.models import F, FloatField, Sum

from .models import Book

# Use the same data file as genre analysis
JSON_PATH = os.path.join(settings.BASE_DIR, 'maruApp', 'data', 'bestseller_all.json')

def load_books_from_json(json_path):
    """JSON 파일을 로드하여 Book 객체 리스트 반환"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    books = []
    for item in data:
        book = Book(
            location=item.get('location', ''),
            ranking=item.get('ranking', 0),
            book_number=item.get('book_number', ''),
            title=item.get('title', ''),
            book_detail=item.get('book_detail', ''),
            book_img=item.get('book_img', ''),
            author=item.get('author', ''),
            publisher=item.get('publisher', ''),
            price=item.get('price', 0),
            score=item.get('score', 0),
            num_of_review=item.get('num_of_review', 0),
            genre=item.get('genre', '')
        )
        books.append(book)
    return books

def location_page(request):
    """지역 페이지 HTML 렌더"""
    top_books_list = None  # (Optional context if needed, similar to genre_page)
    return render(request, 'maru/location.html', {'top_books_list': top_books_list})

def location_data(request):
    """지역별 권수 + 퍼센트 JSON 반환"""
    books = load_books_from_json(JSON_PATH)
    locations = [book.location for book in books]
    counter = Counter(locations)
    total = sum(counter.values())
    data = []
    for loc, count in counter.items():
        percent = round(count / total * 100, 1) if total else 0
        data.append({'location': loc, 'count': count, 'percent': percent})
    return JsonResponse(data, safe=False)

def location_gmv_data(request):
    """지역별 GMV 및 평균 통계 JSON 반환"""
    books = load_books_from_json(JSON_PATH)
    location_stats = {}
    for book in books:
        # 가격, 리뷰수, 평점 숫자 추출 및 변환
        try:
            price_str = str(book.price)
            price_val = float(re.sub(r'[^0-9.]', '', price_str)) if price_str else 0
            reviews_str = str(book.num_of_review)
            reviews_val = int(re.sub(r'[^0-9]', '', reviews_str)) if reviews_str else 0
            score_str = str(book.score)
            score_val = float(re.sub(r'[^0-9.]', '', score_str)) if score_str else 0
        except ValueError:
            price_val, reviews_val, score_val = 0, 0, 0
        gmv = price_val * reviews_val * score_val
        loc = book.location
        if loc not in location_stats:
            location_stats[loc] = {
                "gmv": 0,
                "price_sum": 0,
                "review_sum": 0,
                "score_sum": 0,
                "count": 0
            }
        location_stats[loc]["gmv"] += gmv
        location_stats[loc]["price_sum"] += price_val
        location_stats[loc]["review_sum"] += reviews_val
        location_stats[loc]["score_sum"] += score_val
        location_stats[loc]["count"] += 1
    # 평균 계산 및 결과 구성
    data = []
    for loc, stats in location_stats.items():
        c = stats["count"]
        avg_price = stats["price_sum"] / c if c else 0
        avg_reviews = stats["review_sum"] / c if c else 0
        avg_score = stats["score_sum"] / c if c else 0
        data.append({
            "location": loc,
            "gmv": round(stats["gmv"], 2),
            "price": round(avg_price, 2),
            "num_of_review": int(avg_reviews),
            "score": round(avg_score, 2)
        })
    return JsonResponse(data, safe=False)

def location_top3_json(request):
    """지역별 Top3 책 리스트 JSON 반환"""
    books = load_books_from_json(JSON_PATH)
    # Prepare DataFrame with numeric values for computing GMV
    data = []
    for b in books:
        if not b.book_img:
            continue  # skip entries without image (likely incomplete data)
        # Convert strings to numeric values for price, reviews, score
        price_val = float(re.sub(r'[^0-9.]', '', str(b.price))) if b.price else 0
        reviews_val = int(re.sub(r'[^0-9]', '', str(b.num_of_review))) if b.num_of_review else 0
        score_val = float(re.sub(r'[^0-9.]', '', str(b.score))) if b.score else 0
        gmv_val = price_val * reviews_val * score_val
        data.append({
            'location': b.location,
            'title': b.title,
            'author': b.author,
            'book_img': b.book_img,
            'book_detail': b.book_detail,
            'book_number': getattr(b, 'book_number', None),
            'gmv': gmv_val
        })
    df = pd.DataFrame(data)
    # Remove duplicate books (same book_number) keeping highest GMV entry
    if 'book_number' in df.columns:
        df = df.sort_values('gmv', ascending=False).drop_duplicates(subset='book_number')
    else:
        df = df.sort_values('gmv', ascending=False).drop_duplicates(subset=['title', 'author'])
    # For each location, take top 3 by GMV
    result = {}
    for loc, group in df.groupby('location'):
        top3 = group.sort_values('gmv', ascending=False).head(3)
        # Include title, author, image, detail (and GMV if needed)
        result[loc] = top3[['title', 'author', 'book_img', 'book_detail', 'gmv']].to_dict(orient='records')
    return JsonResponse(result, safe=False)

def location_price_data(request):
    """지역별 가격 통계 JSON 반환"""
    books = load_books_from_json(JSON_PATH)
    price_entries = []
    for b in books:
        if not b.price:
            continue
        price_val = float(re.sub(r'[^0-9.]', '', str(b.price))) if b.price else 0
        price_entries.append({'location': b.location, 'price': price_val})
    df = pd.DataFrame(price_entries)
    # Compute mean, max, min price per location
    stats = df.groupby('location')['price'].agg(['mean', 'max', 'min']).reset_index()
    stats = stats.round(2)
    result = stats.to_dict(orient='records')
    return JsonResponse(result, safe=False)

def location_recommend_top3(request):
    """추천 책 3권 JSON 반환 (지역 분석 페이지용)"""
    books = load_books_from_json(JSON_PATH)
    data = []
    for b in books:
        if not b.book_img:
            continue
        try:
            score_val = float(re.sub(r'[^0-9.]', '', str(b.score))) if b.score else 0
            reviews_val = int(re.sub(r'[^0-9]', '', str(b.num_of_review))) if b.num_of_review else 0
            rank_val = int(re.sub(r'[^0-9]', '', str(b.ranking))) if b.ranking else 0
        except:
            score_val, reviews_val, rank_val = 0, 0, 0
        data.append({
            'title': b.title,
            'book_img': b.book_img,
            'book_detail': b.book_detail,
            'score': score_val,
            'num_of_review': reviews_val,
            'ranking': rank_val
        })
    df = pd.DataFrame(data)
    # Compute a recommendation score (without price, focusing on score, reviews, ranking)
    df['recommend_score'] = df['score'] * 0.5 + df['num_of_review'] * 2 + (100 - df['ranking']) * 0.1
    # Take top 25 by recommendation score, drop duplicates by title to avoid repeats
    top25 = df.sort_values('recommend_score', ascending=False).head(25)
    top25 = top25.drop_duplicates(subset='title')
    # Randomly select 3 books from these top candidates
    recommended = top25.sample(3) if len(top25) >= 3 else top25
    result = recommended[['title', 'book_img', 'book_detail']].to_dict(orient='records')
    return JsonResponse(result, safe=False)

def location_heatmap(request):
    """지역별 price/score/reviews/GMV 히트맵용 JSON 반환"""
    books = load_books_from_json(JSON_PATH)
    records = []
    for b in books:
        # Extract numeric values
        price_val = float(re.sub(r'[^0-9.]', '', str(b.price))) if b.price else 0
        score_val = float(re.sub(r'[^0-9.]', '', str(b.score))) if b.score else 0
        reviews_val = int(re.sub(r'[^0-9]', '', str(b.num_of_review))) if b.num_of_review else 0
        gmv_val = price_val * score_val * reviews_val
        records.append({
            'location': b.location,
            'price': price_val,
            'score': score_val,
            'num_of_review': reviews_val,
            'gmv': gmv_val
        })
    df = pd.DataFrame(records)
    # Calculate average metrics per location
    loc_avg = df.groupby('location')[['price', 'score', 'num_of_review', 'gmv']].mean().round(2)
    result = loc_avg.to_dict(orient='index')
    # `result` format: { "LocationName": {"price": ..., "score": ..., "num_of_review": ..., "gmv": ...}, ... }
    return JsonResponse(result, safe=False)
