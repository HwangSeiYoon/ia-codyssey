import csv
import struct
import os

CSV_FILE = "Mars_Base_Inventory_List.csv"
base_dir = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(base_dir, CSV_FILE)

DANGER_CSV = "Mars_Base_Inventory_danger.csv"

BIN_FILE = "Mars_Base_Inventory_List.bin"


def read_csv_to_list(filename):
    items = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                # 인화성 지수는 float로 변환
                try:
                    row[2] = float(row[2])
                except (ValueError, IndexError):
                    row[2] = 0.0
                items.append(row)
        return header, items
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {filename}")
        return None, []
    except Exception as e:
        print(f"CSV 읽기 오류: {e}")
        return None, []


def print_items(header, items):
    print("\n[적재물 목록]")
    print(", ".join(header))
    for row in items:
        print(", ".join(
            [str(x) if not isinstance(x, float) else f"{x:.3f}" for x in row]))


def sort_by_flammability(items):
    return sorted(items, key=lambda x: x[2], reverse=True)


def filter_danger(items):
    return [row for row in items if row[2] >= 0.7]


def save_csv(filename, header, items):
    try:
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in items:
                writer.writerow([row[0], row[1], f"{row[2]:.3f}"])
        print(f"위험 적재물 CSV 저장 완료: {filename}")
    except Exception as e:
        print(f"CSV 저장 오류: {e}")


def save_bin(filename, items):
    try:
        with open(filename, "wb") as f:
            for row in items:
                # 이름, 타입은 30바이트, 인화성 지수는 float
                name = row[0][:30].ljust(30)
                typ = row[1][:30].ljust(30)
                f.write(name.encode("utf-8"))
                f.write(typ.encode("utf-8"))
                f.write(struct.pack("f", float(row[2])))
        print(f"이진 파일 저장 완료: {filename}")
    except Exception as e:
        print(f"이진 파일 저장 오류: {e}")


def load_bin(filename):
    items = []
    try:
        with open(filename, "rb") as f:
            while True:
                name = f.read(30)
                if not name:
                    break
                typ = f.read(30)
                flammability = f.read(4)
                if not (name and typ and flammability):
                    break
                name = name.decode("utf-8").strip()
                typ = typ.decode("utf-8").strip()
                flammability = struct.unpack("f", flammability)[0]
                items.append([name, typ, flammability])
        return items
    except Exception as e:
        print(f"이진 파일 읽기 오류: {e}")
        return []


def main():
    while True:
        print("\n=== Mars 기지 적재물 관리 ===")
        print("1. 적재물 목록 출력")
        print("2. 인화성 지수 내림차순 정렬 및 출력")
        print("3. 위험 적재물(0.7 이상) 필터링 및 CSV 저장")
        print("4. 정렬된 목록 이진 파일로 저장")
        print("5. 이진 파일에서 목록 읽어 출력")
        print("6. 종료")
        choice = input("메뉴 선택: ").strip()
        if choice == "1":
            header, items = read_csv_to_list(CSV_FILE)
            if header:
                print_items(header, items)
        elif choice == "2":
            header, items = read_csv_to_list(CSV_FILE)
            if header:
                sorted_items = sort_by_flammability(items)
                print_items(header, sorted_items)
        elif choice == "3":
            header, items = read_csv_to_list(CSV_FILE)
            if header:
                sorted_items = sort_by_flammability(items)
                danger_items = filter_danger(sorted_items)
                print_items(header, danger_items)
                save_csv(DANGER_CSV, header, danger_items)
        elif choice == "4":
            _, items = read_csv_to_list(CSV_FILE)
            sorted_items = sort_by_flammability(items)
            save_bin(BIN_FILE, sorted_items)
        elif choice == "5":
            items = load_bin(BIN_FILE)
            if items:
                print_items(["이름", "타입", "인화성지수"], items)
        elif choice == "6":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()
