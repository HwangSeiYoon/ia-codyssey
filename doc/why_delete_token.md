1-2. Personal Access Token을 텍스트 파일로 저장한 뒤 삭제해야 하는 이유
Token은 비밀번호와 같은 민감한 정보야. 텍스트 파일로 저장했다면 바로 삭제해야 하는 이유는 다음과 같아:

보안 위협: 텍스트 파일이 Git에 커밋되거나 백업되면 노출될 수 있음.

누군가 탈취하면 전체 권한 사용 가능: Token은 push, pull, issue 관리 등 권한이 있을 수 있어서 위험.

기본적으로 암호처럼 다뤄야 함: 토큰이 노출되면 즉시 revoke(무효화)하고 새로 발급받아야 함.

💡 Best Practice: 환경 변수, secret manager, .env 파일 (그리고 .gitignore로 제외)