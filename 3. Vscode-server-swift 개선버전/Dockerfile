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

# ----- 기존 UID가 있으면 삭제 후 새로 생성 -----
RUN if id -u ${UID} >/dev/null 2>&1; then \
        OLD_USER=$(getent passwd ${UID} | cut -d: -f1) && \
        userdel -r "$OLD_USER"; \
    fi && \
    groupadd -g ${GID} ${USER} && \
    useradd -m -u ${UID} -g ${GID} ${USER} && \
    echo "${USER}:${PASSWORD}" | chpasswd && \
    adduser ${USER} sudo

# ----- code-server 설치 (root) -----
RUN curl -fsSL https://code-server.dev/install.sh | sh

# ----- 작업 디렉토리 생성 (root) -----
ENV WORKINGDIR="/home/${USER}/vscode"
RUN mkdir -p ${WORKINGDIR} && chown -R ${UID}:${GID} /home/${USER}

# ===============================
# Swiftly 설치 (사용자 권한)
# ===============================
USER ${USER}
WORKDIR /home/${USER}

RUN mkdir -p /home/${USER}/.local/share && \
    curl -O "https://download.swift.org/swiftly/linux/swiftly-$(uname -m).tar.gz" && \
    tar zxf "swiftly-$(uname -m).tar.gz" && \
    chmod +x swiftly && \
    ./swiftly init --quiet-shell-followup --assume-yes && \
    /home/${USER}/.local/share/swiftly/bin/swiftly install 6.1.0 --assume-yes --verify && \
    chmod -R +x /home/${USER}/.local/share/swiftly

# 환경변수 등록
RUN echo 'export SWIFTLY_HOME=/home/'${USER}'/.local/share/swiftly' >> /home/${USER}/.bashrc && \
    echo 'export PATH="$SWIFTLY_HOME/bin:$PATH"' >> /home/${USER}/.bashrc

# ===============================
# VSCode 확장 설치 (root)
# ===============================
USER root
RUN code-server --install-extension ms-python.python && \
    code-server --install-extension ms-azuretools.vscode-docker && \
    code-server --install-extension formulahendry.code-runner

# ----- 컨테이너 환경변수 -----
ENV PASSWORD=${PASSWORD}
ENV USER=${USER}

# ----- 실행 시 사용자 전환 -----
USER ${USER}
WORKDIR ${WORKINGDIR}

# ----- 포트 오픈 -----
EXPOSE 5002

# ----- code-server 실행 -----
CMD ["code-server", "--bind-addr", "0.0.0.0:5002", "--auth", "password", "."]

