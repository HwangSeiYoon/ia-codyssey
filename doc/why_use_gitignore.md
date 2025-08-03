✅ 문제 3: 파이썬 프로젝트에서 .gitignore 사용 이유
3-1. __pycache__와 .venv 생성 이유
__pycache__: Python이 코드를 빠르게 실행하기 위해 컴파일한 .pyc 파일을 저장하는 디렉토리.

.venv: 프로젝트마다 독립적인 가상환경을 만들기 위한 디렉토리 (패키지 의존성 관리)

➡️ 공통점: 프로젝트 실행/개발 중 자동 생성되며, Git 저장소에 필요 없음.

3-2. GitHub의 Python .gitignore 템플릿에 포함된 항목
GitHub의 Python용 .gitignore 템플릿에는 다음과 같은 항목이 포함됨:

__pycache__/

*.py[cod]

.env

.venv

env/

*.egg-info/

dist/

build/

3-3. Flask 프로젝트에서 .gitignore에 추가할 항목

# Python 기본
__pycache__/
*.py[cod]
*.egg-info/
*.log

# 가상환경
.venv/
env/
venv/

# 환경 설정
.env
config.py

# 테스트 관련
coverage.xml
htmlcov/

# 빌드 산출물
build/
dist/

# IDE
.vscode/
.idea/
