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

# ----- ARG로 외부에서 변수 받기 -----
ARG USER
ARG PASSWORD

# ----- 사용자 생성 및 sudo 권한 부여 -----
RUN useradd -m ${USER} && echo "${USER}:${PASSWORD}" | chpasswd && adduser ${USER} sudo

# ----- Swiftly 및 Swift 설치 -----
RUN curl -O "https://download.swift.org/swiftly/linux/swiftly-$(uname -m).tar.gz" && \
    tar zxf "swiftly-$(uname -m).tar.gz" && \
    ~/.local/share/swiftly/bin/swiftly init --quiet-shell-followup && \
    cp ~/.local/share/swiftly/bin/swiftly /usr/local/bin/swiftly && \
    rm swiftly-$(uname -m).tar.gz

# ----- Swift PATH 설정 -----
ENV PATH="${PATH}:${HOME}/.local/share/swiftly/toolchains/swift-6.1.0/usr/bin"

# ----- code-server 설치 및 작업 디렉토리 생성 -----
ENV WORKINGDIR="/home/${USER}/vscode"
RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    mkdir -p ${WORKINGDIR} && chown -R ${USER}:${USER} ${WORKINGDIR}

# ----- 컨테이너 환경변수로도 유지 -----
ENV PASSWORD=${PASSWORD}
ENV USER=${USER}

# ----- 사용자 전환 -----
USER ${USER}
WORKDIR ${WORKINGDIR}

# ----- VSCode 확장 설치 -----
RUN code-server --install-extension ms-python.python && \
    code-server --install-extension ms-azuretools.vscode-docker && \
    code-server --install-extension formulahendry.code-runner

# ----- 포트 오픈 -----
EXPOSE 8080

# ----- code-server 실행 -----
CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "password", "."]



# FROM ubuntu:latest

# # ----- 기본 패키지 설치 -----
# RUN apt-get update && \
#     apt-get install -y \
#         curl sudo python3 python3-pip default-jdk \
#         git wget nano locales && \
#     apt-get clean

# # ----- 로케일 설정 -----
# RUN locale-gen en_US.UTF-8
# ENV LANG=en_US.UTF-8
# ENV LANGUAGE=en_US:en
# ENV LC_ALL=en_US.UTF-8

# # ----- ARG로 외부에서 변수 받기 -----
# ARG USER
# ARG PASSWORD

# # ----- 사용자 생성 및 sudo 권한 부여 -----
# RUN useradd -m ${USER} && echo "${USER}:${PASSWORD}" | chpasswd && adduser ${USER} sudo

# # ----- 작업 디렉토리 및 code-server 설치 -----
# ENV WORKINGDIR="/home/${USER}/vscode"
# RUN curl -fsSL https://code-server.dev/install.sh | sh && \
#     mkdir -p ${WORKINGDIR} && chown -R ${USER}:${USER} ${WORKINGDIR}

# # ----- 컨테이너 환경변수로도 유지 -----
# ENV PASSWORD=${PASSWORD}
# ENV USER=${USER}

# # ----- 사용자 전환 -----
# USER ${USER}
# WORKDIR ${WORKINGDIR}

# # ----- 확장 설치 -----
# RUN code-server --install-extension ms-python.python && \
#     code-server --install-extension ms-azuretools.vscode-docker

# # ----- 포트 오픈 -----
# EXPOSE 8080

# # ----- 실행 명령 -----
# CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "password", "."]
