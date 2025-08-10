# Dockerfiles

```bash
# 압축
tar czf vscode-server.tar.gz vscode-server/

# 다른 PC로 복사
scp vscode-server.tar.gz user@other-host:/home/user/

# 접속 후 압축 해제
tar xzf vscode-server.tar.gz
cd vscode-server/
```

# Dockerfile vs docker-compose 차이

## 1. Dockerfile

- **목적**: 컨테이너 이미지를 **빌드**하기 위한 레시피

- **형태**: 단일 파일 (`Dockerfile`)

- **내용 예시**:

    ```dockerfile
    FROM python:3.11
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install -r requirements.txt
    COPY . .
    CMD ["python", "app.py"]
    ```

- **사용 흐름**:

    1. `Dockerfile` 작성
    2. `docker build -t myimage .` → 이미지 생성
    3. `docker run myimage` → 컨테이너 실행

- **비유**: **레시피** → "이 재료와 조리법으로 음식(이미지)을 만들어라"

---

## 2. docker-compose

- **목적**: 여러 컨테이너를 **한 번에 실행·관리**

- **형태**: YAML 파일 (`docker-compose.yml`)

- **내용 예시**:

    ```yaml
    version: "3.8"
    services:
      web:
        build: .
        ports:
          - "8000:8000"
      db:
        image: mysql:8
        environment:
          MYSQL_ROOT_PASSWORD: root
    ```

- **사용 흐름**:

    1. `docker-compose.yml` 작성
    2. `docker-compose up -d` → 모든 서비스 실행
    3. `docker-compose down` → 모든 서비스 중지

- **비유**: **주방 운영 계획표** → "이 레시피로 만든 음식(A)은 이 테이블, 음식(B)은 저 테이블에 놓고 동시에 서빙해라"

---

## 3. 차이 요약

| 구분      | Dockerfile                     | docker-compose                    |
| --------- | ------------------------------ | --------------------------------- |
| 역할      | 이미지 빌드                    | 여러 컨테이너 실행·관리           |
| 포맷      | 명령어 기반 (`FROM`, `RUN` 등) | YAML 설정                         |
| 사용 시점 | 컨테이너 실행 전               | 컨테이너 실행 시                  |
| 실행 명령 | `docker build`, `docker run`   | `docker-compose up`               |
| 단일/다중 | 단일 컨테이너 기반             | 다중 컨테이너 오케스트레이션 가능 |

---

## 4. 함께 쓰는 경우

- **Dockerfile** → 애플리케이션 이미지를 만드는 방법 정의
- **docker-compose.yml** → 그 이미지를 포함한 여러 컨테이너를 한 번에 띄움

```yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
```