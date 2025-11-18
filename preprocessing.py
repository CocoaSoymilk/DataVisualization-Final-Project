"""
데이터 전처리 모듈
서울시 교통사고 데이터 로드 및 변환
"""

import pandas as pd
import numpy as np
import os

def load_and_clean_data():
    """
    3개 CSV 파일 로드 및 전처리
    
    반환값:
    - df_weather: 기상별 데이터 (long format)
    - df_vehicle: 차종별 데이터 (long format)
    - df_district: 자치구별 데이터 (long format)
    """
    
    data_dir = 'DATA'
    
    # 1. 자치구별 데이터 로드 및 변환
    print("자치구별 데이터 로드 중...")
    df_district = load_district_data(os.path.join(data_dir, '교통사고+현황(구별)_20251025143628.csv'))
    
    # 2. 기상 데이터 로드 및 변환
    print("기상별 데이터 로드 중...")
    df_weather = load_weather_data(os.path.join(data_dir, '기상상태별+교통사고+현황_20251025143706.csv'))
    
    # 3. 차량 데이터 로드 및 변환
    print("차량용도별 데이터 로드 중...")
    df_vehicle = load_vehicle_data(os.path.join(data_dir, '차량용도별+교통사고+현황_20251025143808.csv'))
    
    print("데이터 로드 완료!")
    return df_weather, df_vehicle, df_district


def load_district_data(filepath):
    """자치구별 데이터 로드 및 변환"""
    df = pd.read_csv(filepath, encoding='utf-8-sig', header=None)
    
    # 데이터는 3행(index 2)부터 시작 (0,1행은 헤더)
    new_data = []

    for idx in range(2, len(df)):
        row = df.iloc[idx]
        district_1 = str(row[0])  # 항상 "합계"
        district_2 = str(row[1])  # "소계" 또는 자치구명

        # '소계' 제외 (전체 합계는 제외)
        if district_2 == '소계':
            continue
        
        # 각 연도별 데이터 추출
        col_idx = 2
        for year in range(2024, 2009, -1):  # 2024부터 2010까지
            # 각 연도는 6개 컬럼: 발생건수, 자동차1만대당, 사망자수, 인구10만명당사망, 부상자수, 인구10만명당부상
            try:
                발생건수 = float(row[col_idx]) if pd.notna(row[col_idx]) and row[col_idx] != '-' else 0
                자동차대당 = float(row[col_idx + 1]) if pd.notna(row[col_idx + 1]) and row[col_idx + 1] != '-' else 0
                사망자수 = float(row[col_idx + 2]) if pd.notna(row[col_idx + 2]) and row[col_idx + 2] != '-' else 0
                사망자비율 = float(row[col_idx + 3]) if pd.notna(row[col_idx + 3]) and row[col_idx + 3] != '-' else 0
                부상자수 = float(row[col_idx + 4]) if pd.notna(row[col_idx + 4]) and row[col_idx + 4] != '-' else 0
                부상자비율 = float(row[col_idx + 5]) if pd.notna(row[col_idx + 5]) and row[col_idx + 5] != '-' else 0
                
                new_data.append({
                    '연도': year,
                    '자치구': district_2,
                    '발생건수': 발생건수,
                    '자동차1만대당발생건수': 자동차대당,
                    '사망자수': 사망자수,
                    '인구10만명당사망자수': 사망자비율,
                    '부상자수': 부상자수,
                    '인구10만명당부상자수': 부상자비율
                })
            except Exception as e:
                pass
            
            col_idx += 6
    
    df_clean = pd.DataFrame(new_data)
    return df_clean


