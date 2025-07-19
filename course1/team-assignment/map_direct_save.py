import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "dataFile")

area_map = pd.read_csv(os.path.join(data_dir, "area_map.csv"))
area_struct = pd.read_csv(os.path.join(data_dir, "area_struct.csv"))
area_category = pd.read_csv(os.path.join(data_dir, "area_category.csv"))


# 구조물 이름 변환 및 병합
area_struct = area_struct.merge(area_category, how="left", on="category")
merged = area_struct.merge(area_map, how="left", on=["x", "y"])

# 좌표 집합 만들기
construction_sites = set(
    zip(
        merged[merged["ConstructionSite"] == 1]["x"],
        merged[merged["ConstructionSite"] == 1]["y"],
    )
)
my_home = merged[merged["struct"] == "MyHome"][["x", "y"]].iloc[0]
cafe = merged[merged["struct"] == "BandalgomCoffee"][["x", "y"]].iloc[0]

start = (my_home["x"], my_home["y"])
goal = (cafe["x"], cafe["y"])


# BFS로 최단 경로 탐색
def bfs(start, goal, construction_sites, valid_points):
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상하좌우

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in visited:
                continue
            if (nx, ny) in construction_sites:
                continue
            if (nx, ny) not in valid_points:
                continue
            visited.add((nx, ny))
            queue.append(((nx, ny), path + [(nx, ny)]))
    return None


valid_points = set(zip(merged["x"], merged["y"]))
path = bfs(start, goal, construction_sites, valid_points)

if path is None:
    print("경로를 찾을 수 없습니다.")
else:
    # 경로를 CSV로 저장
    path_df = pd.DataFrame(path, columns=["x", "y"])
    path_df.to_csv("home_to_cafe.csv", index=False)
    print("경로가 home_to_cafe.csv로 저장되었습니다.")

    # 지도 시각화
    x_min, x_max = merged["x"].min(), merged["x"].max()
    y_min, y_max = merged["y"].min(), merged["y"].max()

    plt.figure(figsize=(10, 8))
    # 그리드
    for x in range(int(x_min), int(x_max) + 1):
        plt.axvline(x=x, color="lightgray", linestyle="--", linewidth=0.5, zorder=0)
    for y in range(int(y_min), int(y_max) + 1):
        plt.axhline(y=y, color="lightgray", linestyle="--", linewidth=0.5, zorder=0)

    # 건설 현장
    construction = merged[merged["ConstructionSite"] == 1]
    plt.scatter(
        construction["x"],
        construction["y"],
        marker="s",
        s=400,
        color="gray",
        label="Construction Site",
        zorder=3,
    )

    # 아파트/빌딩
    for struct in ["Apartment", "Building"]:
        subset = merged[
            (merged["struct"] == struct) & (merged["ConstructionSite"] != 1)
        ]
        plt.scatter(
            subset["x"],
            subset["y"],
            marker="o",
            s=300,
            color="#8B4513",
            label=struct,
            zorder=2,
        )

    # 반달곰 커피
    cafe_df = merged[
        (merged["struct"] == "BandalgomCoffee") & (merged["ConstructionSite"] != 1)
    ]
    plt.scatter(
        cafe_df["x"],
        cafe_df["y"],
        marker="s",
        s=400,
        color="green",
        label="Bandalgom Coffee",
        zorder=4,
    )

    # 내 집
    myhome_df = merged[
        (merged["struct"] == "MyHome") & (merged["ConstructionSite"] != 1)
    ]
    plt.scatter(
        myhome_df["x"],
        myhome_df["y"],
        marker="^",
        s=400,
        color="green",
        label="My Home",
        zorder=4,
    )

    # 경로(빨간 선)
    path_x, path_y = zip(*path)
    plt.plot(path_x, path_y, color="red", linewidth=4, label="Path", zorder=5)

    # 범례
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc="upper right")

    plt.xlim(x_min - 1, x_max + 1)
    plt.ylim(y_max + 1, y_min - 1)
    plt.gca().invert_yaxis()
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Shortest Path: My Home to Bandalgom Coffee")
    plt.tight_layout()
    plt.savefig("map_final.png")
    plt.close()
    print("지도 시각화가 map_final.png로 저장되었습니다.")
