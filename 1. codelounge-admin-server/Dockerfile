# 베이스 이미지 선택
FROM python:3.10-slim

# 작업 디렉토리 생성
WORKDIR /app

# 종속성 파일 복사 후 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 전체 프로젝트 복사
COPY . .

# 앱 실행
CMD ["python", "flask_app.py"]
