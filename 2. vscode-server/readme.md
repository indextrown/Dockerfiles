# 🛠️ VSCode Server (Ubuntu + Docker Compose + Volume + .env)

## ✅ 구성 목적

- Ubuntu 기반의 code-server(VSCode 웹버전) 실행
- Python, Java 개발환경 포함
- 사용자명과 비밀번호는 `.env`에서 관리
- 코드 파일은 로컬 `./dev` 폴더에 저장됨
- `docker compose`로 한 줄 실행 및 자동 재시작

---

## 📁 디렉토리 구조

```
vscode-server/
├── Dockerfile
├── docker-compose.yml
├── .env
└── dev/                # ← 여기에 작성한 코드가 저장됨
```

---

## 📝 .env

```env
USER=myuser
PASSWORD=mysecurepassword
```

> ⚠️ `.gitignore`에 `.env`를 꼭 추가하세요.

---

## 🐳 Dockerfile

```Dockerfile
FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y \
        curl sudo python3 python3-pip default-jdk \
        git wget nano locales && \
    apt-get clean

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

ARG USER
ARG PASSWORD

RUN useradd -m ${USER} && echo "${USER}:${PASSWORD}" | chpasswd && adduser ${USER} sudo

ENV WORKINGDIR="/home/${USER}/vscode"
RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    mkdir -p ${WORKINGDIR} && chown -R ${USER}:${USER} ${WORKINGDIR}

ENV USER=${USER}
ENV PASSWORD=${PASSWORD}

USER ${USER}
WORKDIR ${WORKINGDIR}

RUN code-server --install-extension ms-python.python && \
    code-server --install-extension ms-azuretools.vscode-docker

EXPOSE 8080

CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "password", "."]
```

---

## ⚙️ docker-compose.yml

```yaml
version: "3.8"

services:
  vscode:
    build:
      context: .
      args:
        USER: ${USER}
        PASSWORD: ${PASSWORD}
    container_name: vscode-container
    ports:
      - "8080:8080"
    volumes:
      - ./dev:/home/${USER}/vscode
    environment:
      - PASSWORD=${PASSWORD}
    restart: always
```

---

## 🚀 실행 순서

1. 디렉토리 구성

```bash
mkdir vscode-server && cd vscode-server
mkdir dev
touch Dockerfile docker-compose.yml .env
```

2. `.env` 파일에 사용자 정보 입력

```env
USER=myuser
PASSWORD=mysecurepassword
```

3. 빌드 및 실행

```bash
docker compose up -d --build
```

4. 접속

```
http://localhost:8080
```

- 비밀번호: `.env`의 `PASSWORD`
- 작성한 파일은 `./dev/` 폴더에 저장됨

---

## 🔁 중지 및 재실행

| 동작             | 명령어                         |
| ---------------- | ------------------------------ |
| 중지 (완전 정리) | `docker compose down`          |
| 재실행           | `docker compose up -d`         |
| 수정 반영 재빌드 | `docker compose up -d --build` |
| 일시정지         | `docker compose stop`          |
| 다시시작         | `docker compose start`         |
| 로그 확인        | `docker compose logs -f`       |

---

## ✅ 요약

- 안전한 환경 분리: `.env`로 민감 정보 관리
- 코드 영속성: `./dev` 폴더로 안전하게 저장
- 간편 실행/정지: `docker compose` 명령어로 관리

## 🧪 권한 문제 해결

호스트에서:

```bash
sudo chown -R 1000:1000 ./dev
```

또는 컨테이너 안에서:

```bash
docker exec -u root -it vscode-container bash
chown -R ec2-user:ec2-user /home/ec2-user/vscode
exit
```

---

## 🧪 파일 저장 오류 발생 시 해결 방법

### 오류 메시지 예시

```
Unable to write file 'vscode-remote://<...>' (NoPermissions (FileSystemError): Error: EACCES: permission denied, open ...)
```

### 🔧 해결 1: 로컬 dev 폴더 권한 변경 (호스트에서)

```bash
sudo chown -R ec2-user:ec2-user ./dev
```

