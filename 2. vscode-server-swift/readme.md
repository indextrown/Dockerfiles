---
title: "[Docker] code-server"
tags: 
- UIKit
- UIComponent
header: 
  teaser: 
typora-root-url: ../

---

# 🐳 code-server 개발 환경 구성 (Swift 제외)

Ubuntu 기반 컨테이너에 `code-server`를 설치하여 브라우저에서 Visual Studio Code 환경을 사용합니다.  
Swift를 제외한 Python, Java, Docker 등 일반적인 개발에 최적화된 구성입니다.

---

## DockerCompose 실행
```bash
# 빌드 & 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 컨테이너 중지 및 삭제
docker-compose down

# 볼륨·네트워크·이미지까지 삭제
docker-compose down --rmi all --volumes --remove-orphans
```

## 📁 Dockerfile 요약

```dockerfile
FROM ubuntu:latest

# 기본 패키지 설치
RUN apt-get update && \
    apt-get install -y \
        curl sudo python3 python3-pip default-jdk \
        git wget nano locales \
        libpython3.10 libicu-dev libxml2-dev clang \
        unzip gnupg2 libcurl4-openssl-dev pkg-config && \
    apt-get clean

# 로케일 설정
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# 사용자 생성 및 sudo 권한 부여
ARG USER
ARG PASSWORD
RUN useradd -m ${USER} && echo "${USER}:${PASSWORD}" | chpasswd && adduser ${USER} sudo

# code-server 설치 및 작업 디렉토리 생성
ENV WORKINGDIR="/home/${USER}/vscode"
RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    mkdir -p ${WORKINGDIR} && chown -R ${USER}:${USER} ${WORKINGDIR}

# 환경 변수 유지
ENV PASSWORD=${PASSWORD}
ENV USER=${USER}

# 사용자 전환 및 작업 디렉토리 이동
USER ${USER}
WORKDIR ${WORKINGDIR}

# VSCode 확장 설치
RUN code-server --install-extension ms-python.python && \
    code-server --install-extension ms-azuretools.vscode-docker && \
    code-server --install-extension formulahendry.code-runner

# 포트 오픈 및 실행
EXPOSE 8080
CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "password", "."]
```

---

## 🛠 실행 후 설정 (Python 기준)

### 컨테이너 진입 및 설정

```bash
docker exec -it vscode-container bash
cd /home/ec2-user/.local/share/code-server/User
nano settings.json
```

```json
{
  "code-runner.executorMap": {
    "python": "python3 -u"
  },
  "code-runner.showExecutionMessage": false,
  "code-runner.clearPreviousOutput": true
}
```

저장: `Ctrl + O`, `Enter`, 종료: `Ctrl + X`

### 재빌드

```bash
exit
docker compose up -d --build
```

---

## 🧪 Swift 추가 방법 (옵션)

필요 시 Swift 설치는 아래 절차로 진행하세요.

```bash
# 1. 컨테이너 진입
docker exec -it vscode-container bash

# 2. 기존 Swiftly 삭제
rm -rf ~/.local/share/swiftly
rm -f ~/swiftly

# 3. 필수 패키지 설치
sudo apt-get update
sudo apt-get install -y clang libicu-dev wget libpython3-dev

# 4. Swiftly 다운로드 및 설치
curl -O "https://download.swift.org/swiftly/linux/swiftly-$(uname -m).tar.gz"
tar zxf "swiftly-$(uname -m).tar.gz"
chmod +x swiftly
./swiftly init --quiet-shell-followup --assume-yes

# 5. 환경변수 등록
source ~/.local/share/swiftly/env.sh
echo 'source ~/.local/share/swiftly/env.sh' >> ~/.bashrc

# 6. Swift 6.1.0 설치
~/.local/share/swiftly/bin/swiftly install 6.1.0 --assume-yes --verify

# 7. 설치 확인
swift --version
```

---

✅ Python, Java, Docker 개발은 기본 지원  
🌀 Swift는 옵션으로, 사용 시 별도 설치  
💻 `code-server`로 어디서든 웹에서 개발