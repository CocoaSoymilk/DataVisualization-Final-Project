"""
서울시 교통사고 인터랙티브 대시보드
Plotly Dash 기반 웹 애플리케이션
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
print("\n✅ 데이터 로딩 완료!\n")

# 년도 범위
years = sorted(df_district['연도'].unique())
min_year, max_year = min(years), max(years)

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

app.title = "서울시 교통사고 대시보드"

# 다크 테마 커스텀 스타일
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
            .stat-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
                border: 2px solid #3b82f6 !important;
                border-radius: 12px !important;
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
            .text-muted {
                color: #64748b !important;
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
app.layout = dbc.Container([
        # 헤더
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1(
                        [html.I(className="fas fa-car-crash", 
                                style={"margin-right": "15px", "color": "#3b82f6"}),
                         "서울시 교통사고 안전 대시보드"],
                        className="text-center mb-3",
                        style={
                            "color": "#1e40af", 
                            "font-weight": "700",
                            "letter-spacing": "2px"
                        }
                    ),
                    html.P(
                        [html.I(className="fas fa-chart-line", 
                                style={"margin-right": "8px", "color": "#3b82f6"}),
                         f"서울시 25개 자치구 실시간 데이터 분석  |  {min_year}~{max_year}년"],
                        className="text-center",
                        style={
                            "font-size": "1.1rem", 
                            "color": "#64748b",
                            "letter-spacing": "1px"
                        }
                    ),
                    html.Hr(style={
                        "border-top": "3px solid #3b82f6",
                        "opacity": "0.3"
                    })
                ])
            ])
        ], className="mb-4"),
    
        # 통계 카드
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-exclamation-triangle fa-2x", 
                                   style={
                                       "color": "#3b82f6",
                                       "margin-bottom": "10px"
                                   }),
                            html.H6("TOTAL ACCIDENTS", 
                                   className="mt-2", 
                                   style={
                                       "color": "#64748b",
                                       "letter-spacing": "2px",
                                       "font-size": "0.75rem"
                                   }),
                            html.H1(f"{df_district['발생건수'].sum():,.0f}", 
                                    className="mb-0", 
                                    style={
                                        "color": "#1e40af",
                                        "font-weight": "700",
                                        "font-size": "2.5rem"
                                    },
                                    id="total-accidents")
                        ], className="text-center")
                    ])
                ], style={
                    "border": "2px solid #3b82f6",
                    "box-shadow": "0 4px 15px rgba(59, 130, 246, 0.2)",
                    "background": "linear-gradient(135deg, #ffffff 0%, #eff6ff 100%)"
                })
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-skull-crossbones fa-2x", 
                                   style={
                                       "color": "#ef4444",
                                       "margin-bottom": "10px"
                                   }),
                            html.H6("DEATHS", 
                                   className="mt-2", 
                                   style={
                                       "color": "#64748b",
                                       "letter-spacing": "2px",
                                       "font-size": "0.75rem"
                                   }),
                            html.H1(f"{df_district['사망자수'].sum():,.0f}", 
                                    className="mb-0", 
                                    style={
                                        "color": "#dc2626",
                                        "font-weight": "700",
                                        "font-size": "2.5rem"
                                    },
                                    id="total-deaths")
                        ], className="text-center")
                    ])
                ], style={
                    "border": "2px solid #ef4444",
                    "box-shadow": "0 4px 15px rgba(239, 68, 68, 0.2)",
                    "background": "linear-gradient(135deg, #ffffff 0%, #fef2f2 100%)"
                })
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-user-injured fa-2x", 
                                   style={
                                       "color": "#f59e0b",
                                       "margin-bottom": "10px"
                                   }),
                            html.H6("INJURIES", 
                                   className="mt-2", 
                                   style={
                                       "color": "#64748b",
                                       "letter-spacing": "2px",
                                       "font-size": "0.75rem"
                                   }),
                            html.H1(f"{df_district['부상자수'].sum():,.0f}", 
                                    className="mb-0", 
                                    style={
                                        "color": "#d97706",
                                        "font-weight": "700",
                                        "font-size": "2.5rem"
                                    },
                                    id="total-injuries")
                        ], className="text-center")
                    ])
                ], style={
                    "border": "2px solid #f59e0b",
                    "box-shadow": "0 4px 15px rgba(245, 158, 11, 0.2)",
                    "background": "linear-gradient(135deg, #ffffff 0%, #fffbeb 100%)"
                })
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-database fa-2x", 
                                   style={
                                       "color": "#06b6d4",
                                       "margin-bottom": "10px"
                                   }),
                            html.H6("PERIOD", 
                                   className="mt-2", 
                                   style={
                                       "color": "#64748b",
                                       "letter-spacing": "2px",
                                       "font-size": "0.75rem"
                                   }),
                            html.H1(f"{max_year - min_year + 1}년", 
                                    className="mb-0", 
                                    style={
                                        "color": "#0891b2",
                                        "font-weight": "700",
                                        "font-size": "2.5rem"
                                    })
                        ], className="text-center")
                    ])
                ], style={
                    "border": "2px solid #06b6d4",
                    "box-shadow": "0 4px 15px rgba(6, 182, 212, 0.2)",
                    "background": "linear-gradient(135deg, #ffffff 0%, #ecfeff 100%)"
                })
            ], width=3),
        ], className="mb-3", style={"margin-bottom": "20px"}),
    
        # 필터 영역 (상단 가로 배치)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H4([
                                html.I(className="fas fa-sliders-h", 
                                       style={
                                           "margin-right": "10px",
                                           "color": "#3b82f6"
                                       }),
                                "FILTERS"
                            ], style={
                                "color": "#1e40af",
                                "margin-bottom": "15px",
                                "letter-spacing": "1px",
                                "font-size": "1.1rem"
                            }),
                            
                            # 필터들을 가로로 배치
                            dbc.Row([
                                # 연도 필터
                                dbc.Col([
                                    html.Div([
                                        html.I(className="fas fa-calendar-check", 
                                               style={"margin-right": "8px", "color": "#3b82f6"}),
                                        html.Label("연도 범위", className="fw-bold", 
                                                  style={"font-size": "0.9rem", "color": "#1e293b"})
                                    ], style={"margin-bottom": "10px"}),
                                    dcc.RangeSlider(
                                        id='year-slider',
                                        min=min_year,
                                        max=max_year,
                                        value=[min_year, max_year],
                                        marks={str(year): {'label': str(year), 
                                                           'style': {'font-weight': 'bold', 'font-size': '0.8rem'}} 
                                               for year in years},
                                        step=1,
                                        tooltip={"placement": "bottom", "always_visible": True}
                                    )
                                ], width=12, lg=3, md=6, className="mb-3 mb-lg-0"),
                                
                                # 자치구 필터
                                dbc.Col([
                                    html.Div([
                                        html.I(className="fas fa-map-marked-alt", 
                                               style={"margin-right": "8px", "color": "#3b82f6"}),
                                        html.Label("자치구 선택", className="fw-bold", 
                                                  style={"font-size": "0.9rem", "color": "#1e293b"})
                                    ], style={"margin-bottom": "10px"}),
                                    dcc.Dropdown(
                                        id='district-dropdown',
                                        options=[{'label': d, 'value': d} for d in districts],
                                        value=[],
                                        multi=True,
                                        placeholder="전체 자치구",
                                        style={"font-size": "0.85rem"}
                                    )
                                ], width=12, lg=3, md=6, className="mb-3 mb-lg-0"),
                                
                                # 기상 필터
                                dbc.Col([
                                    html.Div([
                                        html.I(className="fas fa-cloud-sun-rain", 
                                               style={"margin-right": "8px", "color": "#3b82f6"}),
                                        html.Label("기상 조건", className="fw-bold", 
                                                  style={"font-size": "0.9rem", "color": "#1e293b"})
                                    ], style={"margin-bottom": "10px"}),
                                    dcc.Checklist(
                                        id='weather-checklist',
                                        options=[{'label': f' {w}', 'value': w} 
                                                for w in weather_conditions],
                                        value=weather_conditions,
                                        inline=True,
                                        labelStyle={
                                            'margin-right': '12px',
                                            'font-size': '0.85rem',
                                            'cursor': 'pointer'
                                        },
                                        inputStyle={"margin-right": "5px"}
                                    )
                                ], width=12, lg=3, md=6, className="mb-3 mb-lg-0"),
                                
                                # 지도 표시 지표
                                dbc.Col([
                                    html.Div([
                                        html.I(className="fas fa-layer-group", 
                                               style={"margin-right": "8px", "color": "#3b82f6"}),
                                        html.Label("지도 지표", className="fw-bold", 
                                                  style={"font-size": "0.9rem", "color": "#1e293b"})
                                    ], style={"margin-bottom": "10px"}),
                                    dcc.Dropdown(
                                        id='map-metric-dropdown',
                                        options=[
                                            {'label': '👥 사상자수', 'value': '사상자수'},
                                            {'label': '💀 사망자수', 'value': '사망자수'},
                                            {'label': '🚗 발생건수', 'value': '발생건수'}
                                        ],
                                        value='사상자수',
                                        clearable=False,
                                        style={"font-size": "0.85rem"}
                                    )
                                ], width=12, lg=3, md=6, className="mb-3 mb-lg-0"),
                            ])
                        ])
                    ], style={"padding": "20px"})
                ], style={
                    "background": "#ffffff",
                    "border": "2px solid #dbeafe",
                    "box-shadow": "0 4px 15px rgba(59, 130, 246, 0.1)",
                    "border-radius": "12px"
                })
            ])
        ], className="mb-4"),
        
        # 차트 영역
        dbc.Row([
            dbc.Col([
                # 지도 + 랭킹 차트 (나란히 배치)
                dbc.Row([
                    # 지도 차트
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Div([
                                    html.I(className="fas fa-map-marked-alt", 
                                           style={
                                               "margin-right": "8px",
                                               "color": "#ffffff"
                                           }),
                                    html.Strong("서울시 자치구별 지도", 
                                               style={
                                                   "font-size": "1.0rem",
                                                   "color": "#ffffff",
                                                   "letter-spacing": "0.5px"
                                               })
                                ], style={"display": "flex", "align-items": "center"})
                            ], style={
                                "background": "linear-gradient(90deg, #8b5cf6 0%, #7c3aed 100%)",
                                "border-bottom": "none",
                                "padding": "12px 15px"
                            }),
                            dbc.CardBody([
                                dcc.Graph(id='map-chart', config={'displayModeBar': False})
                            ], style={"padding": "15px"})
                        ], style={"margin-bottom": "20px", "box-shadow": "0 6px 20px rgba(139, 92, 246, 0.2)"})
                    ], width=12, lg=7, md=12),
                    
                    # 랭킹 차트
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Div([
                                    html.I(className="fas fa-trophy", 
                                           style={
                                               "margin-right": "8px",
                                               "color": "#ffffff"
                                           }),
                                    html.Strong("TOP 10 다발지역", 
                                               style={
                                                   "font-size": "1.0rem",
                                                   "color": "#ffffff",
                                                   "letter-spacing": "0.5px"
                                               })
                                ], style={"display": "flex", "align-items": "center"})
                            ], style={
                                "background": "linear-gradient(90deg, #ef4444 0%, #dc2626 100%)",
                                "border-bottom": "none",
                                "padding": "12px 15px"
                            }),
                            dbc.CardBody([
                                dcc.Graph(id='ranking-chart', config={'displayModeBar': False})
                            ], style={"padding": "15px"})
                        ], style={"margin-bottom": "20px", "box-shadow": "0 6px 20px rgba(239, 68, 68, 0.2)"})
                    ], width=12, lg=5, md=12),
                ], className="mb-3"),
                
                # 📊 상세 분석 차트들 (1행 3열 배치)
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Div([
                                    html.I(className="fas fa-chart-line", 
                                           style={
                                               "margin-right": "8px",
                                               "color": "#ffffff"
                                           }),
                                    html.Strong("연도별 추이", 
                                               style={
                                                   "font-size": "0.9rem",
                                                   "color": "#ffffff",
                                                   "letter-spacing": "0.5px"
                                               })
                                ], style={"display": "flex", "align-items": "center"})
                            ], style={
                                "background": "linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)",
                                "border-bottom": "none",
                                "padding": "8px 12px"
                            }),
                            dbc.CardBody([
                                dcc.Graph(id='trend-chart', config={'displayModeBar': False})
                            ], style={"padding": "15px"})
                        ], style={"margin-bottom": "20px"})
                    ], width=12, lg=4, md=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Div([
                                    html.I(className="fas fa-cloud-sun", 
                                           style={
                                               "margin-right": "8px",
                                               "color": "#ffffff"
                                           }),
                                    html.Strong("기상별 분석", 
                                               style={
                                                   "font-size": "0.9rem",
                                                   "color": "#ffffff",
                                                   "letter-spacing": "0.5px"
                                               })
                                ], style={"display": "flex", "align-items": "center"})
                            ], style={
                                "background": "linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)",
                                "border-bottom": "none",
                                "padding": "8px 12px"
                            }),
                            dbc.CardBody([
                                dcc.Graph(id='weather-chart', config={'displayModeBar': False})
                            ], style={"padding": "15px"})
                        ], style={"margin-bottom": "20px"})
                    ], width=12, lg=4, md=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Div([
                                    html.I(className="fas fa-car", 
                                           style={
                                               "margin-right": "8px",
                                               "color": "#ffffff"
                                           }),
                                    html.Strong("차종별 분석", 
                                               style={
                                                   "font-size": "0.9rem",
                                                   "color": "#ffffff",
                                                   "letter-spacing": "0.5px"
                                               })
                                ], style={"display": "flex", "align-items": "center"})
                            ], style={
                                "background": "linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)",
                                "border-bottom": "none",
                                "padding": "8px 12px"
                            }),
                            dbc.CardBody([
                                dcc.Graph(id='vehicle-chart', config={'displayModeBar': False})
                            ], style={"padding": "15px"})
                        ], style={"margin-bottom": "20px"})
                    ], width=12, lg=4, md=6),
                ], className="mb-3"),
                
                # 히트맵 (전체 너비)
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Div([
                                    html.I(className="fas fa-th", 
                                           style={
                                               "margin-right": "8px",
                                               "color": "#ffffff"
                                           }),
                                    html.Strong("히트맵 분석", 
                                               style={
                                                   "font-size": "0.9rem",
                                                   "color": "#ffffff",
                                                   "letter-spacing": "0.5px"
                                               })
                                ], style={"display": "flex", "align-items": "center"})
                            ], style={
                                "background": "linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)",
                                "border-bottom": "none",
                                "padding": "8px 12px"
                            }),
                            dbc.CardBody([
                                dcc.Graph(id='heatmap-chart', config={'displayModeBar': False})
                            ], style={"padding": "15px"})
                        ], style={"margin-bottom": "20px"})
                    ], width=12)
                ], className="mb-3"),
            ], width=12)
        ], className="mb-4"),
    
    # 푸터
    dbc.Row([
        dbc.Col([
            html.Hr(style={
                "border-top": "2px solid #3b82f6",
                "margin-top": "30px",
                "opacity": "0.3"
            }),
            html.Div([
                html.P([
                    html.I(className="fas fa-copyright", 
                           style={"margin-right": "5px", "color": "#3b82f6"}),
                    "2024 서울시 교통사고 안전 대시보드"
                ], className="text-center mb-2", 
                   style={"color": "#94a3b8", "font-size": "0.9rem"}),
                html.P([
                    html.I(className="fas fa-database", 
                           style={"margin-right": "5px", "color": "#3b82f6"}),
                    "데이터 출처: 서울 열린데이터광장"
                ], className="text-center mb-2",
                   style={"color": "#94a3b8", "font-size": "0.9rem"}),
                html.P([
                    html.I(className="fas fa-code", 
                           style={"margin-right": "5px", "color": "#3b82f6"}),
                    "Powered by Plotly Dash & Python"
                ], className="text-center",
                   style={"color": "#94a3b8", "font-size": "0.9rem"})
            ], style={"padding": "20px"})
        ])
    ])
], fluid=True, style={
    "padding": "15px 20px",
    "background": "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)",
    "max-width": "1600px",
    "margin": "0 auto"
})


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
        Input('map-metric-dropdown', 'value')
    ]
)
def update_charts(year_range, selected_districts, selected_weather, map_metric):
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
        fig_weather = create_weather_chart(df_weather_filtered)
        fig_vehicle = create_vehicle_chart(df_vehicle_filtered)
        fig_heatmap = create_heatmap_chart(df_dist_filtered)
        fig_ranking = create_ranking_chart(df_dist_filtered)
        
        # 통계 업데이트
        total_accidents = f"{df_dist_filtered['발생건수'].sum():,.0f}"
        total_deaths = f"{df_dist_filtered['사망자수'].sum():,.0f}"
        total_injuries = f"{df_dist_filtered['부상자수'].sum():,.0f}"
        
        return (
            fig_map, fig_trend, fig_weather, fig_vehicle,
            fig_heatmap, fig_ranking,
            total_accidents, total_deaths, total_injuries
        )
    
    except Exception as e:
        print(f"⚠️ 콜백 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 에러 발생 시 기본 차트 반환
        fig_map = create_map_chart(df_district, '사상자수')
        fig_trend = create_trend_chart(df_district, None)
        fig_weather = create_weather_chart(df_weather)
        fig_vehicle = create_vehicle_chart(df_vehicle)
        fig_heatmap = create_heatmap_chart(df_district)
        fig_ranking = create_ranking_chart(df_district)
        
        total_accidents = f"{df_district['발생건수'].sum():,.0f}"
        total_deaths = f"{df_district['사망자수'].sum():,.0f}"
        total_injuries = f"{df_district['부상자수'].sum():,.0f}"
        
        return (
            fig_map, fig_trend, fig_weather, fig_vehicle,
            fig_heatmap, fig_ranking,
            total_accidents, total_deaths, total_injuries
        )


if __name__ == '__main__':
    print("=" * 70)
    print("🚀 대시보드 서버 시작!")
    print("=" * 70)
    print("\n📱 브라우저에서 접속: http://localhost:8050")
    print("\n종료하려면 Ctrl+C를 누르세요.\n")
    
    app.run(debug=True, host='0.0.0.0', port=8050)
