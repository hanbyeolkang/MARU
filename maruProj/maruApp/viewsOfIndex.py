import io
import json
import pandas as pd
from collections import Counter
from django.http import HttpResponse
from .models import Book
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
from io import BytesIO
from django.views.decorators.cache import never_cache


# Mac 한글 폰트 설정
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

# json 경로
# JSON_PATH = 'maruApp/data/test.json'    # 연습용
JSON_PATH = 'maruApp/data/bestseller_all.json'


# json 파일을 읽어서 Book 객체 리스트로 반환하는 함수
def load_books_from_json(json_path):
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
            genre=item.get('genre', ''),
        )
        books.append(book)
    return books


# 장르 분포 (원형 차트)
@never_cache
def genre_chart(request):
    books = load_books_from_json(JSON_PATH)
    
    # 카테고리별 개수 집계
    genres = [book.genre for book in books]
    counter = Counter(genres)
    labels = list(counter.keys())
    sizes = list(counter.values())

    plt.figure(figsize=(5, 4))  # 더 넓게
    # 각 카테고리별 % 계산
    total = sum(sizes)
    percent_data = sorted(
        zip(labels, sizes, [size/total*100 for size in sizes]),
        key=lambda x: x[2], reverse=True
    )
    sorted_labels = [label for label, _, _ in percent_data]
    sorted_sizes = [size for _, size, _ in percent_data]
    sorted_percent_labels = [f"{label} ({percent:.1f}%)" for label, _, percent in percent_data]

    fig = plt.figure(figsize=(7, 5))
    patches, texts = plt.pie(
        sorted_sizes,
        labels=None,
        autopct=None,
        startangle=140,
        pctdistance=0.75,
        labeldistance=1
    )
    plt.legend(
        patches,
        sorted_percent_labels,
        loc='center left',
        bbox_to_anchor=(1.0, 0.5),
        fontsize=11
    )
    plt.subplots_adjust(top=0.97, bottom=0.07)  # 여백 더 줄임
    plt.axis('equal')
    plt.tight_layout(pad=0.5)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.05)
    plt.close('all')
    buf.seek(0)
    
    response = HttpResponse(buf.getvalue(), content_type="image/png")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response


# 지역별 평균 가격 (막대 차트)
@never_cache
def price_by_location_chart(request):
    books = load_books_from_json(JSON_PATH)

    # Book 객체 → DataFrame 변환
    df = pd.DataFrame([{
        "location": b.location,
        "price": float(str(b.price).replace(",", ""))  # price 정수/문자 혼용 처리
    } for b in books])

    # 지역별 평균 가격
    avg_price = df.groupby("location")["price"].mean().sort_values()

    # 시각화
    plt.figure(figsize=(7,4))
    avg_price.plot(kind="bar", color="skyblue", edgecolor="black")
    # plt.title("지역별 평균 가격 비교", fontsize=14)
    plt.ylabel("평균 가격(원)", fontsize=12)
    plt.xlabel("지점", fontsize=12)
    plt.xticks(rotation=45)

    # PNG 이미지로 반환
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")   # format="jpg" 도 가능
    plt.close('all')
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response


# 저자별 베스트셀러 TOP10 (막대 그래프)
@never_cache
def author_top_chart(request):
    books = load_books_from_json(JSON_PATH)
    authors = [book.author for book in books]
    counter = Counter(authors)
    top_authors = counter.most_common(10) # 상위 작가 10명
    labels = [a[0] for a in top_authors]
    values = [a[1] for a in top_authors]

    plt.figure(figsize=(7, 5))
    plt.barh(labels[::-1], values[::-1], color='skyblue', edgecolor='black')
    # plt.title('저자별 베스트셀러 수 TOP 10', fontsize=14)
    plt.xlabel('도서 수', fontsize=12)
    plt.ylabel('저자명', fontsize=12)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close('all')
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Cache-Control'] = 'no-store'
    return response


# 리뷰 수 vs 평점 (산점도)
@never_cache
def review_score_chart(request):
    books = load_books_from_json(JSON_PATH)

    # Book 객체 → DataFrame 변환
    df = pd.DataFrame([{
        "review": int(str(b.num_of_review).replace(",", "").strip() or 0),
        "score": float(str(b.score).strip() or 0)
    } for b in books])

    plt.figure(figsize=(6.5, 5))
    plt.scatter(df["review"], df["score"], alpha=0.6, color="#FF6384", edgecolor='black')
    # plt.title("리뷰 수와 평점의 상관관계", fontsize=14)
    plt.xlabel("리뷰 수", fontsize=12)
    plt.ylabel("평점", fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close('all')
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Cache-Control'] = 'no-store'
    return response