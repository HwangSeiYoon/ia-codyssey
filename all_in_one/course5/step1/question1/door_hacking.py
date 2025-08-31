'''
A script to brute-force the password of a ZIP file using multiprocessing.
'''
import zipfile
import io
import time
import zlib
from itertools import product
from multiprocessing import Process, Value, Lock, Array, current_process
import os
import sys
from absl import logging

logging.set_verbosity(logging.INFO)

# set working directory
WORKING_DIR = os.path.dirname(
    '/Users/n99102/ia-codyssey/all_in_one/course5/step1/question1/')
ZIP_PATH = os.path.join(WORKING_DIR, 'emergency_storage_key.zip')
PASS_PATH = os.path.join(WORKING_DIR, 'password.txt')
# for password cracking
CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'


def check_files():
    '''
    Check if necessary files exist.
    '''
    if not os.path.exists(ZIP_PATH):
        logging.error(f'[오류] ZIP 파일이 존재하지 않습니다: {ZIP_PATH}')
        return False
    return True


# 파일 읽기 함수
def read_zip_file(zip_path: str):
    '''
    Read a ZIP file and return its binary content and the name of the first file.
    '''
    with open(zip_path, 'rb') as f:
        zip_bytes = f.read()
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zip_file:
        file_to_test = zip_file.namelist()[0]
    return zip_bytes, file_to_test


# prefix 분할 함수
def split_prefixes(prefixes, process_count):
    '''
    Split the list of prefixes into chunks for each process.
    '''
    step = len(prefixes) // process_count
    chunks = [
        prefixes[i * step:(i + 1) * step] for i in range(process_count - 1)
    ]
    chunks.append(prefixes[(process_count - 1) * step:])
    return chunks


# 프로세스 실행 함수
def run_processes(zip_bytes, file_to_test, pw_length, chunks, found_flag,
                  pw_holder, lock):
    '''
    Run password cracking processes.
    '''
    processes = []
    for idx, chunk in enumerate(chunks):
        proc = Process(target=try_passwords,
                       args=(zip_bytes, file_to_test, CHARS, pw_length, chunk,
                             found_flag, pw_holder, lock),
                       name=f'P{idx + 1}')
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()


def try_passwords(zip_binary, target_file, charset, pw_length, prefix_group,
                  found_flag, pw_holder, lock):
    '''
    Try all password combinations for the given zip file.
    zip_binary : the binary content of the zip file
    target_file : the name of the file to extract
    charset : the character set to use for generating passwords
    pw_length : the length of the passwords to try
    prefix_group : a list of prefix strings to use
    found_flag : a multiprocessing.Value to indicate if the password has been found
    pw_holder : a multiprocessing.Array to hold the found password
    lock : a multiprocessing.Lock to synchronize access to shared resources
    '''
    # Create a BytesIO object from the zip binary
    # the reason why we use BytesIO is to avoid writing the zip file to disk
    zip_data = io.BytesIO(zip_binary)
    start_time = time.time()
    attempts = 0
    with zipfile.ZipFile(zip_data) as zip_obj:
        for prefix in prefix_group:
            if found_flag.value:
                return
            for tail in product(charset, repeat=pw_length - 1):
                if found_flag.value:
                    return
                candidate = prefix + ''.join(tail)
                attempts += 1
                try:
                    with zip_obj.open(target_file,
                                      pwd=candidate.encode('ascii')) as f:
                        data = f.read(1)
                    if data:
                        with lock:
                            if not found_flag.value:
                                found_flag.value = True
                                for i, c in enumerate(candidate.encode('ascii')):
                                    pw_holder[i] = c
                                pw_holder[len(candidate):] = b'\x00' * (
                                    len(pw_holder) - len(candidate))
                                elapsed = time.time() - start_time
                                logging.info(f'\nSUCCESS! password: {candidate}')
                                logging.info(f'elapsed time: {elapsed:.2f}seconds')
                        return
                except (RuntimeError, zipfile.BadZipFile, zlib.error):
                    pass
                if attempts % 100000 == 0:
                    elapsed = time.time() - start_time
                    logging.info(
                        f'{candidate} [{current_process().name}] {attempts}th attempt :\n'
                        f'  {elapsed:.1f} seconds elapsed')


def main():
    '''
    Main function to orchestrate the password cracking.
    '''
    if not check_files():
        sys.exit(1)

    logging.info(f'[시작] 암호 해제 시도: {ZIP_PATH}')
    logging.info(
        f'시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}'
    )

    pw_length = 6
    process_count = os.cpu_count()
    logging.info(f'프로세스 수: {process_count}, 비밀번호 길이: {pw_length}')

    zip_bytes, file_to_test = read_zip_file(ZIP_PATH)
    prefixes = list(CHARS)
    chunks = split_prefixes(prefixes, process_count)
    found_flag = Value('b', False)
    pw_holder = Array('c', pw_length + 1)
    lock = Lock()

    run_processes(zip_bytes, file_to_test, pw_length, chunks, found_flag,
                  pw_holder, lock)

    if found_flag.value:
        password = bytes(pw_holder[:pw_length]).decode('utf-8').rstrip('\x00')
        logging.info(f'[성공] 암호: {password}')
        with open(PASS_PATH, 'w', encoding='utf-8') as f:
            f.write(password)
    else:
        logging.info('[실패] 암호를 찾지 못했습니다.')

    logging.info(
        f'종료 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}'
    )


if __name__ == "__main__":
    main()
    logging.info(
        f'종료 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}'
    )
