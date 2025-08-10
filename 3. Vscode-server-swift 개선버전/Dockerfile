FROM ubuntu:latest

# ----- 기본 패키지 설치 -----
RUN apt-get update && \
    apt-get install -y \
        curl sudo python3 python3-pip default-jdk \
        git wget nano locales \
        libpython3.10 libicu-dev libxml2-dev clang \
        unzip gnupg2 libcurl4-openssl-dev pkg-config \
    && apt-get clean

# ----- 로케일 설정 -----
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# ----- ARG -----
ARG USER
ARG PASSWORD
ARG UID=1000
ARG GID=1000

# ----- 사용자 생성 (root로) -----
RUN useradd -m ${USER} && echo "${USER}:${PASSWORD}" | chpasswd && adduser ${USER} sudo

# ----- code-server 설치 (root) -----
RUN curl -fsSL https://code-server.dev/install.sh | sh

# ----- 작업 디렉토리 생성 (root) -----
ENV WORKINGDIR="/home/${USER}/vscode"
RUN mkdir -p ${WORKINGDIR} && chown -R ${UID}:${GID} /home/${USER}

# ----- VSCode 확장 설치 (root) -----
RUN code-server --install-extension ms-python.python && \
    code-server --install-extension ms-azuretools.vscode-docker && \
    code-server --install-extension formulahendry.code-runner

# ----- 컨테이너 환경변수 -----
ENV PASSWORD=${PASSWORD}
ENV USER=${USER}

# ----- 실행 시 사용자 전환은 docker-compose에서 -----
WORKDIR ${WORKINGDIR}

# ----- 포트 오픈 -----
EXPOSE 5002

# ----- code-server 실행 -----
CMD ["code-server", "--bind-addr", "0.0.0.0:5002", "--auth", "password", "."]


# 권한 문제 발생시 아래 커맨드 입력
# sudo chown -R $(id -u):$(id -g) ./dev

