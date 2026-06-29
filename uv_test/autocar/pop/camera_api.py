# /video 카메라 정보가 나오는것
# flask 로 서버를 열것
# cam = Util.gstrmer(width=640, height=480, fps=30, flip=0)
#cap = cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)

#for _ in range(120):
#    ret, frame = cap.read()
#    if not ret:
#        print(ret)
#        continue
#    cv2.imshow("frame", frame)
#cap.release()
# 위 코드를 기준으로 해서 작성
# jpg 압축 60% 해서 데이터 보내기
# 5000번 포트로 api 열기
# 쓰레드 사용


import cv2
import threading
import time
from flask import Flask, Response

# 사용자님의 카메라 설정 모듈 (같은 폴더에 Util.py가 있어야 합니다)
import Util

app = Flask(__name__)

# 스레드 간 데이터 공유를 위한 전역 변수
output_frame = None
lock = threading.Lock()

def capture_frames():
    """백그라운드 스레드에서 계속해서 카메라 프레임을 읽고 압축하는 함수"""
    global output_frame, lock
    
    # 1. 사용자님의 카메라 초기화 코드 적용
    cam = Util.gstrmer(width=640, height=480, fps=30, flip=0)
    cap = cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
            
        # 2. JPG 압축 60% 설정
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
        ret, buffer = cv2.imencode('.jpg', frame, encode_param)
        
        if ret:
            # 3. 안전하게 전역 변수에 압축된 이미지 데이터 업데이트
            with lock:
                output_frame = buffer.tobytes()

def generate_video():
    """클라이언트(웹 브라우저)에게 압축된 이미지를 연속으로 보내주는 제너레이터"""
    global output_frame, lock
    
    while True:
        with lock:
            if output_frame is None:
                continue
            frame_data = output_frame
            
        # 브라우저가 인식할 수 있는 실시간 스트리밍 포맷(MJPEG)으로 데이터 포장
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
        
        # CPU 과부하 방지를 위한 아주 짧은 대기 시간
        time.sleep(0.01)

# /video 주소로 접속하면 스트리밍 데이터 전송
@app.route('/video')
def video_feed():
    # multipart/x-mixed-replace 는 화면을 덮어씌우면서 영상을 재생하게 해주는 마법의 설정입니다.
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 편의를 위해 기본 주소(/)로 접속 시 영상을 볼 수 있는 웹 페이지 띄우기
@app.route('/')
def index():
    return '''
    <html>
        <head><title>AutoCar Camera</title></head>
        <body style="background-color:black; color:white; text-align:center;">
            <h1>🚗 AutoCar 실시간 카메라</h1>
            <img src="/video" style="border: 2px solid white; border-radius: 10px;">
        </body>
    </html>
    '''

if __name__ == '__main__':
    # Flask 서버를 켜기 전에 카메라 캡처 스레드를 먼저 시작 (데몬 스레드로 설정하여 메인 종료 시 함께 종료)
    t = threading.Thread(target=capture_frames, daemon=True)
    t.start()
    
    print("🚀 비디오 스트리밍 서버가 시작되었습니다! http://[소다IP]:5000 으로 접속하세요.")
    
    # 5000번 포트로 API 열기 (하드웨어 제어 시 debug=True를 켜면 카메라 충돌이 날 수 있어 False 유지 권장)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)