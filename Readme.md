# DE7 1차 프로젝트
## 2팀 마루

# MARU Book Analysis
A Django-based web service for analyzing bestseller books by main, genre and location.
Django 기반 웹 서비스로, 메인/장르별/지역별 베스트셀러 도서를 분석하고 시각화합니다.


* 실행 전 설치
```
$ pip install django
$ pip install djangorestframework
$ pip install matplotlib
$ pip install pandas
```


## 기술 스택
- Python 3.11
- Django 5.x
- Pandas, Matplotlib
- PostgreSQL / SQLite
- HTML, CSS, JavaScript (Chart.js)


## 폴더 구조
MARU/
├─ maruProj/
│  ├─ maruSite/               
│  │  ├─ static/               # CSS, JS 등 정적 파일
│  │  │  └─ maru/
│  │  │     ├─ css/            # 공통 CSS
│  │  │     └─ js/             # 공통 JS
│  │  ├─ templates/            # HTML 템플릿
│  │  │  └─ maru/
│  │  │     └─ genre.html      # 장르별 분석 페이지
│  │  ├─ views.py              # 뷰 로직 (페이지 렌더링, API 처리)
│  │  └─ urls.py               # URL 라우팅
│  ├─ manage.py                
│  └─ settings.py              
├─ .gitignore                  
└─ README.md                   


## 주요 기능
장르별 베스트셀러 분석
지역별 추천 도서 Top3 조회
차트 시각화 (Chart.js, Matplotlib)
REST API 제공 (Django REST Framework)


## 실행 방법
# 개발 서버 실행
python manage.py runserver

# 브라우저에서 확인
http://127.0.0.1:8000/


## 기대 효과
장르/지역별 베스트셀러 분석
차트 시각화 (Chart.js, Matplotlib)
통계 기반 추천 시스템 구성 기초 구현
REST API 제공 (Django REST Framework)
