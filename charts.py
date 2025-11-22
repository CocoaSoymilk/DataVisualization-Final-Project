"""
차트 생성 함수 모음
각 차트는 필터링된 데이터를 받아 Plotly Figure를 반환합니다.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json

# 색상 팔레트 (더 생동감 있는 색상)
COLORS = {
    '사망': '#FF4757',      # 선명한 빨강
    '부상': '#FFA502',      # 선명한 주황
    '발생': '#1E90FF',      # 선명한 파랑
    '맑음': '#FFD700',      # 골드
    '흐림': '#95A5A6',      # 회색
    '비': '#3498DB',        # 파랑
    '안개': '#BDC3C7',      # 연한 회색
    '눈': '#ECF0F1',        # 흰색
    '기타/불명': '#7F8C8D', # 진한 회색
    '소계': '#2C3E50',      # 매우 진한 회색
    '사업용차량': '#FF6348', # 밝은 오렌지
    '비사업용차량': '#1E90FF', # 밝은 파랑
    '이륜차': '#FF4757',    # 선명한 빨강
    '자전거': '#2ECC71',    # 밝은 초록
}

# 차트 공통 스타일 (밝은 라이트 테마)
COMMON_LAYOUT = {
    'font': {
        'family': 'Segoe UI, Malgun Gothic, sans-serif',
        'size': 13,
        'color': '#1e293b'
    },
    'plot_bgcolor': '#ffffff',  # 흰색 배경
    'paper_bgcolor': '#ffffff',  # 흰색 배경
    'margin': {'l': 60, 'r': 60, 't': 70, 'b': 60}
}

# 제목 스타일 (개별 적용용)
TITLE_STYLE = {
    'font': {
        'size': 18,
        'color': '#1e40af',
        'family': 'Segoe UI, Malgun Gothic',
    },
    'x': 0.5,
    'xanchor': 'center'
}


def create_trend_chart(df_district, selected_districts=None):
    """
    차트 1: 연도별 사고 추이 (Line Chart)
    
    선택 이유: 시계열 데이터의 추세를 명확하게 표현하기 위함
    - 여러 자치구의 사고 추이를 동시에 비교 가능
    - 증가/감소 트렌드를 직관적으로 파악
    """
    if len(df_district) == 0:
        # 빈 차트 반환
        fig = go.Figure()
        fig.update_layout(
            **COMMON_LAYOUT,
            title={**TITLE_STYLE, 'text': '<b>📊 연도별 교통사고 발생 추이</b>'},
            annotations=[dict(text='데이터가 없습니다', xref='paper', yref='paper', 
                             x=0.5, y=0.5, showarrow=False, font=dict(size=20))]
        )
        return fig
    
    try:
        if selected_districts and len(selected_districts) > 0:
            df = df_district[df_district['자치구'].isin(selected_districts)].copy()
            # 자치구별 추이 표시
            df_trend = df.groupby(['연도', '자치구'])['발생건수'].sum().reset_index()
            
            fig = px.line(
                df_trend,
                x='연도',
                y='발생건수',
                color='자치구',
                title='<b>📈 연도별 교통사고 발생 추이</b>',
                labels={'발생건수': '사고 건수 (건)', '연도': '연도'},
                markers=True
            )
            
            # 라인 및 마커 스타일 개선
            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=10, line=dict(width=2, color='white')),
                hovertemplate='<b>%{fullData.name}</b><br>연도: %{x}<br>사고: %{y:,.0f}건<extra></extra>'
            )
        else:
            # 전체 서울시 추이 (발생건수만 표시 - 단순화)
            df_trend = df_district.groupby('연도').agg({
                '발생건수': 'sum',
                '사망자수': 'sum',
                '부상자수': 'sum'
            }).reset_index()
            
            fig = go.Figure()
            
            # 발생건수 라인
            fig.add_trace(go.Scatter(
                x=df_trend['연도'],
                y=df_trend['발생건수'],
                name='발생건수',
                mode='lines+markers+text',
                line=dict(color='#3b82f6', width=4),
                marker=dict(size=12, line=dict(width=2, color='white')),
                text=df_trend['발생건수'],
                textposition='top center',
                textfont=dict(size=11, color='#1e40af', family='Malgun Gothic'),
                hovertemplate='<b>발생건수</b><br>연도: %{x}<br>건수: %{y:,.0f}건<extra></extra>'
            ))
            
            # 사망자수 라인
            fig.add_trace(go.Scatter(
                x=df_trend['연도'],
                y=df_trend['사망자수'],
                name='사망자수',
                mode='lines+markers',
                line=dict(color='#ef4444', width=3, dash='dash'),
                marker=dict(size=10, line=dict(width=2, color='white'), symbol='x'),
                hovertemplate='<b>사망자수</b><br>연도: %{x}<br>인원: %{y:,.0f}명<extra></extra>'
            ))
            
            # 부상자수 라인
            fig.add_trace(go.Scatter(
                x=df_trend['연도'],
                y=df_trend['부상자수'],
                name='부상자수',
                mode='lines+markers',
                line=dict(color='#f59e0b', width=3, dash='dot'),
                marker=dict(size=10, line=dict(width=2, color='white'), symbol='diamond'),
                hovertemplate='<b>부상자수</b><br>연도: %{x}<br>인원: %{y:,.0f}명<extra></extra>'
            ))
    except Exception as e:
        print(f"⚠️ 연도별 추이 차트 생성 오류: {e}")
        import traceback
        traceback.print_exc()
        
        # 에러 시 기본 차트 반환
        fig = go.Figure()
        fig.add_annotation(
            text=f'차트 생성 실패<br>{str(e)[:100]}',
            xref='paper', yref='paper',
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color='#ef4444')
        )
    
    fig.update_layout(
        font=COMMON_LAYOUT['font'],
        plot_bgcolor=COMMON_LAYOUT['plot_bgcolor'],
        paper_bgcolor=COMMON_LAYOUT['paper_bgcolor'],
        title={**TITLE_STYLE, 'text': '<b>📊 연도별 교통사고 발생 추이</b>', 'y': 0.98},
        height=480,
        hovermode='x unified',
        margin={'l': 60, 'r': 60, 't': 90, 'b': 60},  # 상단 여백 증가
        xaxis=dict(
            title='<b>연도</b>',
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#e5e7eb',
            dtick=1,
            color='#64748b',
            linecolor='#cbd5e1'
        ),
        yaxis=dict(
            title='<b>건수/인원</b>',
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#e5e7eb',
            color='#64748b',
            linecolor='#cbd5e1'
        ),
        legend=dict(
            title='<b>구분</b>',
            orientation="h",
            yanchor="bottom",
            y=1.05,  # 범례를 더 위로
            xanchor="right",
            x=0.98,  # 범례를 약간 왼쪽으로 (우측 정렬 기준)
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor='#3b82f6',
            borderwidth=1,
            font=dict(color='#1e293b')
        )
    )
    
    return fig


def create_weather_chart(df_weather, weather_metric='both'):
    """
    차트 2: 기상별 사고 비율 (Stacked Bar Chart)
    
    선택 이유: 범주형 데이터의 비율을 직관적으로 비교하기 위함
    - 기상 조건별 사고 심각도(사망/부상) 비교
    - 전체 대비 각 기상의 영향도 파악
    
    Args:
        df_weather: 기상 데이터
        weather_metric: 'deaths' (사망자), 'injuries' (부상자), 'both' (둘 다)
    """
    if len(df_weather) == 0:
        # 빈 차트 반환
        fig = go.Figure()
        fig.update_layout(
            **COMMON_LAYOUT,
            title={**TITLE_STYLE, 'text': '<b>🌤️ 기상 상태별 사고 피해 현황</b>'},
            annotations=[dict(text='데이터가 없습니다', xref='paper', yref='paper', 
                             x=0.5, y=0.5, showarrow=False, font=dict(size=20))]
        )
        return fig
    
    # '소계' 제외
    df = df_weather[df_weather['기상상태'] != '소계'].copy()
    
    if len(df) == 0:
        # 빈 차트 반환
        fig = go.Figure()
        fig.update_layout(
            **COMMON_LAYOUT,
            title={**TITLE_STYLE, 'text': '<b>🌤️ 기상 상태별 사고 피해 현황</b>'},
            annotations=[dict(text='데이터가 없습니다', xref='paper', yref='paper', 
                             x=0.5, y=0.5, showarrow=False, font=dict(size=20))]
        )
        return fig
    
    # 기상별 사망자/부상자 집계
    df_agg = df.groupby('기상상태').agg({
        '사망자수': 'sum',
        '부상자수': 'sum'
    }).reset_index()
    
    # 기상별로 정렬 (발생 건수가 많은 순)
    df_agg['합계'] = df_agg['사망자수'] + df_agg['부상자수']
    df_agg = df_agg.sort_values('합계', ascending=False)
    
    # 차트 생성
    fig = go.Figure()
    
    # 선택된 지표에 따라 표시 (하나만 표시)
    if weather_metric == 'both':
        fig.add_trace(go.Bar(
            name='사망자',
            x=df_agg['기상상태'],
            y=df_agg['사망자수'],
            marker=dict(color=COLORS['사망'], line=dict(width=1.5, color='white')),
            text=df_agg['사망자수'],
            textposition='inside',
            textfont=dict(size=11, color='white', family='Malgun Gothic'),
            hovertemplate='<b>사망자</b><br>기상: %{x}<br>인원: %{y:,.0f}명<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            name='부상자',
            x=df_agg['기상상태'],
            y=df_agg['부상자수'],
            marker=dict(color=COLORS['부상'], line=dict(width=1.5, color='white')),
            text=df_agg['부상자수'],
            textposition='inside',
            textfont=dict(size=11, color='white', family='Malgun Gothic'),
            hovertemplate='<b>부상자</b><br>기상: %{x}<br>인원: %{y:,.0f}명<extra></extra>'
        ))
    elif weather_metric == 'deaths':
        fig.add_trace(go.Bar(
            name='사망자',
            x=df_agg['기상상태'],
            y=df_agg['사망자수'],
            marker=dict(color=COLORS['사망'], line=dict(width=1.5, color='white')),
            text=df_agg['사망자수'],
            textposition='auto',
            textfont=dict(size=12, color='white', family='Malgun Gothic'),
            hovertemplate='<b>사망자</b><br>기상: %{x}<br>인원: %{y:,.0f}명<extra></extra>',
            showlegend=False
        ))
    elif weather_metric == 'injuries':
        fig.add_trace(go.Bar(
            name='부상자',
            x=df_agg['기상상태'],
            y=df_agg['부상자수'],
            marker=dict(color=COLORS['부상'], line=dict(width=1.5, color='white')),
            text=df_agg['부상자수'],
            textposition='auto',
            textfont=dict(size=12, color='white', family='Malgun Gothic'),
            hovertemplate='<b>부상자</b><br>기상: %{x}<br>인원: %{y:,.0f}명<extra></extra>',
            showlegend=False
        ))
    
    fig.update_layout(
        **COMMON_LAYOUT,
        title={**TITLE_STYLE, 'text': '<b>🌤️ 기상 상태별 사고 피해 현황</b>'},
        height=480,
        barmode='group' if weather_metric == 'both' else 'overlay',
        xaxis=dict(
            title='<b>기상 상태</b>',
            tickangle=-45,
            showgrid=False,
            color='#64748b',
            linecolor='#cbd5e1'
        ),
        yaxis=dict(
            title='<b>인원 (명)</b>',
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#e5e7eb',
            color='#64748b',
            linecolor='#cbd5e1'
        ),
        legend=dict(
            title='<b>구분</b>',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor='#3b82f6',
            borderwidth=1,
            font=dict(color='#1e293b')
        ),
        bargap=0.2,
        bargroupgap=0.1
    )
    
    return fig


def create_vehicle_chart(df_vehicle):
    """
    차트 3: 차종별 사고 비율 (Donut Chart)
    
    선택 이유: 전체 대비 각 차종의 비율을 한눈에 파악하기 위함
    - 원형 차트로 직관적인 비율 표현
    - 도넛 형태로 중앙에 총계 표시 가능
    """
    if len(df_vehicle) == 0:
        # 빈 차트 반환
        fig = go.Figure()
        fig.update_layout(
            **COMMON_LAYOUT,
            title={**TITLE_STYLE, 'text': '<b>🚗 차종별 사고 발생 건수</b>'},
            annotations=[dict(text='데이터가 없습니다', xref='paper', yref='paper', 
                             x=0.5, y=0.5, showarrow=False, font=dict(size=20))]
        )
        return fig
    
    # '소계' 제외
    df = df_vehicle[df_vehicle['차종'] != '소계'].copy()
    
    # 차종별 발생건수 집계
    df_agg = df.groupby('차종')['발생건수'].sum().reset_index()
    df_agg = df_agg.sort_values('발생건수', ascending=False)
    
    total = df_agg['발생건수'].sum()
    
    fig = go.Figure(data=[go.Pie(
        labels=df_agg['차종'],
        values=df_agg['발생건수'],
        hole=0.45,
        marker=dict(
            colors=[COLORS.get(x, '#34495e') for x in df_agg['차종']],
            line=dict(color='white', width=3)
        ),
        textposition='inside',
        textinfo='label',  # 라벨만 표시
        textfont=dict(size=13, color='white', family='Malgun Gothic', weight='bold'),
        hovertemplate='<b>%{label}</b><br>사고: %{value:,.0f}건<br>비율: %{percent}<extra></extra>',
        pull=[0.05 if i == 0 else 0 for i in range(len(df_agg))],  # 가장 큰 조각 강조
        rotation=90,  # 텍스트 회전 각도 조정
        insidetextorientation='horizontal'  # 텍스트 수평 정렬
    )])
    
    fig.update_layout(
        **COMMON_LAYOUT,
        title={**TITLE_STYLE, 'text': '<b>🚗 차량 용도별 사고 발생 비율</b>'},
        height=700,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor='#3b82f6',
            borderwidth=1,
            font=dict(size=13, color='#1e293b')
        ),
        annotations=[dict(
            text=f'<b>총계</b><br>{total:,.0f}건',
            x=0.5, y=0.5,
            font=dict(size=18, color='#1e40af', family='Segoe UI, Malgun Gothic'),
            showarrow=False
        )]
    )
    
    return fig


def create_heatmap_chart(df_district):
    """
    차트 4: 자치구별 사고 밀도 히트맵
    
    선택 이유: 지역별, 시간별 패턴을 2차원으로 시각화하기 위함
    - 위험 지역과 위험 기간을 동시에 파악
    - 색상 강도로 위험도를 직관적으로 표현
    """
    if len(df_district) == 0:
        # 빈 차트 반환
        fig = go.Figure()
        fig.update_layout(
            **COMMON_LAYOUT,
            title={**TITLE_STYLE, 'text': '<b>🔥 자치구-연도별 사고 히트맵</b>'},
            annotations=[dict(text='데이터가 없습니다', xref='paper', yref='paper', 
                             x=0.5, y=0.5, showarrow=False, font=dict(size=20))]
        )
        return fig
    
    # 최근 5개년 데이터만 필터링
    df = df_district.copy()
    years = sorted(df['연도'].unique())
    if len(years) > 5:
        recent_years = years[-5:]
        df = df[df['연도'].isin(recent_years)]
    
    # 피벗 테이블 생성
    df_pivot = df.pivot_table(
        index='자치구',
        columns='연도',
        values='발생건수',
        aggfunc='sum'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=df_pivot.values,
        x=df_pivot.columns,
        y=df_pivot.index,
        colorscale=[
            [0, '#FFF5F5'],      # 매우 연한 빨강
            [0.2, '#FED7D7'],    # 연한 빨강
            [0.4, '#FC8181'],    # 중간 빨강
            [0.6, '#F56565'],    # 진한 빨강
            [0.8, '#E53E3E'],    # 매우 진한 빨강
            [1, '#C53030']       # 가장 진한 빨강
        ],
        text=df_pivot.values,
        texttemplate='<b>%{text:.0f}</b>',
        textfont={"size": 11, "color": "#1e293b"},
        hovertemplate='<b>자치구</b>: %{y}<br><b>연도</b>: %{x}<br><b>사고</b>: %{z:,.0f}건<extra></extra>',
        colorbar=dict(
            title="<b>사고 건수</b>",
            title_font=dict(size=13),  # ✅ 수정: titlefont → title_font
            tickfont=dict(size=12),
            thickness=20,
            len=0.7
        )
    ))
    
    fig.update_layout(
        font=COMMON_LAYOUT['font'],
        plot_bgcolor=COMMON_LAYOUT['plot_bgcolor'],
        paper_bgcolor=COMMON_LAYOUT['paper_bgcolor'],
        title={**TITLE_STYLE, 'text': '<b>🗺️ 자치구별 연도별 사고 발생 히트맵</b>', 'y': 0.97},
        height=650,  # 높이 감소하여 컨테이너에 맞춤
        margin={'l': 80, 'r': 80, 't': 80, 'b': 40},  # 여백 감소
        autosize=True,  # 자동 크기 조정
        xaxis=dict(
            title='<b>연도</b>',
            side='top',
            tickfont=dict(size=11, color='#64748b'),
            dtick=1,
            color='#94a3b8',
            linecolor='#374151'
        ),
        yaxis=dict(
            title='<b>자치구</b>',
            tickfont=dict(size=10, color='#64748b'),
            autorange='reversed',
            color='#94a3b8',
            linecolor='#374151'
        )
    )
    
    return fig


def create_ranking_chart(df_district, top_n=10):
    """
    차트 5: 위험 자치구 랭킹 (Horizontal Bar)
    
    선택 이유: 순위를 한눈에 비교하기 좋음
    - 가로 막대로 긴 자치구명 표시에 유리
    - 상위 위험 지역을 명확하게 강조
    """
    if len(df_district) == 0:
        # 빈 차트 반환
        fig = go.Figure()
        fig.update_layout(
            **COMMON_LAYOUT,
            title={**TITLE_STYLE, 'text': '<b>🏆 사고 다발 지역 TOP 10</b>'},
            annotations=[dict(text='데이터가 없습니다', xref='paper', yref='paper', 
                             x=0.5, y=0.5, showarrow=False, font=dict(size=20))]
        )
        return fig
    
    # 최근 연도 데이터로 랭킹
    latest_year = df_district['연도'].max()
    df_latest = df_district[df_district['연도'] == latest_year].copy()
    
    # 상위 N개 자치구
    df_top = df_latest.nlargest(top_n, '발생건수')
    df_top = df_top.sort_values('발생건수')  # 오름차순 정렬 (그래프에서 큰 값이 위로)
    
    # 순위 추가 (역순)
    df_top['순위'] = range(top_n, 0, -1)
    
    fig = go.Figure(go.Bar(
        x=df_top['발생건수'],
        y=df_top['자치구'],
        orientation='h',
        marker=dict(
            color=df_top['발생건수'],
            colorscale=[
                [0, '#FED7D7'],      # 연한 빨강
                [0.5, '#FC8181'],    # 중간 빨강
                [1, '#E53E3E']       # 진한 빨강
            ],
            line=dict(color='white', width=2)
        ),
        text=df_top['발생건수'].apply(lambda x: f'<b>{x:,.0f}건</b>'),
        textposition='outside',
        textfont=dict(size=13, color='#1e40af'),
        hovertemplate='<b>%{y}</b><br>사고: %{x:,.0f}건<extra></extra>'
    ))
    
    fig.update_layout(
        font=COMMON_LAYOUT['font'],
        plot_bgcolor=COMMON_LAYOUT['plot_bgcolor'],
        paper_bgcolor=COMMON_LAYOUT['paper_bgcolor'],
        title={**TITLE_STYLE, 'text': f'<b>⚠️ 교통사고 다발 자치구 TOP {top_n} ({latest_year}년)</b>'},
        height=600,
        margin={'l': 80, 'r': 150, 't': 70, 'b': 60},  # 우측 여백 더 증가하여 수치 잘림 방지
        xaxis=dict(
            title='<b>사고 건수 (건)</b>',
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#e5e7eb',
            color='#64748b',
            linecolor='#cbd5e1',
            range=[0, df_top['발생건수'].max() * 1.15]  # x축 범위를 15% 더 확장
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=12, color='#64748b'),
            color='#64748b',
            linecolor='#cbd5e1'
        )
    )
    
    return fig


def create_comparison_chart(df_district, selected_districts=None):
    """
    차트 6: 사망자/부상자 비교 (Grouped Bar)
    
    선택 이유: 두 지표를 명확하게 대비하여 심각도를 파악하기 위함
    - 그룹 막대로 직접 비교 용이
    - 사고 심각도(사망/부상 비율) 분석
    """
    if len(df_district) == 0:
        # 빈 차트 반환
        fig = go.Figure()
        fig.update_layout(
            **COMMON_LAYOUT,
            title={**TITLE_STYLE, 'text': '<b>⚖️ 사망자 vs 부상자 비교</b>'},
            annotations=[dict(text='데이터가 없습니다', xref='paper', yref='paper', 
                             x=0.5, y=0.5, showarrow=False, font=dict(size=20))]
        )
        return fig
    
    if selected_districts and len(selected_districts) > 0:
        df = df_district[df_district['자치구'].isin(selected_districts)]
    else:
        # 최근 연도 상위 10개 자치구만
        latest_year = df_district['연도'].max()
        top_districts = df_district[df_district['연도'] == latest_year].nlargest(10, '발생건수')['자치구'].tolist()
        df = df_district[df_district['자치구'].isin(top_districts)]
    
    # 최근 연도 데이터
    latest_year = df['연도'].max()
    df_latest = df[df['연도'] == latest_year]
    
    # 사망자/부상자 데이터
    df_latest = df_latest.sort_values('발생건수', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='사망자',
        x=df_latest['자치구'],
        y=df_latest['사망자수'],
        marker=dict(
            color=COLORS['사망'],
            line=dict(color='white', width=2)
        ),
        text=df_latest['사망자수'],
        textposition='outside',
        textfont=dict(size=11, color=COLORS['사망']),
        hovertemplate='<b>%{x}</b><br>사망자: %{y:,.0f}명<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='부상자',
        x=df_latest['자치구'],
        y=df_latest['부상자수'],
        marker=dict(
            color=COLORS['부상'],
            line=dict(color='white', width=2)
        ),
        text=df_latest['부상자수'],
        textposition='outside',
        textfont=dict(size=11, color=COLORS['부상']),
        hovertemplate='<b>%{x}</b><br>부상자: %{y:,.0f}명<extra></extra>'
    ))
    
    fig.update_layout(
        **COMMON_LAYOUT,
        title={**TITLE_STYLE, 'text': f'<b>👥 자치구별 사망자/부상자 비교 ({latest_year}년)</b>'},
        barmode='group',
        height=480,
        xaxis=dict(
            title='',
            tickangle=-45,
            tickfont=dict(size=12, color='#64748b'),
            showgrid=False,
            color='#94a3b8',
            linecolor='#374151'
        ),
        yaxis=dict(
            title='<b>인원 (명)</b>',
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#e5e7eb',
            color='#64748b',
            linecolor='#cbd5e1'
        ),
        legend=dict(
            title='<b>구분</b>',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(15, 23, 42, 0.9)',
            bordercolor='#00d9ff',
            borderwidth=1,
            font=dict(size=13, color='#e0e0e0')
        ),
        bargap=0.15,
        bargroupgap=0.1
    )
    
    return fig


def create_map_chart(df_district, map_metric='total'):
    """
    차트 7: 서울시 자치구별 교통사고 Choropleth 지도
    
    선택 이유: 지리적 맥락에서 사고 데이터를 시각화하기 위함
    - 자치구 경계선으로 지역별 차이를 명확히 표현
    - 호버로 상세 정보 제공
    - 색상 그라데이션으로 위험도 직관적 표현
    
    Args:
        df_district: 자치구별 데이터프레임
        map_metric: 표시할 지표 ('total', 'deaths', 'injuries', 'count')
    """
    if len(df_district) == 0:
        # 빈 차트 반환
        fig = go.Figure()
        fig.update_layout(
            font=COMMON_LAYOUT['font'],
            plot_bgcolor=COMMON_LAYOUT['plot_bgcolor'],
            paper_bgcolor=COMMON_LAYOUT['paper_bgcolor'],
            margin={'l': 10, 'r': 10, 't': 70, 'b': 10},
            title={**TITLE_STYLE, 'text': '<b>🗺️ 서울시 자치구별 교통사고 지도</b>'},
            annotations=[dict(text='데이터가 없습니다', xref='paper', yref='paper', 
                             x=0.5, y=0.5, showarrow=False, font=dict(size=20))],
            height=600
        )
        return fig
    
    try:
        # 서울시 자치구 GeoJSON 로드 (인터넷에서)
        print("🗺️ GeoJSON 다운로드 중...")
        geojson_url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json"
        response = requests.get(geojson_url, timeout=30)  # 타임아웃 30초로 증가
        response.raise_for_status()  # HTTP 에러 체크
        seoul_geo = response.json()
        print(f"✓ GeoJSON 다운로드 완료! ({len(seoul_geo.get('features', []))}개 자치구)")
        
        # 자치구별 데이터 집계
        df_agg = df_district.groupby('자치구').agg({
            '발생건수': 'sum',
            '사망자수': 'sum',
            '부상자수': 'sum'
        }).reset_index()
        
        # 사상자수 계산
        df_agg['사상자수'] = df_agg['사망자수'] + df_agg['부상자수']
        
        print(f"📊 데이터 자치구: {sorted(df_agg['자치구'].unique())}")
        
        # GeoJSON의 자치구명과 데이터의 자치구명 매칭
        # GeoJSON은 '종로구', '중구' 등으로 되어 있음
        geojson_districts = []
        for feature in seoul_geo['features']:
            name = feature['properties']['name']
            geojson_districts.append(name)
        
        print(f"🗺️ GeoJSON 자치구: {sorted(geojson_districts)}")
        
        # 매칭되지 않는 자치구 확인
        data_districts = set(df_agg['자치구'].unique())
        geo_districts = set(geojson_districts)
        unmatched = data_districts - geo_districts
        if unmatched:
            print(f"⚠️ 매칭되지 않는 자치구: {unmatched}")
        
        # 표시할 지표 선택
        if map_metric == 'total':
            color_column = '사상자수'
            color_label = '사상자 수 (명)'
            title_text = '<b>🗺️ 서울시 자치구별 총 사상자 수</b>'
        elif map_metric == 'deaths':
            color_column = '사망자수'
            color_label = '사망자 수 (명)'
            title_text = '<b>🗺️ 서울시 자치구별 총 사망자 수</b>'
        elif map_metric == 'injuries':
            color_column = '부상자수'
            color_label = '부상자 수 (명)'
            title_text = '<b>🗺️ 서울시 자치구별 총 부상자 수</b>'
        else:  # count
            color_column = '발생건수'
            color_label = '발생 건수 (건)'
            title_text = '<b>🗺️ 서울시 자치구별 총 사고 발생 건수</b>'
        
        # Choropleth Mapbox 생성
        fig = px.choropleth_mapbox(
            df_agg,
            geojson=seoul_geo,
            locations='자치구',
            featureidkey='properties.name',
            color=color_column,
            color_continuous_scale=[
                [0, '#EFF6FF'],      # 매우 연한 파랑
                [0.2, '#BFDBFE'],    # 연한 파랑
                [0.4, '#60A5FA'],    # 중간 파랑
                [0.6, '#3B82F6'],    # 진한 파랑
                [0.8, '#1D4ED8'],    # 매우 진한 파랑
                [1, '#1E3A8A']       # 가장 진한 파랑
            ],
            hover_name='자치구',
            hover_data={
                '자치구': False,
                '발생건수': ':,.0f',
                '사망자수': ':,.0f',
                '부상자수': ':,.0f',
                '사상자수': ':,.0f',
                color_column: False
            },
            labels={
                '발생건수': '사고 건수',
                '사망자수': '사망자',
                '부상자수': '부상자',
                '사상자수': '사상자'
            },
            mapbox_style='open-street-map',
            center={'lat': 37.5665, 'lon': 126.9780},  # 서울시청 좌표
            zoom=10,
            opacity=0.7
        )
        
        # 자치구 이름 텍스트 추가
        for feature in seoul_geo['features']:
            district_name = feature['properties']['name']
            # 자치구의 중심 좌표 계산 (간단한 평균)
            coords = feature['geometry']['coordinates'][0]
            if isinstance(coords[0][0], list):  # MultiPolygon 처리
                coords = coords[0]
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            center_lon = sum(lons) / len(lons)
            center_lat = sum(lats) / len(lats)
            
            # 텍스트 추가 (구 포함)
            fig.add_scattermapbox(
                lon=[center_lon],
                lat=[center_lat],
                mode='text',
                text=[district_name],
                textfont=dict(size=10, color='#1e293b', family='Malgun Gothic', weight='bold'),
                hoverinfo='skip',
                showlegend=False
            )
        
        # 레이아웃 업데이트 (COMMON_LAYOUT의 margin과 충돌하지 않도록 별도 처리)
        fig.update_layout(
            font=COMMON_LAYOUT['font'],
            plot_bgcolor=COMMON_LAYOUT['plot_bgcolor'],
            paper_bgcolor=COMMON_LAYOUT['paper_bgcolor'],
            title={**TITLE_STYLE, 'text': title_text},
            height=650,
            margin={'l': 10, 'r': 10, 't': 70, 'b': 10},
            coloraxis_colorbar=dict(
                title=f'<b>{color_label}</b>',
                title_font=dict(size=13, color='#1e40af'),  # ✅ 수정: titlefont → title_font
                tickfont=dict(size=12, color='#1e293b'),
                thickness=20,
                len=0.7,
                x=1.0,
                xanchor='left'
            )
        )
        
        # 호버 템플릿 커스터마이징
        fig.update_traces(
            hovertemplate='<b>%{hovertext}</b><br><br>' +
                         '사고 건수: %{customdata[0]}<br>' +
                         '사망자: %{customdata[1]}명<br>' +
                         '부상자: %{customdata[2]}명<br>' +
                         '사상자: %{customdata[3]}명<extra></extra>'
        )
        
        return fig
        
    except requests.exceptions.RequestException as e:
        # 네트워크/GeoJSON 로딩 에러
        print(f"❌ GeoJSON 로딩 실패: {e}")
        import traceback
        traceback.print_exc()
        
        fig = go.Figure()
        fig.update_layout(
            font=COMMON_LAYOUT['font'],
            plot_bgcolor=COMMON_LAYOUT['plot_bgcolor'],
            paper_bgcolor=COMMON_LAYOUT['paper_bgcolor'],
            title={**TITLE_STYLE, 'text': '<b>🗺️ 서울시 자치구별 교통사고 지도</b>'},
            annotations=[dict(
                text=f'지도 로딩 실패<br><span style="font-size:14px">인터넷 연결을 확인해주세요</span><br><span style="font-size:12px; color:#94a3b8">{str(e)[:100]}</span>',
                xref='paper', yref='paper',
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=18, color='#64748b')
            )],
            height=600,
            margin={'l': 10, 'r': 10, 't': 70, 'b': 10}
        )
        return fig
    except Exception as e:
        # 기타 에러
        print(f"❌ 지도 생성 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        
        fig = go.Figure()
        fig.update_layout(
            font=COMMON_LAYOUT['font'],
            plot_bgcolor=COMMON_LAYOUT['plot_bgcolor'],
            paper_bgcolor=COMMON_LAYOUT['paper_bgcolor'],
            title={**TITLE_STYLE, 'text': '<b>🗺️ 서울시 자치구별 교통사고 지도</b>'},
            annotations=[dict(
                text=f'지도 생성 실패<br><span style="font-size:14px">{type(e).__name__}</span><br><span style="font-size:12px; color:#94a3b8">{str(e)[:100]}</span>',
                xref='paper', yref='paper',
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=18, color='#64748b')
            )],
            height=600,
            margin={'l': 10, 'r': 10, 't': 70, 'b': 10}
        )
        return fig
