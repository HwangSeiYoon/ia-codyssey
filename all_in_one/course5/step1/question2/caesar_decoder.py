'''
카이사르 암호 해독 프로그램
1. password.txt에서 암호문을 읽어온다.
2. caesar_cipher_decode(target_text) 함수에서 모든 자리수(1~25)로 해독 결과를 출력한다.
3. 눈으로 읽어서 맞는 결과의 자리수를 입력하면 result.txt에 저장한다.
'''

def caesar_cipher_decode(target_text):
    '''
    카이사르 암호를 자리수별로 모두 해독하여 출력하는 함수.
    '''
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    results = []
    for shift in range(1, 26):
        decoded = ''
        for char in target_text:
            # 알파벳인지 확인
            if char.isalpha():
                # 소문자/대문자 구분
                # find() 메서드를 사용하여 인덱스 찾기
                idx = alphabet.find(char.lower())
                # 인덱스가 유효한지 확인
                if idx != -1:
                    # 새로운 인덱스 계산
                    new_idx = (idx - shift) % 26
                    # 알파벳으로 변환
                    new_char = alphabet[new_idx]
                    # 대문자/소문자 구분
                    # 대문자인 경우는 대문자로, 소문자인 경우는 소문자로 변환
                    decoded += new_char if char.islower() else new_char.upper()
                else:
                    decoded += char
            # 공백 문자나 특수문자는 그대로 추가
            else:
                decoded += char
        print(f'{shift}: {decoded}')
        results.append(decoded)
    return results

def main():
    '''
    메인 함수
    '''
    # 1. 암호문 읽기
    with open('password.txt', 'r', encoding='utf-8') as f:
        cipher_text = f.read().strip()

    # 2. 자리수별 해독 결과 출력
    decoded_list = caesar_cipher_decode(cipher_text)

    # 3. 눈으로 확인 후 자리수 입력
    shift_num = int(input('정상적으로 해독된 자리수를 입력하세요(1~25): '))
    result_text = decoded_list[shift_num - 1]

    # 4. 결과 저장
    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(result_text)

if __name__ == '__main__':
    main()
