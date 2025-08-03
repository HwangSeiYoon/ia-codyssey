import os
import pandas as pd

class AreaMap:
    def __init__(self, data_dir):
        self.area_map = pd.read_csv(os.path.join(data_dir,"area_map.csv"))
        self.area_struct = pd.read_csv(os.path.join(data_dir,"area_struct.csv"))
        self.area_category = pd.read_csv(os.path.join(data_dir,"area_category.csv"))
        self.merged = None
    def merge_data(self):
        # 2. 구조물 ID를 이름으로 변환
        self.area_struct = self.area_struct.merge(self.area_category, how='left', on='category')

        # 3. 세 데이터 병합 (좌표 기준)
        self.merged = self.area_struct.merge(self.area_map, how='left', on=['x', 'y'])
        return self.merged
    
    def filter_area(self, area_num):
        if self.merged is None:
            self.merge_data()
        filtered = self.merged[self.merged['area'] == area_num]
        return filtered
    
    def print_area_data(self, area_num):
        filtered = self.filter_area(area_num)
        print(f"\n=== area {area_num} 데이터 ===")
        print(filtered)
        if "struct" in filtered.columns:
            print("\n=== area {} 구조물 종류별 통계 ===".format(area_num))
            print(filtered["struct"].value_counts())
        else:
            print("\n[경고] area{} 데이터에 'struct' 컬럼이 없습니다. 컬럼 목록: {}".format(area_num, filtered.columns))
    
def main():
    # 모든 행/열 생략 없이 출력
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)


    # base_dir: 현재 파일의 디렉토리 경로
    # data_dir: 데이터 파일이 있는 디렉토리 경로
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "dataFile")

    area_map = AreaMap(data_dir)
    area_map.merge_data()
    area_map.print_area_data(area_num=1)

if __name__ == "__main__":
    main()