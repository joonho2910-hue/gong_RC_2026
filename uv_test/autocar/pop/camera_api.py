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

# 사용자님의 카메라 설정 모듈
print("1. 라이브러리 로딩 완료!") # <--- 추가

import Util
print("2. Util 모듈 로딩 완료!")  # <--- 추가

app = Flask(__name__)

# 스레드 간 영상 데이터를 안전하게 공유하기 위한 변수
output_frame = None
lock = threading.Lock()

def capture_frames():
    """백그라운드 스레드에서 카메라 프레임을 읽고 60%로 압축하는 함수"""
    global output_frame, lock
    
    # 1. 카메라 초기화 (주신 코드 기준)
    cam = Util.gstrmer(width=640, height=480, fps=30, flip=0)
    cap = cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)
    
    if not cap.isOpened():
        print("❌ 에러: 카메라를 찾을 수 없거나 열 수 없습니다! 물리적 선 연결을 확인하세요.")
        return

    print("✅ 카메라 캡처가 정상적으로 시작되었습니다.")

    while True:
        ret, frame = cap.read()
        
        # 2. 터미널 폭주 방지 (프레임을 못 읽었을 때)
        if not ret:
            print("⚠️ 프레임 읽기 실패. 카메라 상태 확인 중...")
            time.sleep(1)  # 1초 대기하여 터미널이 점(.)으로 도배되는 것을 막습니다.
            continue
            
        # 3. JPG 압축 60% 설정
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
        ret_encode, buffer = cv2.imencode('.jpg', frame, encode_param)
        
        # 4. 압축 성공 시 전역 변수에 저장 (스레드 충돌 방지를 위해 lock 사용)
        if ret_encode:
            with lock:
                output_frame = buffer.tobytes()

def generate_video():
    """웹 브라우저로 압축된 프레임을 쏴주는 제너레이터 함수"""
    global output_frame, lock
    
    while True:
        with lock:
            if output_frame is None:
                continue
            frame_data = output_frame
            
        # MJPEG 스트리밍 포맷으로 데이터 전송
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
        
        # CPU 과부하 방지
        time.sleep(0.01)

# 5. /video 주소로 접속하면 스트리밍 시작
@app.route('/video')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # 6. Flask 서버를 켜기 전에 백그라운드에서 카메라 스레드 먼저 실행
    t = threading.Thread(target=capture_frames, daemon=True)
    t.start()
    
    print("=========================================================")
    print("🚀 스트리밍 서버 시작! 웹 브라우저에서 아래 주소로 접속하세요:")
    print("👉 http://[RC카의_IP주소]:5000/video")
    print("=========================================================")
    
    # 7. 5000번 포트로 서버 열기
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)