# Code Lounge DB Editor

👉 [실행 링크](http://3.39.127.75:5000)
<!-- 👉 [실행 링크](https://codeloungeeditor.pythonanywhere.com/) -->

## 도커 없이 실행방법
```bash
# 도커 없이 실행방법
nohup python3 flask_app.py > flask.log 2>&1 &

# 실행중인 프로스 확인
sudo lsof -i -P -n | grep :5000
```

## 도커 실행 방법
```bash
# 1. 이미지 빌드
docker build -t codelounge-server .

# 2. docker image로 이미지 확인 가능 
docker image

# 3. 컨테이너 실행 (포트 매핑)
```bash
docker run -p 5000:5000 --name codelounge-server-container codelounge-server # 포그라운드
docker run -d -p 5000:5000 --name codelounge-server-container codelounge-server # 백그라운드

# 3-1. 숨겨야 할 파일을 .env로 뻈을 때
docker run --env-file .env -d -p 5000:5000 --name codelounge-server-container codelounge-server # 백그라운드
```
<br/><br/><br/>

## 도커 파일 내보내기
# 1. Docker이미지 -> .tar 파일로 저장
```bash
docker save -o my-codelounge.tar codelounge-server
```

# 2. .tar 파일 -> Docker 이미지로 가져오기
```bash
docker load -i my-codelounge.tar
```

소스 + Dockerfile 공유
- 받은 사람이 직접 빌드해야 함 (docker build .)

이미지 .tar 공유
- 받은 사람이 바로 실행 가능 (docker load, docker run)
<br/><br/><br/>

## 도커 컨테이너 종료
# 1. 실행중인 컨테이너 확인
```bash
docker ps
# a1b2c3d4e5f6   codelounge-server      "python app.py" ...  codelounge-server-container
```

# 2. 컨테이너 이름 또는 ID로 종료
```bash
docker stop codelounge-server-container
docker stop a1b2c3d4e5f6
docker kill codelounge-server-container # 권장하지 않음
docker run -d --name codelounge-server-container -p 5000:5000 my-flask # 백그라운드 실행시 stop이나 kill로 종료해야함
```

## Portainer 세팅
```bash
# 1. Portainer 전용 볼륨 생성
docker volume create portainer_data

# 2. Portainer 실행 (9000 포트 열기)
docker run -d \
  -p 9000:9000 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce
```