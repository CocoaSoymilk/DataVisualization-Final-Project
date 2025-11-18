# 🚗 서울시 교통사고 안전 대시보드

서울시 25개 자치구의 교통사고 데이터를 분석하고 시각화하는 인터랙티브 웹 대시보드입니다.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/dash-2.0+-green.svg)
![Plotly](https://img.shields.io/badge/plotly-5.0+-red.svg)

## 📊 주요 기능

### 🎛️ 인터랙티브 필터
- **연도 범위 선택**: 슬라이더로 분석 기간 조정
- **자치구 선택**: 특정 지역 집중 분석
- **기상 조건**: 날씨별 사고 패턴 분석
- **지도 지표**: 사상자수/사망자수/발생건수 선택

### 🗺️ 시각화
1. **서울시 자치구별 지도**: Choropleth 맵으로 지역별 사고 현황 표시
2. **TOP 10 다발지역**: 사고 다발 자치구 순위
3. **연도별 추이**: 시계열 분석으로 트렌드 파악
4. **기상별 분석**: 날씨 조건에 따른 사고 피해 현황
5. **차종별 분석**: 차량 용도별 사고 발생 비율
6. **히트맵 분석**: 자치구×연도 2차원 사고 밀도

### 📈 통계 카드
- 총 사고 건수
- 총 사망자 수
- 총 부상자 수
- 분석 기간

## 🛠️ 기술 스택

- **Backend**: Python 3.8+
- **Framework**: Plotly Dash 2.0+
- **Data Processing**: Pandas
- **Visualization**: Plotly Express, Plotly Graph Objects
- **UI Components**: Dash Bootstrap Components
- **Data Source**: 서울 열린데이터광장

## 📁 프로젝트 구조

```
교통사고 대시보드/
├── app.py                      # 메인 대시보드 애플리케이션
├── charts.py                   # 차트 생성 함수들
├── preprocessing.py            # 데이터 전처리 함수
├── requirements.txt            # Python 패키지 의존성
├── DATA/                       # 데이터 파일
│   ├── 교통사고+현황(구별)_*.csv
│   ├── 기상상태별+교통사고+현황_*.csv
│   └── 차량용도별+교통사고+현황_*.csv
├── start_dashboard.bat         # 대시보드 실행 파일
└── install_and_run.bat         # 패키지 설치 및 실행

```

## 🚀 설치 및 실행

### 방법 1: 자동 설치 및 실행 (권장)

1. `install_and_run.bat` 파일을 더블클릭

### 방법 2: 수동 설치

1. **패키지 설치**
```bash
pip install -r requirements.txt
```

2. **대시보드 실행**
```bash
python app.py
```

3. **브라우저 접속**
```
http://localhost:8050
```

## 📦 필수 패키지

```
dash>=2.0.0
dash-bootstrap-components>=1.0.0
plotly>=5.0.0
pandas>=1.3.0
requests>=2.31.0
```

## 📊 데이터 소스

- **출처**: 서울 열린데이터광장
- **기간**: 2009년 ~ 2024년
- **지역**: 서울시 25개 자치구
- **항목**: 발생건수, 사망자수, 부상자수, 기상상태, 차량용도 등

## 🎨 주요 특징

### 반응형 디자인
- 데스크톱, 태블릿, 모바일 모두 지원
- 브레이크포인트 기반 레이아웃 조정

### 실시간 필터링
- 사용자 선택에 따라 모든 차트 즉시 업데이트
- 부드러운 인터랙션과 빠른 응답 속도

### 시각적 디자인
- 현대적인 라이트 블루 테마
- 직관적인 아이콘과 색상 구분
- 그라데이션과 그림자 효과

## 🔧 주요 함수

### `preprocessing.py`
- `load_and_clean_data()`: CSV 파일 로드 및 전처리
- `load_district_data()`: 자치구별 데이터 처리
- `load_weather_data()`: 기상별 데이터 처리
- `load_vehicle_data()`: 차종별 데이터 처리

### `charts.py`
- `create_map_chart()`: Choropleth 지도 생성
- `create_trend_chart()`: 연도별 추이 차트
- `create_weather_chart()`: 기상별 분석 차트
- `create_vehicle_chart()`: 차종별 파이 차트
- `create_heatmap_chart()`: 히트맵 차트
- `create_ranking_chart()`: TOP 10 랭킹 차트

### `app.py`
- Dash 앱 초기화 및 레이아웃 정의
- 콜백 함수로 인터랙티브 기능 구현

## 📸 스크린샷

### 전체 대시보드
![Dashboard Overview](docs/screenshot_overview.png)

### 지도 및 랭킹
![Map and Ranking](docs/screenshot_map.png)

### 상세 분석 차트
![Detail Charts](docs/screenshot_charts.png)

## 🤝 기여

이슈나 풀 리퀘스트는 언제든 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

## 👤 제작자

**[Your Name]**

## 🙏 감사의 말

- 서울 열린데이터광장 - 데이터 제공
- Plotly 커뮤니티 - 시각화 도구
- Dash 프레임워크 - 대시보드 프레임워크

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 등록해주세요.

---

⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!
