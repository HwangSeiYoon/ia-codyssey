import matplotlib.pyplot as plt
import pandas as pd
import os
from caffee_map import AreaMap

def draw_area_map(save_path=None):
    # AreaMap 클래스 인스턴스 생성 및 데이터 병합
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "dataFile")
    area_map = AreaMap(data_dir)
    merged = area_map.merge_data()

    # 좌표 범위 계산
    x_min, x_max = merged['x'].min(), merged['x'].max()
    y_min, y_max = merged['y'].min(), merged['y'].max()

    plt.figure(figsize=(x_max-x_min+1, y_max-y_min+1))

    # 그리드 라인
    for x in range(int(x_min), int(x_max) + 1):
        plt.axvline(x=x, color='lightgray', linestyle='--', linewidth=0.5, zorder=0)
    for y in range(int(y_min), int(y_max) + 1):
        plt.axhline(y=y, color='lightgray', linestyle='--', linewidth=0.5, zorder=0)

    # 건설 현장 먼저 그림 (겹칠 때 우선) (회색 사각형)
    # ConstructionSite가 1인 좌표만 추출

    construction = merged[merged['ConstructionSite'] == 1]
    plt.scatter(construction['x'], construction['y'], marker='s', s=400, color='gray', label='Construction Site', zorder=3)

    # 아파트와 빌딩(갈색 원형)
    for struct in ['Apartment', 'Building']:
        subset = merged[(merged['struct'] == struct) & (merged['ConstructionSite'] != 1)]
        if not subset.empty:
            plt.scatter(subset['x'], subset['y'], marker='o', s=300, color='brown', label=struct, zorder=2)

    # 반달곰 커피(녹색 사각형)
    cafe = merged[(merged['struct'] == 'BandalgomCoffee') & (merged['ConstructionSite'] != 1)]
    plt.scatter(cafe['x'], cafe['y'], marker='s', s=400, color='green', label='Bandalgom Coffee', zorder=4)


    # 내 집 (녹색 삼각형)
    my_home = merged[(merged['struct'] == 'MyHome') & (merged['ConstructionSite'] != 1)]
    plt.scatter(my_home['x'], my_home['y'], marker='^', s=300, color='green', label='My Home', zorder=5)

    # 범례 (중복 방지)
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper left')


    # 축 설정
    plt.xlim(x_min - 1, x_max + 1)
    plt.ylim(y_min - 1, y_max + 1)
    # gca(): 현재 Axes 객체를 가져옴
    # set_aspect('equal')는 x축과 y축의 단위 길이를 동일하게 설정하여 비율을 유지
    # adjustable='box'는 박스 형태로 유지
    plt.gca().set_aspect('equal', adjustable='box')
    # y축의 역순 설정
    plt.gca().invert_yaxis()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Area 1 Map Visualization')

    # tight_layout()는 레이아웃을 자동으로 조정하여 요소들이 겹치지 않도록 함
    plt.tight_layout()

    # Save image
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    
    # 이미지 저장 경로 설정
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "map.png")
    
    draw_area_map(save_path=save_path)