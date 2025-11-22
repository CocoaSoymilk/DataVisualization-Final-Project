"""
서울시 교통사고 인터랙티브 대시보드
Plotly Dash 기반 웹 애플리케이션 - 새로운 레이아웃 (사이드바)
"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from preprocessing import load_and_clean_data
from charts import (
    create_trend_chart,
    create_weather_chart,
    create_vehicle_chart,
    create_heatmap_chart,
    create_ranking_chart,
    create_map_chart
)

# 데이터 로드 (전역 변수)
print("=" * 70)
print("📊 데이터 로딩 중...")
print("=" * 70)
df_weather, df_vehicle, df_district = load_and_clean_data()

# 2020~2024년 데이터만 필터링
df_weather = df_weather[df_weather['연도'].between(2020, 2024)]
df_vehicle = df_vehicle[df_vehicle['연도'].between(2020, 2024)]
df_district = df_district[df_district['연도'].between(2020, 2024)]

print("\n✅ 데이터 로딩 완료! (2020~2024년)\n")

# 년도 범위
years = sorted(df_district['연도'].unique())
min_year, max_year = 2020, 2024

# 자치구 목록
districts = sorted(df_district['자치구'].unique())

# 기상 조건 목록
weather_conditions = ['맑음', '흐림', '비', '안개', '눈', '기타/불명']

# Dash 앱 초기화
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,  # 다크 테마
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
    ],
    suppress_callback_exceptions=True
)

# ✅ Render 배포를 위한 server 변수 추가
server = app.server

app.title = "서울시 교통사고 대시보드"

# 커스텀 스타일
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                color: #1e293b;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
            }
            .card {
                background: #ffffff !important;
                border: 1px solid #bfdbfe !important;
                box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15) !important;
                transition: all 0.3s ease !important;
            }
            .card:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 30px rgba(59, 130, 246, 0.25) !important;
            }
            .card-header {
                background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%) !important;
                border-bottom: none !important;
                color: #ffffff !important;
                font-weight: 600 !important;
            }
            h1, h2, h3, h4, h5 {
                color: #1e40af !important;
                text-shadow: none;
            }
            .Select-control, .dash-dropdown {
                background-color: #ffffff !important;
                border: 1px solid #93c5fd !important;
                color: #1e293b !important;
            }
            input[type="checkbox"] {
                accent-color: #3b82f6;
            }
            hr {
                border-color: #93c5fd !important;
                opacity: 0.6;
            }
            
            /* 사이드바 스타일 */
            .sidebar {
                position: fixed;
                top: 0;
                left: 0;
                height: 100vh;
                width: 280px;
                background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                border-right: 2px solid #bfdbfe;
                box-shadow: 4px 0 20px rgba(59, 130, 246, 0.1);
                overflow-y: auto;
                z-index: 1000;
                padding: 20px;
            }
            
            .sidebar::-webkit-scrollbar {
                width: 8px;
            }
            
            .sidebar::-webkit-scrollbar-track {
                background: #f1f5f9;
                border-radius: 10px;
            }
            
            .sidebar::-webkit-scrollbar-thumb {
                background: #3b82f6;
                border-radius: 10px;
            }
            
            .main-content {
                margin-left: 300px;
                padding: 20px;
                min-height: 100vh;
            }
            
            @media (max-width: 992px) {
                .sidebar {
                    position: relative;
                    width: 100%;
                    height: auto;
                }
                .main-content {
                    margin-left: 0;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# 레이아웃
app.layout = html.Div([
    # 왼쪽 사이드바 (고정)
    html.Div([
        # 로고/제목
        html.Div([
            html.H3([
                html.I(className="fas fa-car-crash", 
                       style={"margin-right": "10px", "color": "#3b82f6"}),
                "FILTERS"
            ], style={
                "color": "#1e40af",
                "margin-bottom": "10px",
                "font-size": "1.3rem",
                "font-weight": "700",
                "letter-spacing": "1px"
            }),
            html.Hr(style={"border-color": "#3b82f6", "opacity": "0.5"}),
        ], style={"margin-bottom": "25px"}),
        
        # 연도 범위 필터
        html.Div([
            html.Label([
                html.I(className="fas fa-calendar-check", 
                       style={"margin-right": "8px", "color": "#3b82f6"}),
                "연도 범위"
            ], style={
                "font-weight": "bold",
                "font-size": "0.95rem",
                "color": "#1e293b",
                "margin-bottom": "10px",
                "display": "block"
            }),
            dcc.RangeSlider(
                id='year-slider',
                min=min_year,
                max=max_year,
                value=[min_year, max_year],
                marks={str(year): {
                    'label': str(year),
                    'style': {'font-weight': 'bold', 'font-size': '0.75rem', 'color': '#1e293b'}
                } for year in years},
                step=1,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={"margin-bottom": "30px"}),
        
        # 자치구 선택
        html.Div([
            html.Label([
                html.I(className="fas fa-map-marked-alt", 
                       style={"margin-right": "8px", "color": "#3b82f6"}),
                "자치구 선택"
            ], style={
                "font-weight": "bold",
                "font-size": "0.95rem",
                "color": "#1e293b",
                "margin-bottom": "10px",
                "display": "block"
            }),
            dcc.Dropdown(
                id='district-dropdown',
                options=[{'label': dist, 'value': dist} for dist in districts],
                value=[],
                multi=True,
                placeholder="전체 자치구",
                style={"font-size": "0.9rem"}
            )
        ], style={"margin-bottom": "30px"}),
        
        # 기상 조건 선택
        html.Div([
            html.Label([
                html.I(className="fas fa-cloud-sun", 
                       style={"margin-right": "8px", "color": "#3b82f6"}),
                "기상 조건"
            ], style={
                "font-weight": "bold",
                "font-size": "0.95rem",
                "color": "#1e293b",
                "margin-bottom": "10px",
                "display": "block"
            }),
            dcc.Checklist(
                id='weather-checklist',
                options=[{'label': w, 'value': w} for w in weather_conditions],
                value=weather_conditions,
                style={"font-size": "0.85rem"},
                labelStyle={"display": "block", "margin-bottom": "8px"}
            )
        ], style={"margin-bottom": "30px"}),
        
        
        # 푸터 정보
        html.Hr(style={"border-color": "#3b82f6", "opacity": "0.3", "margin-top": "30px"}),
        html.Div([
            html.P([
                html.I(className="fas fa-database", 
                       style={"margin-right": "5px", "color": "#3b82f6"}),
                "2020-2024"
            ], style={"font-size": "0.8rem", "color": "#64748b", "margin-bottom": "5px"}),
            html.P([
                html.I(className="fas fa-map-marked-alt", 
                       style={"margin-right": "5px", "color": "#3b82f6"}),
                "25개 자치구"
            ], style={"font-size": "0.8rem", "color": "#64748b", "margin-bottom": "5px"}),
        ])
        
    ], className="sidebar"),
    
    # 오른쪽 메인 콘텐츠
    html.Div([
        # 헤더
        html.Div([
            html.H1(
                [html.I(className="fas fa-car-crash", 
                        style={"margin-right": "15px", "color": "#3b82f6"}),
                 "서울시 교통사고 안전 대시보드"],
                style={
                    "color": "#1e40af",
                    "font-weight": "700",
                    "letter-spacing": "2px",
                    "margin-bottom": "10px"
                }
            ),
            html.P(
                "Seoul Traffic Accident Safety Dashboard",
                style={
                    "font-size": "1.1rem",
                    "color": "#64748b",
                    "letter-spacing": "1px",
                    "margin-bottom": "20px"
                }
            ),
            html.Hr(style={
                "border-top": "3px solid #3b82f6",
                "opacity": "0.3",
                "margin-bottom": "30px"
            })
        ]),
        
        # 통계 카드 (1행 4열)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.I(className="fas fa-exclamation-triangle fa-2x",
                               style={"color": "#3b82f6", "margin-bottom": "10px"}),
                        html.H6("TOTAL ACCIDENTS",
                               style={"color": "#64748b", "font-size": "0.75rem", "letter-spacing": "1px"}),
                        html.H2([
                            html.Span(f"{df_district['발생건수'].sum():,.0f}",
                                     id="total-accidents",
                                     style={"color": "#1e40af", "font-weight": "700"}),
                            html.Span(" 건", style={"color": "#64748b", "font-size": "1.2rem", "font-weight": "500"})
                        ], style={"margin": "10px 0"})
                    ], style={"text-align": "center"})
                ], style={
                    "border": "2px solid #3b82f6",
                    "box-shadow": "0 4px 15px rgba(59, 130, 246, 0.2)"
                })
            ], width=12, lg=3, md=6, className="mb-3"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.I(className="fas fa-skull-crossbones fa-2x",
                               style={"color": "#ef4444", "margin-bottom": "10px"}),
                        html.H6("DEATHS",
                               style={"color": "#64748b", "font-size": "0.75rem", "letter-spacing": "1px"}),
                        html.H2([
                            html.Span(f"{df_district['사망자수'].sum():,.0f}",
                                     id="total-deaths",
                                     style={"color": "#dc2626", "font-weight": "700"}),
                            html.Span(" 명", style={"color": "#64748b", "font-size": "1.2rem", "font-weight": "500"})
                        ], style={"margin": "10px 0"})
                    ], style={"text-align": "center"})
                ], style={
                    "border": "2px solid #ef4444",
                    "box-shadow": "0 4px 15px rgba(239, 68, 68, 0.2)"
                })
            ], width=12, lg=3, md=6, className="mb-3"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.I(className="fas fa-user-injured fa-2x",
                               style={"color": "#f59e0b", "margin-bottom": "10px"}),
                        html.H6("INJURIES",
                               style={"color": "#64748b", "font-size": "0.75rem", "letter-spacing": "1px"}),
                        html.H2([
                            html.Span(f"{df_district['부상자수'].sum():,.0f}",
                                     id="total-injuries",
                                     style={"color": "#d97706", "font-weight": "700"}),
                            html.Span(" 명", style={"color": "#64748b", "font-size": "1.2rem", "font-weight": "500"})
                        ], style={"margin": "10px 0"})
                    ], style={"text-align": "center"})
                ], style={
                    "border": "2px solid #f59e0b",
                    "box-shadow": "0 4px 15px rgba(245, 158, 11, 0.2)"
                })
            ], width=12, lg=3, md=6, className="mb-3"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.I(className="fas fa-clock fa-2x",
                               style={"color": "#06b6d4", "margin-bottom": "10px"}),
                        html.H6("PERIOD",
                               style={"color": "#64748b", "font-size": "0.75rem", "letter-spacing": "1px"}),
                        html.H2([
                            html.Span(f"{min_year}~{max_year}",
                                     style={"color": "#0891b2", "font-weight": "700"})
                        ], style={"margin": "10px 0"})
                    ], style={"text-align": "center"})
                ], style={
                    "border": "2px solid #06b6d4",
                    "box-shadow": "0 4px 15px rgba(6, 182, 212, 0.2)"
                })
            ], width=12, lg=3, md=6, className="mb-3"),
        ], className="mb-4"),
        
        # 2x2 그리드 레이아웃
        # 첫 번째 행 (지도 + 랭킹)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-map-marked-alt",
                               style={"margin-right": "8px"}),
                        "서울시 자치구별 지도"
                    ]),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='map-metric-dropdown',
                            options=[
                                {'label': '총 사상자 수', 'value': 'total'},
                                {'label': '사망자 수', 'value': 'deaths'},
                                {'label': '부상자 수', 'value': 'injuries'},
                                {'label': '발생 건수', 'value': 'count'}
                            ],
                            value='total',
                            clearable=False,
                            style={"margin-bottom": "10px"}
                        ),
                        dcc.Graph(id='map-chart', config={'displayModeBar': False},
                                 style={"height": "500px"})
                    ])
                ], className="mb-3")
            ], width=12, lg=6, md=12),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-trophy",
                               style={"margin-right": "8px"}),
                        "TOP 10 다발지역"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='ranking-chart', config={'displayModeBar': False},
                                 style={"height": "500px"})
                    ])
                ], className="mb-3")
            ], width=12, lg=6, md=12),
        ]),
        
        # 두 번째 행 (연도별 + 기상별)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-chart-line",
                               style={"margin-right": "8px"}),
                        "연도별 추이"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='trend-chart', config={'displayModeBar': False},
                                 style={"height": "500px"})
                    ])
                ], className="mb-3")
            ], width=12, lg=6, md=12),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-cloud-sun",
                               style={"margin-right": "8px"}),
                        "기상별 분석"
                    ]),
                    dbc.CardBody([
                        dcc.RadioItems(
                            id='weather-metric-radio',
                            options=[
                                {'label': ' 사망자', 'value': 'deaths'},
                                {'label': ' 부상자', 'value': 'injuries'}
                            ],
                            value='deaths',
                            inline=True,
                            style={"margin-bottom": "10px"},
                            labelStyle={"margin-right": "15px"}
                        ),
                        dcc.Graph(id='weather-chart', config={'displayModeBar': False},
                                 style={"height": "470px"})
                    ])
                ], className="mb-3")
            ], width=12, lg=6, md=12),
        ]),
        
        # 세 번째 행 (차종별 + 히트맵을 2x1로 - 히트맵이 더 크게)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-car",
                               style={"margin-right": "8px"}),
                        "차종별 분석"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='vehicle-chart', config={'displayModeBar': False},
                                 style={"height": "700px"})
                    ])
                ], className="mb-3")
            ], width=12, lg=6, md=12),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-th",
                               style={"margin-right": "8px"}),
                        "자치구 × 연도 히트맵"
                    ]),
                    dbc.CardBody([
                        html.Div([
                            dcc.Graph(id='heatmap-chart', config={'displayModeBar': False},
                                     style={"height": "650px", "width": "100%"})
                        ], style={"max-height": "650px", "overflow": "hidden"})
                    ], style={"padding": "10px", "overflow": "hidden"})
                ], className="mb-3", style={"max-height": "730px", "overflow": "hidden"})
            ], width=12, lg=6, md=12),
        ]),
        
        # 푸터
        html.Hr(style={"border-top": "2px solid #3b82f6", "opacity": "0.3", "margin-top": "40px"}),
        html.Div([
            html.P([
                html.I(className="fas fa-copyright", style={"margin-right": "5px"}),
                "2024 서울시 교통사고 안전 대시보드"
            ], style={"color": "#94a3b8", "font-size": "0.9rem", "text-align": "center", "margin-bottom": "10px"}),
            html.P([
                html.I(className="fas fa-database", style={"margin-right": "5px"}),
                "데이터 출처: 서울 열린데이터광장"
            ], style={"color": "#94a3b8", "font-size": "0.9rem", "text-align": "center"})
        ], style={"padding": "20px 0"})
        
    ], className="main-content")
], style={"margin": "0", "padding": "0"})


# 콜백: 모든 차트 업데이트
@app.callback(
    [
        Output('map-chart', 'figure'),
        Output('trend-chart', 'figure'),
        Output('weather-chart', 'figure'),
        Output('vehicle-chart', 'figure'),
        Output('heatmap-chart', 'figure'),
        Output('ranking-chart', 'figure'),
        Output('total-accidents', 'children'),
        Output('total-deaths', 'children'),
        Output('total-injuries', 'children'),
    ],
    [
        Input('year-slider', 'value'),
        Input('district-dropdown', 'value'),
        Input('weather-checklist', 'value'),
        Input('map-metric-dropdown', 'value'),
        Input('weather-metric-radio', 'value')
    ]
)
def update_charts(year_range, selected_districts, selected_weather, map_metric, weather_metric):
    """모든 차트와 통계를 업데이트"""
    
    try:
        # 데이터 필터링
        # 1. 연도 필터
        df_dist_filtered = df_district[
            (df_district['연도'] >= year_range[0]) &
            (df_district['연도'] <= year_range[1])
        ].copy()
        
        df_weather_filtered = df_weather[
            (df_weather['연도'] >= year_range[0]) &
            (df_weather['연도'] <= year_range[1])
        ].copy()
        
        df_vehicle_filtered = df_vehicle[
            (df_vehicle['연도'] >= year_range[0]) &
            (df_vehicle['연도'] <= year_range[1])
        ].copy()
        
        # 2. 자치구 필터
        if selected_districts and len(selected_districts) > 0:
            df_dist_filtered = df_dist_filtered[df_dist_filtered['자치구'].isin(selected_districts)]
            df_weather_filtered = df_weather_filtered[df_weather_filtered['자치구'].isin(selected_districts)]
            df_vehicle_filtered = df_vehicle_filtered[df_vehicle_filtered['자치구'].isin(selected_districts)]
        
        # 3. 기상 필터
        if selected_weather and len(selected_weather) > 0:
            df_weather_filtered = df_weather_filtered[
                df_weather_filtered['기상상태'].isin(selected_weather + ['소계'])
            ]
        
        # 빈 데이터 체크
        if len(df_dist_filtered) == 0:
            df_dist_filtered = df_district.copy()
        if len(df_weather_filtered) == 0:
            df_weather_filtered = df_weather.copy()
        if len(df_vehicle_filtered) == 0:
            df_vehicle_filtered = df_vehicle.copy()
        
        # 차트 생성
        fig_map = create_map_chart(df_dist_filtered, map_metric)
        fig_trend = create_trend_chart(df_dist_filtered, selected_districts)
        fig_weather = create_weather_chart(df_weather_filtered, weather_metric)
        fig_vehicle = create_vehicle_chart(df_vehicle_filtered)
        fig_heatmap = create_heatmap_chart(df_dist_filtered)
        fig_ranking = create_ranking_chart(df_dist_filtered)
        
        # 통계 업데이트 (숫자만 반환, 단위는 HTML에서 처리)
        total_accidents = f"{df_dist_filtered['발생건수'].sum():,.0f}"
        total_deaths = f"{df_dist_filtered['사망자수'].sum():,.0f}"
        total_injuries = f"{df_dist_filtered['부상자수'].sum():,.0f}"
        
        return (
            fig_map, fig_trend, fig_weather, fig_vehicle,
            fig_heatmap, fig_ranking,
            total_accidents, total_deaths, total_injuries
        )
    
    except Exception as e:
        print(f"❌ 콜백 에러: {e}")
        import traceback
        traceback.print_exc()
        
        # 에러 발생 시 기본 차트 반환
        return (
            create_map_chart(df_district, 'total'),
            create_trend_chart(df_district, []),
            create_weather_chart(df_weather, 'both'),
            create_vehicle_chart(df_vehicle),
            create_heatmap_chart(df_district),
            create_ranking_chart(df_district),
            "N/A", "N/A", "N/A"
        )


# ✅ 배포용으로 수정
if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 대시보드 실행 중...")
    print("=" * 70)
    print("📍 URL: http://127.0.0.1:8050")
    print("⏹️  종료: Ctrl + C")
    print("=" * 70 + "\n")
    
    app.run_server(debug=False, host='0.0.0.0', port=8050)