### 🔧 해결 2: 컨테이너 내부 vscode 폴더 권한 변경 (루트로 진입)

```bash
docker exec -u root -it vscode-container bash
chown -R ec2-user:ec2-user /home/ec2-user/vscode
exit
```

이 두 작업을 수행하면 VSCode 웹에서 파일을 저장할 수 있습니다.

✅ 1. 컨테이너 터미널로 진입
아래 명령어를 EC2에서 실행하세요:
```bash
docker exec -it vscode-container bash
```
→ 프롬프트가 이렇게 바뀌면 성공입니다:
```bash
ec2-user@xxxxxxxx:/home/ec2-user/vscode$
```

✅ 2. 설정 파일 디렉토리로 이동
```bash
cd /home/ec2-user/.local/share/code-server/User
```
📌 폴더가 없으면 먼저 만들어야 합니다:
```bash
mkdir -p /home/ec2-user/.local/share/code-server/User
cd /home/ec2-user/.local/share/code-server/User
```
✅ 3. settings.json 파일 생성 또는 수정
```bash
nano settings.json
그리고 아래 내용 입력 (기존 내용 있으면 병합):
{
  "code-runner.executorMap": {
    "python": "python3 -u"
  },
  "code-runner.showExecutionMessage": false,
  "code-runner.clearPreviousOutput": true
}

저장 및 종료:
Ctrl + O → Enter (저장)
Ctrl + X (나가기)
```
## 도커 캐시 삭제
```bash
docker system prune -af
```

# Swift추가 방법

```bash
docker exec -it vscode-container bash
```

```bash
# 1. 기존 swiftly 완전 삭제
rm -rf ~/.local/share/swiftly
rm -f ~/swiftly

# 2. 필수 패키지 설치
sudo apt-get update
sudo apt-get install -y clang libicu-dev wget libpython3-dev

# 3. 최신 swiftly 설치
curl -O "https://download.swift.org/swiftly/linux/swiftly-$(uname -m).tar.gz"
tar zxf "swiftly-$(uname -m).tar.gz"
chmod +x swiftly
./swiftly init --quiet-shell-followup --assume-yes

# 4. 환경 변수 적용
source ~/.local/share/swiftly/env.sh
echo 'source ~/.local/share/swiftly/env.sh' >> ~/.bashrc

# 5. Swift 6.1.0 설치 (실제 toolchain 다운로드)
~/.local/share/swiftly/bin/swiftly install 6.1.0 --assume-yes --verify

# 6. swift 실행 확인
find ~/.local/share/swiftly/toolchains -name swift -type f -executable
swift --version
```

```bash
# 권한문제 해결
sudo chown -R ec2-user:ec2-user /home/ec2-user

cd /home/ec2-user/.local/share/code-server/User

nano settings.json
그리고 아래 내용 입력 (기존 내용 있으면 병합):
{
  "code-runner.executorMap": {
    "python": "python3 -u",
    "swift": "/home/ec2-user/.local/share/swiftly/bin/swift"
  },
  "code-runner.showExecutionMessage": false,
  "code-runner.clearPreviousOutput": true
}

```



<!--  -->
<!-- FROM ubuntu:latest

# ----- 기본 패키지 설치 -----
RUN apt-get update && \
    apt-get install -y \
        curl sudo python3 python3-pip default-jdk \
        git wget nano locales && \
    apt-get clean

# ----- 로케일 설정 -----
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# ----- ARG로 외부에서 변수 받기 -----
ARG USER
ARG PASSWORD

# ----- 사용자 생성 및 sudo 권한 부여 -----
RUN useradd -m ${USER} && echo "${USER}:${PASSWORD}" | chpasswd && adduser ${USER} sudo

# ----- 작업 디렉토리 및 code-server 설치 -----
ENV WORKINGDIR="/home/${USER}/vscode"
RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    mkdir -p ${WORKINGDIR} && chown -R ${USER}:${USER} ${WORKINGDIR}

