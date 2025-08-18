'''read mission computer main.log'''
import os
import json


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
            # ex ) log : '2023-08-27 10:25:00,INFO,Engine ignition sequence started.'

            lines = file.readlines()
            # 날짜/시간, 로그레벨, 메시지
            # 로그 파일 내용을 콤마(,)를 기준으로 날짜/시간과 메시지를 분리하여 Python의 리스트(List) 객체로 전환
            log_content = []
            for line in lines:
                if line.strip():
                    [time, _, message] = line.strip().split(',', 2)
                    log_content.append([time.strip(), message.strip()])
            # 로그 내용을 시간 역순으로 정렬
            log_content.sort(key=lambda x: x[0], reverse=True)
            # log_content pretty print
            for entry in log_content:
                print(f'{entry[0]}: {entry[1]}')
            # 정렬된 리스트를 사전(Dict) 객체로 변환
            log_dict = {entry[0]: entry[1] for entry in log_content}
            # 변환된 Dict 객체를 mission_computer_main.json 파일로 저장 (UTF-8, JSON 포맷)

            json_file = os.path.join(base_dir, 'mission_computer_main.json')
            with open(json_file, 'w', encoding='utf-8') as json_out:
                json.dump(log_dict, json_out, ensure_ascii=False, indent=4)
            print(f'Log content saved to: {json_file}')

    except FileNotFoundError:
        print('Log file not found.')
    # deal with decoding errors
    except UnicodeDecodeError:
        print('Error decoding the log file. Please check the file encoding.')
    except OSError as e:
        print(f'OS error occurred: {e}')
    except json.JSONDecodeError as e:
        print(f'JSON decode error: {e}')


if __name__ == "__main__":
    read_log()