def load_weather_data(filepath):
    """기상별 데이터 로드 및 변환"""
    # 간단한 방식으로 재작성 - 연도별로 직접 매핑
    df = pd.read_csv(filepath, encoding='utf-8-sig', header=None)
    
    new_data = []
    
    # 데이터는 4행(index 3)부터 시작
    # 각 행은: "합계", 자치구명, 항목, 그 다음 연도별 데이터
    for idx in range(3, len(df)):
        row = df.iloc[idx]
        district_1 = str(row[0])  # 항상 "합계"
        district_2 = str(row[1])  # "소계" 또는 자치구명
        항목 = str(row[2])
        
        # '소계' 제외 (전체 합계는 제외)
        if district_2 == '소계':
            continue
        
        # 직접 컬럼 인덱스 계산
        # 2024년: 3~8 (6개)
        # 2023년: 9~15 (7개)
        # 2022년: 16~22 (7개)
        # 나머지도 7개씩
        
        year_configs = [
            (2024, 3, ['소계', '맑음', '흐림', '비', '눈', '기타/불명']),
            (2023, 9, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2022, 16, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2021, 23, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2020, 30, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2019, 37, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2018, 44, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2017, 51, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2016, 58, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2015, 65, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2014, 72, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2013, 79, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2012, 86, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2011, 93, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
            (2010, 100, ['소계', '맑음', '흐림', '비', '안개', '눈', '기타/불명']),
        ]
        
        for year, start_col, weather_list in year_configs:
            for i, weather_name in enumerate(weather_list):
                try:
                    col_idx = start_col + i
                    if col_idx < len(row):
                        value = row[col_idx]
                        if pd.isna(value) or value == '-':
                            value = 0
                        else:
                            value = float(value)
                        
                        new_data.append({
                            '연도': year,
                            '자치구': district_2,
                            '항목': 항목,
                            '기상상태': weather_name,
                            '값': value
                        })
                except:
                    continue
    
    df_clean = pd.DataFrame(new_data)
    
    # 디버깅: 데이터 확인
    if len(df_clean) == 0:
        print("WARNING: 기상 데이터가 비어있습니다!")
        return pd.DataFrame()
    
    print(f"✓ 기상 데이터 레코드 수: {len(df_clean)}")
    
    # Pivot해서 발생건수, 사망자, 부상자 컬럼으로 분리
    df_pivot = df_clean.pivot_table(
        index=['연도', '자치구', '기상상태'],
        columns='항목',
        values='값',
        aggfunc='sum'
    ).reset_index()
    
    # 컬럼명 정리
    df_pivot.columns.name = None
    if '발생건수 (건)' in df_pivot.columns:
        df_pivot = df_pivot.rename(columns={
            '발생건수 (건)': '발생건수',
            '사망자 (명)': '사망자수',
            '부상자 (명)': '부상자수'
        })
    
    # NaN을 0으로 채우기
    df_pivot = df_pivot.fillna(0)
    
    return df_pivot


def load_vehicle_data(filepath):
    """차량용도별 데이터 로드 및 변환"""
    df = pd.read_csv(filepath, encoding='utf-8-sig', header=None)
    
    new_data = []
    
    # 데이터는 8행(index 7)부터 시작 (0~6행은 헤더, 7행은 소계)
    for idx in range(7, len(df)):
        row = df.iloc[idx]
        district_1 = str(row[0])  # 항상 "합계"
        district_2 = str(row[1])  # "소계" 또는 자치구명
        
        # '소계' 제외 (전체 합계는 제외)
        if district_2 == '소계':
            continue
        
        # 각 연도별로 차종별 데이터 추출
        col_idx = 2
        for year in range(2024, 2009, -1):  # 2024부터 2010까지
            # 각 연도는 51개 컬럼
            try:
                # 소계 (0-2)
                소계_발생 = float(row[col_idx]) if pd.notna(row[col_idx]) and row[col_idx] != '-' else 0
                소계_사망 = float(row[col_idx + 1]) if pd.notna(row[col_idx + 1]) and row[col_idx + 1] != '-' else 0
                소계_부상 = float(row[col_idx + 2]) if pd.notna(row[col_idx + 2]) and row[col_idx + 2] != '-' else 0
                
                # 사업용차량 소계 (3-5)
                사업용_발생 = float(row[col_idx + 3]) if pd.notna(row[col_idx + 3]) and row[col_idx + 3] != '-' else 0
                사업용_사망 = float(row[col_idx + 4]) if pd.notna(row[col_idx + 4]) and row[col_idx + 4] != '-' else 0
                사업용_부상 = float(row[col_idx + 5]) if pd.notna(row[col_idx + 5]) and row[col_idx + 5] != '-' else 0
                
                # 비사업용차량 소계 (27-29)
                비사업용_발생 = float(row[col_idx + 27]) if pd.notna(row[col_idx + 27]) and row[col_idx + 27] != '-' else 0
                비사업용_사망 = float(row[col_idx + 28]) if pd.notna(row[col_idx + 28]) and row[col_idx + 28] != '-' else 0
                비사업용_부상 = float(row[col_idx + 29]) if pd.notna(row[col_idx + 29]) and row[col_idx + 29] != '-' else 0
                
                # 이륜차 (42-44)
                이륜차_발생 = float(row[col_idx + 42]) if pd.notna(row[col_idx + 42]) and row[col_idx + 42] != '-' else 0
                이륜차_사망 = float(row[col_idx + 43]) if pd.notna(row[col_idx + 43]) and row[col_idx + 43] != '-' else 0
                이륜차_부상 = float(row[col_idx + 44]) if pd.notna(row[col_idx + 44]) and row[col_idx + 44] != '-' else 0
                
                # 자전거 (45-47)
                자전거_발생 = float(row[col_idx + 45]) if pd.notna(row[col_idx + 45]) and row[col_idx + 45] != '-' else 0
                자전거_사망 = float(row[col_idx + 46]) if pd.notna(row[col_idx + 46]) and row[col_idx + 46] != '-' else 0
                자전거_부상 = float(row[col_idx + 47]) if pd.notna(row[col_idx + 47]) and row[col_idx + 47] != '-' else 0
                
                # 각 차종별로 레코드 추가
                vehicle_types = [
                    ('소계', 소계_발생, 소계_사망, 소계_부상),
                    ('사업용차량', 사업용_발생, 사업용_사망, 사업용_부상),
                    ('비사업용차량', 비사업용_발생, 비사업용_사망, 비사업용_부상),
                    ('이륜차', 이륜차_발생, 이륜차_사망, 이륜차_부상),
                    ('자전거', 자전거_발생, 자전거_사망, 자전거_부상)
                ]
                
                for vtype, 발생, 사망, 부상 in vehicle_types:
                    new_data.append({
                        '연도': year,
                        '자치구': district_2,
                        '차종': vtype,
                        '발생건수': 발생,
                        '사망자수': 사망,
                        '부상자수': 부상
                    })
                
            except Exception as e:
                pass
            
            col_idx += 51  # 다음 연도로 (51개 컬럼)
    
    df_clean = pd.DataFrame(new_data)
    
    print(f"✓ 차량용도별 데이터 레코드 수: {len(df_clean)}")
    
    return df_clean


if __name__ == '__main__':
    # 테스트
    df_weather, df_vehicle, df_district = load_and_clean_data()
    
    print("\n자치구별 데이터:")
    print(df_district.head(10))
    print(f"Shape: {df_district.shape}")
    
    print("\n기상별 데이터:")
    print(df_weather.head(10))
    print(f"Shape: {df_weather.shape}")
    
    print("\n차량용도별 데이터:")
    print(df_vehicle.head(10))
    print(f"Shape: {df_vehicle.shape}")

