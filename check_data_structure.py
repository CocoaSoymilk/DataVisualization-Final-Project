"""
데이터 구조 확인 스크립트
"""
import pandas as pd
import os

data_dir = 'DATA'

print("=" * 80)
print("1. 자치구별 데이터 구조 확인")
print("=" * 80)
df1 = pd.read_csv(os.path.join(data_dir, '교통사고+현황(구별)_20251025143628.csv'), encoding='utf-8-sig')
print(f"Shape: {df1.shape}")
print(f"\n첫 5개 컬럼:")
print(df1.columns[:5].tolist())
print(f"\n첫 3행:")
print(df1.head(3))

print("\n" + "=" * 80)
print("2. 기상상태별 데이터 구조 확인")
print("=" * 80)
df2 = pd.read_csv(os.path.join(data_dir, '기상상태별+교통사고+현황_20251025143706.csv'), encoding='utf-8-sig')
print(f"Shape: {df2.shape}")
print(f"\n모든 컬럼:")
print(df2.columns.tolist())
print(f"\n첫 5행:")
print(df2.head(5))

print("\n" + "=" * 80)
print("3. 차량용도별 데이터 구조 확인")
print("=" * 80)
df3 = pd.read_csv(os.path.join(data_dir, '차량용도별+교통사고+현황_20251025143808.csv'), encoding='utf-8-sig')
print(f"Shape: {df3.shape}")
print(f"\n첫 5개 컬럼:")
print(df3.columns[:5].tolist())
print(f"\n첫 5행:")
print(df3.head(5))

