#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""데이터 로딩 및 확인 스크립트"""

import pandas as pd
from preprocessing import load_and_clean_data

def main():
    print("=" * 70)
    print("📊 서울시 교통사고 데이터 로딩 및 분석")
    print("=" * 70)
    
    # 데이터 로딩
    print("\n데이터 로딩 중...")
    df_weather, df_vehicle, df_district = load_and_clean_data()
    
    print("\n" + "=" * 70)
    print("✅ 데이터 로딩 성공!")
    print("=" * 70)
    
    # 1. 자치구별 데이터
    print("\n" + "=" * 70)
    print("📍 자치구별 교통사고 데이터")
    print("=" * 70)
    print(f"Shape: {df_district.shape}")
    print(f"Columns: {list(df_district.columns)}")
    print(f"\n연도 범위: {df_district['연도'].min()} ~ {df_district['연도'].max()}")
    print(f"자치구 수: {df_district['자치구'].nunique()}")
    print(f"\n자치구 목록 ({len(sorted(df_district['자치구'].unique()))}개):")
    districts = sorted(df_district['자치구'].unique())
    for i in range(0, len(districts), 5):
        print("  ", ", ".join(districts[i:i+5]))
    print(f"\n상위 5개 행:")
    print(df_district.head())
    
    # 2. 기상별 데이터
    print("\n" + "=" * 70)
    print("🌤️ 기상상태별 교통사고 데이터")
    print("=" * 70)
    print(f"Shape: {df_weather.shape}")
    print(f"Columns: {list(df_weather.columns)}")
    print(f"\n연도 범위: {df_weather['연도'].min()} ~ {df_weather['연도'].max()}")
    print(f"자치구 수: {df_weather['자치구'].nunique()}")
    print(f"기상상태 종류: {sorted(df_weather['기상상태'].unique())}")
    print(f"\n상위 5개 행:")
    print(df_weather.head())
    
    # 3. 차량용도별 데이터
    print("\n" + "=" * 70)
    print("🚗 차량용도별 교통사고 데이터")
    print("=" * 70)
    print(f"Shape: {df_vehicle.shape}")
    print(f"Columns: {list(df_vehicle.columns)}")
    print(f"\n연도 범위: {df_vehicle['연도'].min()} ~ {df_vehicle['연도'].max()}")
    print(f"자치구 수: {df_vehicle['자치구'].nunique()}")
    print(f"차종 종류: {sorted(df_vehicle['차종'].unique())}")
    print(f"\n상위 10개 행:")
    print(df_vehicle.head(10))
    
    # 4. 통계 요약
    print("\n" + "=" * 70)
    print("📊 데이터 통계")
    print("=" * 70)
    
    # 자치구별 통계
    print("\n▶ 2024년 자치구별 사고 건수 TOP 5:")
    top_districts = df_district[df_district['연도'] == 2024].nlargest(5, '발생건수')[['자치구', '발생건수', '사망자수', '부상자수']]
    print(top_districts.to_string(index=False))
    
    # 기상별 통계
    print("\n▶ 2024년 기상별 사고 건수:")
    weather_stats = df_weather[df_weather['연도'] == 2024].groupby('기상상태')['발생건수'].sum().sort_values(ascending=False)
    for weather, count in weather_stats.items():
        print(f"  {weather}: {count:,.0f}건")
    
    # 차종별 통계
    print("\n▶ 2024년 차종별 사고 건수:")
    vehicle_stats = df_vehicle[df_vehicle['연도'] == 2024].groupby('차종')['발생건수'].sum().sort_values(ascending=False)
    for vehicle, count in vehicle_stats.items():
        print(f"  {vehicle}: {count:,.0f}건")
    
    # 최종 요약
    print("\n" + "=" * 70)
    print("📋 전체 데이터 요약")
    print("=" * 70)
    print(f"✓ 자치구별 데이터: {df_district.shape[0]:,}개 행 × {df_district.shape[1]}개 열")
    print(f"✓ 기상별 데이터: {df_weather.shape[0]:,}개 행 × {df_weather.shape[1]}개 열")
    print(f"✓ 차량용도별 데이터: {df_vehicle.shape[0]:,}개 행 × {df_vehicle.shape[1]}개 열")
    print(f"\n총 데이터 레코드 수: {df_district.shape[0] + df_weather.shape[0] + df_vehicle.shape[0]:,}개")
    
    print("\n" + "=" * 70)
    print("✅ 모든 데이터가 정상적으로 로드되었습니다!")
    print("=" * 70)

if __name__ == '__main__':
    main()

