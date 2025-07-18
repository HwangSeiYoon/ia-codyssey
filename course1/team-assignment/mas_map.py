import pandas as pd
import matplotlib.pyplot as plt

# 모든 행/열 생략 없이 출력
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

import os
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "dataFile")

area_map = pd.read_csv(os.path.join(data_dir, "area_map.csv"))
area_struct = pd.read_csv(os.path.join(data_dir, "area_struct.csv"))
area_category = pd.read_csv(os.path.join(data_dir, "area_category.csv"))

print("=== area_map.csv ===")
print(area_map)
print("\n=== area_struct.csv ===")
print(area_struct)
print("\n=== area_category.csv ===")
print(area_category)

# 2. 구조물 ID를 이름으로 변환
area_struct = area_struct.merge(area_category, how="left", on="category")

# 3. 세 데이터 병합 (좌표 기준)
merged = area_struct.merge(area_map, how="left", on=["x", "y"])

# 4. area 기준 정렬
merged = merged.sort_values(by="area")

# 5. area 1만 필터링
area1 = merged[merged["area"] == 1]

print("\n=== area 1 데이터 ===")
print(area1)

# (보너스) 구조물 종류별 요약 통계
if "struct" in area1.columns:
    print("\n=== area 1 구조물 종류별 통계 ===")
    print(area1["struct"].value_counts())
else:
    print("\n[경고] area1 데이터에 'struct' 컬럼이 없습니다. 컬럼 목록:", area1.columns)