# ----- 컨테이너 환경변수로도 유지 -----
ENV PASSWORD=${PASSWORD}
ENV USER=${USER}

# ----- 사용자 전환 -----
USER ${USER}
WORKDIR ${WORKINGDIR}

# ----- 확장 설치 -----
RUN code-server --install-extension ms-python.python && \
    code-server --install-extension ms-azuretools.vscode-docker

# ----- 포트 오픈 -----
EXPOSE 8080

# ----- 실행 명령 -----
CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "password", "."] -->










<!--  -->


<!-- # 🛠️ VSCode Server - Ubuntu 기반 개발환경 구성 (Docker Compose + Volume)

## ✅ 목표

- Ubuntu 기반 VS Code Server 웹 환경 구축
- Python, Java 개발 가능
- 코드 파일은 로컬(dev 폴더)에 저장
- 컨테이너 중단/재시작해도 코드 유지
- `docker-compose`로 한 줄 실행 관리

---

## 📁 디렉토리 구조

```
vscode-server/
├── Dockerfile
├── docker-compose.yml
└── dev/                 # ← 작성한 코드가 저장되는 폴더
```

---

## 📝 Dockerfile

```Dockerfile
FROM ubuntu:latest

# 기본 패키지 설치
RUN apt-get update && \
    apt-get install -y \
        curl \
        sudo \
        python3 \
        python3-pip \
        default-jdk \
        git \
        wget \
        nano \
        locales \
    && apt-get clean

# 로케일 설정
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# 사용자 생성 및 비밀번호 설정
ENV USER="user" \
    PASSWORD="password"
RUN useradd -m ${USER} && echo "${USER}:${PASSWORD}" | chpasswd && adduser ${USER} sudo

# code-server 설치 및 작업 디렉토리 설정
ENV WORKINGDIR="/home/${USER}/vscode"
RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    mkdir -p ${WORKINGDIR} && chown -R ${USER}:${USER} ${WORKINGDIR}

# 사용자 전환 및 작업 경로 설정
USER ${USER}
WORKDIR ${WORKINGDIR}

# 확장 설치
RUN code-server --install-extension ms-python.python && \
    code-server --install-extension ms-azuretools.vscode-docker

# 포트 오픈
EXPOSE 8080

# code-server 실행
CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "password", "."]
```

---

## ⚙️ docker-compose.yml

```yaml
version: "3.8"

services:
  vscode:
    build: .
    container_name: vscode-container
    ports:
      - "8080:8080"
    volumes:
      - ./dev:/home/user/vscode
    environment:
      - PASSWORD=password
    restart: always
```

---

## 🚀 실행 방법

1. 프로젝트 폴더 생성

```bash
mkdir vscode-server && cd vscode-server
mkdir dev
touch Dockerfile docker-compose.yml
```

2. 위 내용을 `Dockerfile`, `docker-compose.yml`에 각각 붙여넣기

3. 빌드 및 실행

```bash
docker compose up -d
```

4. 브라우저 접속

```
http://localhost:8080
```

🔑 비밀번호: `password`

---

## 🛠️ 주요 명령어

| 동작        | 명령어                         |
| ----------- | ------------------------------ |
| 실행        | `docker compose up -d`         |
| 중지        | `docker compose down`          |
| 로그 확인   | `docker compose logs -f`       |
| 재시작      | `docker compose restart`       |
| 강제 재빌드 | `docker compose up -d --build` |

---

## 📦 볼륨 설명

- `./dev` 폴더에 코드 저장됨 (로컬)
- 컨테이너 안의 `/home/user/vscode`와 연결
- 컨테이너 삭제해도 `dev` 폴더는 그대로 유지됨

---

## ✅ 결과

- 브라우저에서 VSCode 사용 가능
- 코드, 설정 파일은 `./dev`에 저장
- Python, Java 개발 환경 준비 완료
- VSCode 확장도 미리 설치되어 있음

---

## 💡 필요시 확장

- `node.js`, `zsh`, `conda` 추가
- 도메인 연결 + HTTPS 설정
- Git 연동, SSH 키 연동 -->