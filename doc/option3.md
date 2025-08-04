# 리눅스 DevOps 완전 가이드

## 목차
1. [하이퍼바이저](#1-하이퍼바이저)
2. [리눅스 배포판](#2-리눅스-배포판)
3. [커널](#3-커널)
4. [쉘 종류 및 특징](#4-쉘-종류-및-특징)
5. [리눅스 명령어](#5-리눅스-명령어)
6. [디렉토리 구조](#6-디렉토리-구조)
7. [계정 관리 명령어](#7-계정-관리-명령어)
8. [Git 설치 방식](#8-git-설치-방식)
9. [리눅스 에디터](#9-리눅스-에디터)

---

## 1. 하이퍼바이저

### 하이퍼바이저란?
물리적 하드웨어 위에서 여러 개의 가상머신(VM)을 실행할 수 있게 해주는 소프트웨어

### 하이퍼바이저 종류

#### Type 1 (베어메탈 하이퍼바이저)
- **특징**: 하드웨어에 직접 설치되어 실행
- **성능**: 높은 성능, 낮은 오버헤드
- **사용 용도**: 데이터센터, 엔터프라이즈 환경
- **예시**:
  - VMware vSphere/ESXi
  - Microsoft Hyper-V Server
  - Citrix XenServer
  - KVM (Linux)

#### Type 2 (호스트 기반 하이퍼바이저)
- **특징**: 호스트 OS 위에서 애플리케이션처럼 실행
- **성능**: 상대적으로 낮은 성능
- **사용 용도**: 개발, 테스트, 개인 사용
- **예시**:
  - Oracle VirtualBox
  - VMware Workstation/Fusion
  - Parallels Desktop
  - QEMU

### 하이퍼바이저 비교

| 구분 | Type 1 | Type 2 |
|------|--------|--------|
| **설치 위치** | 하드웨어 직접 | 호스트 OS 위 |
| **성능** | 높음 | 보통 |
| **관리 복잡도** | 높음 | 낮음 |
| **비용** | 높음 | 낮음 (무료 옵션 많음) |
| **용도** | 운영 환경 | 개발/테스트 |

---

## 2. 리눅스 배포판

### 주요 배포판 계열

#### Debian 계열
**특징**: 안정성 중시, 패키지 관리자 `apt`
- **Ubuntu**: 사용자 친화적, 데스크톱 및 서버용
- **Debian**: 매우 안정적, 서버용
- **Linux Mint**: Ubuntu 기반, 데스크톱 중심
- **Kali Linux**: 보안 테스트용

#### Red Hat 계열
**특징**: 엔터프라이즈 환경, 패키지 관리자 `yum`/`dnf`
- **RHEL (Red Hat Enterprise Linux)**: 상용 엔터프라이즈
- **CentOS**: RHEL 무료 버전 (2021년 종료)
- **Fedora**: 최신 기술 테스트베드
- **Rocky Linux**: CentOS 대체

#### SUSE 계열
**특징**: 유럽에서 인기, 패키지 관리자 `zypper`
- **openSUSE**: 커뮤니티 버전
- **SLES (SUSE Linux Enterprise Server)**: 상용 버전

#### Arch 계열
**특징**: 롤링 릴리스, 최신 패키지
- **Arch Linux**: 최소 설치, 사용자 맞춤
- **Manjaro**: Arch 기반, 사용자 친화적

### 배포판 선택 기준

| 용도 | 추천 배포판 | 이유 |
|------|-------------|------|
| **서버** | Ubuntu Server, RHEL, Debian | 안정성, 지원 |
| **데스크톱** | Ubuntu, Linux Mint, Fedora | 사용 편의성 |
| **개발** | Ubuntu, Fedora, Arch | 최신 도구 지원 |
| **보안** | Kali Linux, Parrot OS | 보안 도구 내장 |
| **학습** | Ubuntu, CentOS | 문서화, 커뮤니티 |

---

## 3. 커널

### 리눅스 커널이란?
운영체제의 핵심 부분으로, 하드웨어와 소프트웨어 간의 인터페이스 역할

### 커널의 주요 기능

#### 프로세스 관리
```bash
# 실행 중인 프로세스 확인
ps aux
top
htop

# 프로세스 종료
kill [PID]
killall [프로세스명]
```

#### 메모리 관리
```bash
# 메모리 사용량 확인
free -h
cat /proc/meminfo

# 스왑 정보
swapon --show
```

#### 파일 시스템 관리
```bash
# 파일 시스템 확인
df -h
lsblk

# 마운트된 파일 시스템
mount | column -t
```

#### 디바이스 관리
```bash
# 하드웨어 정보
lscpu          # CPU 정보
lsusb          # USB 장치
lspci          # PCI 장치
lsblk          # 블록 장치
```

### 커널 버전 확인
```bash
# 커널 버전 확인
uname -r
uname -a

# 상세 정보
cat /proc/version
```

### 커널 모듈 관리
```bash
# 로드된 모듈 확인
lsmod

# 모듈 정보 확인
modinfo [모듈명]

# 모듈 로드/언로드
sudo modprobe [모듈명]
sudo modprobe -r [모듈명]
```

---

## 4. 쉘 종류 및 특징

### 주요 쉘 비교

#### Bash (Bourne Again Shell)
```bash
# 특징
- 가장 널리 사용되는 쉘
- 풍부한 기능과 확장성
- 스크립팅에 최적화
- 히스토리, 자동완성 지원

# 설정 파일
~/.bashrc      # 대화형 쉘 설정
~/.bash_profile # 로그인 쉘 설정
~/.bash_history # 명령어 히스토리
```

#### Zsh (Z Shell)
```bash
# 특징
- Bash와 호환되면서 더 많은 기능
- 강력한 자동완성
- 테마와 플러그인 지원 (Oh My Zsh)
- 스펠링 체크

# 설정 파일
~/.zshrc       # 주 설정 파일
~/.zsh_history # 명령어 히스토리
```

#### Fish (Friendly Interactive Shell)
```bash
# 특징
- 사용자 친화적 인터페이스
- 실시간 문법 하이라이팅
- 자동 제안 기능
- 웹 기반 설정

# 설정 위치
~/.config/fish/config.fish
```

#### Dash (Debian Almquist Shell)
```bash
# 특징
- POSIX 준수 경량 쉘
- 빠른 실행 속도
- 시스템 스크립트용
- 최소한의 기능

# 사용 예
/bin/sh -> dash (Ubuntu)
```

### 쉘 비교표

| 쉘 | 크기 | 속도 | 기능 | 호환성 | 사용 용도 |
|----|------|------|------|--------|-----------|
| **Bash** | 보통 | 보통 | 풍부 | 높음 | 일반 사용, 스크립팅 |
| **Zsh** | 큼 | 보통 | 매우 풍부 | 높음 | 고급 사용자 |
| **Fish** | 보통 | 빠름 | 친화적 | 낮음 | 초보자, 대화형 |
| **Dash** | 작음 | 매우 빠름 | 최소 | 보통 | 시스템 스크립트 |

### 쉘 변경 및 확인
```bash
# 현재 쉘 확인
echo $SHELL
ps -p $$

# 사용 가능한 쉘 목록
cat /etc/shells

# 쉘 변경
chsh -s /bin/zsh        # 영구 변경
exec zsh                # 임시 변경
```

---

## 5. 리눅스 명령어

### 파일 및 디렉토리 명령어

#### 기본 조작
```bash
# 디렉토리 이동
cd /path/to/directory   # 절대 경로
cd ../parent           # 상대 경로
cd ~                   # 홈 디렉토리
cd -                   # 이전 디렉토리

# 파일 목록
ls                     # 기본 목록
ls -la                 # 상세 정보 + 숨김 파일
ls -lh                 # 사람이 읽기 쉬운 크기
ls -lt                 # 시간순 정렬

# 디렉토리 생성/삭제
mkdir directory        # 디렉토리 생성
mkdir -p path/to/dir   # 중간 경로 자동 생성
rmdir directory        # 빈 디렉토리 삭제
rm -rf directory       # 디렉토리 강제 삭제
```

#### 파일 조작
```bash
# 파일 복사/이동
cp source dest         # 파일 복사
cp -r source dest      # 디렉토리 복사
mv source dest         # 파일/디렉토리 이동/이름변경

# 파일 삭제
rm file               # 파일 삭제
rm -f file            # 강제 삭제
rm -i file            # 확인 후 삭제

# 파일 생성
touch filename        # 빈 파일 생성
echo "text" > file    # 텍스트로 파일 생성
```

### 텍스트 처리 명령어

```bash
# 파일 내용 보기
cat file              # 전체 내용
head file             # 앞 10줄
tail file             # 뒤 10줄
tail -f file          # 실시간 모니터링
less file             # 페이지 단위 보기
more file             # 페이지 단위 보기 (구버전)

# 텍스트 검색
grep "pattern" file   # 패턴 검색
grep -r "pattern" dir # 디렉토리 내 재귀 검색
grep -i "pattern" file # 대소문자 무시
grep -n "pattern" file # 줄 번호 표시

# 텍스트 처리
sort file             # 정렬
uniq file             # 중복 제거
wc file               # 라인/단어/문자 수
cut -d: -f1 /etc/passwd # 필드 추출
```

### 시스템 정보 명령어

```bash
# 시스템 정보
uname -a              # 시스템 전체 정보
hostname              # 호스트명
whoami                # 현재 사용자
id                    # 사용자 ID 정보
uptime                # 시스템 가동 시간

# 프로세스 관리
ps aux                # 모든 프로세스
top                   # 실시간 프로세스 모니터링
htop                  # 향상된 top (설치 필요)
jobs                  # 백그라운드 작업
nohup command &       # 백그라운드 실행

# 디스크 사용량
df -h                 # 파일시스템 사용량
du -sh directory      # 디렉토리 크기
du -h --max-depth=1   # 하위 디렉토리별 크기
```

### 네트워크 명령어

```bash
# 네트워크 정보
ip addr show          # IP 주소 확인
ifconfig              # 네트워크 인터페이스 (구버전)
ping google.com       # 연결성 테스트
wget url              # 파일 다운로드
curl url              # HTTP 요청

# 포트 및 연결
netstat -tlnp         # 리스닝 포트
ss -tlnp              # 소켓 정보 (최신)
lsof -i :80           # 특정 포트 사용 프로세스
```

---

## 6. 디렉토리 구조

### FHS (Filesystem Hierarchy Standard)

```
/                    # 루트 디렉토리
├── bin/            # 기본 실행 파일
├── boot/           # 부트 로더 파일
├── dev/            # 장치 파일
├── etc/            # 시스템 설정 파일
├── home/           # 사용자 홈 디렉토리
├── lib/            # 공유 라이브러리
├── media/          # 이동식 미디어 마운트
├── mnt/            # 임시 마운트 포인트
├── opt/            # 추가 소프트웨어
├── proc/           # 프로세스 정보 (가상)
├── root/           # root 사용자 홈
├── run/            # 런타임 데이터
├── sbin/           # 시스템 실행 파일
├── srv/            # 서비스 데이터
├── sys/            # 시스템 정보 (가상)
├── tmp/            # 임시 파일
├── usr/            # 사용자 프로그램
└── var/            # 가변 데이터
```

### 주요 디렉토리 상세 설명

#### /etc (Configuration Files)
```bash
/etc/passwd         # 사용자 계정 정보
/etc/shadow         # 암호화된 패스워드
/etc/group          # 그룹 정보
/etc/hosts          # 호스트 이름 매핑
/etc/fstab          # 파일시스템 마운트 설정
/etc/crontab        # 크론 작업 설정
/etc/ssh/           # SSH 설정
/etc/nginx/         # Nginx 웹서버 설정
/etc/systemd/       # systemd 서비스 설정
```

#### /var (Variable Data)
```bash
/var/log/           # 시스템 로그 파일
  ├── syslog        # 시스템 일반 로그
  ├── auth.log      # 인증 로그
  ├── nginx/        # Nginx 로그
  └── apache2/      # Apache 로그
/var/www/           # 웹 서버 문서 루트
/var/cache/         # 캐시 파일
/var/tmp/           # 임시 파일 (재부팅 후 유지)
```

#### /usr (Unix System Resources)
```bash
/usr/bin/           # 사용자 실행 파일
/usr/sbin/          # 시스템 관리 실행 파일
/usr/lib/           # 라이브러리
/usr/local/         # 로컬 설치 프로그램
  ├── bin/          # 로컬 실행 파일
  ├── lib/          # 로컬 라이브러리
  └── etc/          # 로컬 설정 파일
/usr/share/         # 공유 데이터
  ├── doc/          # 문서
  └── man/          # 매뉴얼 페이지
```

#### /home (User Home Directories)
```bash
/home/username/     # 사용자 홈 디렉토리
  ├── .bashrc       # Bash 설정
  ├── .bash_history # 명령어 히스토리
  ├── .ssh/         # SSH 키
  ├── .config/      # 애플리케이션 설정
  ├── Documents/    # 문서
  ├── Downloads/    # 다운로드
  └── Desktop/      # 데스크톱
```

### 경로 표현

#### 절대 경로 vs 상대 경로
```bash
# 절대 경로 (/ 로 시작)
/home/user/documents/file.txt
/etc/nginx/nginx.conf
/var/log/syslog

# 상대 경로 (현재 위치 기준)
./file.txt          # 현재 디렉토리의 file.txt
../parent/file.txt  # 상위 디렉토리의 parent/file.txt
docs/readme.md      # 현재 디렉토리의 docs/readme.md
```

#### 특수 디렉토리 기호
```bash
~                   # 홈 디렉토리 (/home/username)
.                   # 현재 디렉토리
..                  # 상위 디렉토리
-                   # 이전 디렉토리 (cd - 에서 사용)
```

---

## 7. 계정 관리 명령어

### adduser vs useradd

#### adduser (고수준 명령어)
```bash
# 기본 사용법
sudo adduser username

# 특징:
- 대화형 인터페이스
- 자동으로 홈 디렉토리 생성
- 기본 그룹 자동 생성
- 패스워드 설정 프롬프트
- 사용자 정보 입력 프롬프트
- 기본 쉘 자동 설정

# 실행 과정:
1. 사용자 계정 생성
2. 홈 디렉토리 생성 (/home/username)
3. 기본 파일들 복사 (/etc/skel 내용)
4. 기본 그룹 생성 (username 그룹)
5. 패스워드 설정 요청
6. 사용자 정보 입력 요청
```

#### useradd (저수준 명령어)
```bash
# 기본 사용법
sudo useradd username

# 옵션과 함께 사용:
sudo useradd -m -s /bin/bash -G sudo username
# -m: 홈 디렉토리 생성
# -s: 기본 쉘 지정
# -G: 추