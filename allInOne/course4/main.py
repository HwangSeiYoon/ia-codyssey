'''read mission computer main.log'''
import os
import json

DANGER_KEYWORDS = ['폭발', '누출', '고온', 'Oxygen']


def read_log():
    '''
    Reads a log file named 'mission_computer_main.log' located in the same directory as the script,
    parses its contents, sorts the log entries in reverse chronological order, and saves the results
    as a JSON file named 'mission_computer_main.json'.    
    '''
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(base_dir, "mission_computer_main.log")
    print(f'Reading log file from: {log_file}')
    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            log_content = []
            for line in lines:
                if line.strip() and not line.startswith('timestamp'):
                    [time, _, message] = line.strip().split(',', 2)
                    log_content.append([time.strip(), message.strip()])
            # 로그 내용을 시간 역순으로 정렬
            log_content.sort(key=lambda x: x[0], reverse=True)
            print('\n[시간 역순 정렬된 로그]')
            for entry in log_content:
                print(f'{entry[0]}: {entry[1]}')
            # 정렬된 리스트를 사전(Dict) 객체로 변환
            log_dict = {entry[0]: entry[1] for entry in log_content}
            # 변환된 Dict 객체를 mission_computer_main.json 파일로 저장 (UTF-8, JSON 포맷)
            json_file = os.path.join(base_dir, 'mission_computer_main.json')
            with open(json_file, 'w', encoding='utf-8') as json_out:
                json.dump(log_dict, json_out, ensure_ascii=False, indent=4)
            print(f'Log content saved to: {json_file}')

            # 위험 키워드 필터링 및 저장 (보너스)
            danger_logs = [
                entry for entry in log_content
                if any(k in entry[1] for k in DANGER_KEYWORDS)
            ]
            if danger_logs:
                danger_dict = {entry[0]: entry[1] for entry in danger_logs}
                danger_file = os.path.join(base_dir, 'danger_logs.json')
                with open(danger_file, 'w', encoding='utf-8') as f:
                    json.dump(danger_dict, f, ensure_ascii=False, indent=4)
                print(f'Danger logs saved to: {danger_file}')

            # 검색 기능 (보너스)
            search_str = input('검색할 문자열을 입력하세요(엔터시 건너뜀): ').strip()
            if search_str:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                results = {k: v for k, v in data.items() if search_str in v}
                print(f'\n[검색 결과: "{search_str}"]')
                if results:
                    for k, v in results.items():
                        print(f'{k}: {v}')
                else:
                    print('검색 결과가 없습니다.')

    except FileNotFoundError:
        print('Log file not found.')
    # deal with decoding errors
    except UnicodeDecodeError:
        print('Error decoding the log file. Please check the file encoding.')
    except OSError as e:
        print(f'OS error occurred: {e}')
    except json.JSONDecodeError as e:
        print(f'JSON decode error: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == "__main__":
    read_log()
