"""
오토카 통합 제어 서버
- 비디오 스트리밍 (/video)
- 움직임 제어 (/api/control)
- 카메라 팬-틸트 제어 (/api/pantilt)
- 음성 출력 (/api/audio)
"""

import cv2
import threading
import time
import json
from flask import Flask, Response, request, jsonify
from threading import Lock
import subprocess
import os

# ============================================================
# 1. 모듈 로딩
# ============================================================
print("1. 라이브러리 로딩 중...")
try:
    import Util
    print("✅ Util 모듈 로딩 완료")
except Exception as e:
    print(f"❌ Util 로드 실패: {e}")

try:
    from CAN import OmniWheel
    print("✅ CAN(OmniWheel) 모듈 로딩 완료")
    omnwheel = None  # 나중에 초기화
except Exception as e:
    print(f"❌ CAN 로드 실패: {e}")
    omnwheel = None

# ============================================================
# 2. Flask 앱 초기화
# ============================================================
app = Flask(__name__)

# 스레드 간 영상 데이터 공유 (camera_api.py 방식)
output_frame = None
lock = Lock()
camera_thread = None
pan_angle = 90
tilt_angle = 90

# ============================================================
# 3. 카메라 캡처 함수 (background thread)
# ============================================================
def capture_frames():
    """백그라운드 스레드에서 카메라 프레임을 캡처"""
    global output_frame, lock
    
    try:
        # Util.gstrmer를 사용한 카메라 설정
        Util.__main__._camera_flip_method = 0
        cam = Util.gstrmer(width=640, height=480, fps=30, flip=0)
        cap = cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)
        
        if not cap.isOpened():
            print("❌ 카메라를 열 수 없습니다! GStreamer 또는 카메라 연결 확인")
            return
        
        print("✅ 카메라 캡처 시작")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ 프레임 읽기 실패")
                time.sleep(1)
                continue
            
            # JPG 60% 압축
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
            ret_encode, buffer = cv2.imencode('.jpg', frame, encode_param)
            
            if ret_encode:
                with lock:
                    output_frame = buffer.tobytes()
    
    except Exception as e:
        print(f"❌ 카메라 캡처 오류: {e}")
    finally:
        if 'cap' in locals():
            cap.release()

def generate_video():
    """MJPEG 비디오 스트림 생성"""
    global output_frame, lock
    
    while True:
        with lock:
            if output_frame is None:
                time.sleep(0.01)
                continue
            frame_data = output_frame
        
        # MJPEG 포맷으로 전송
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
        
        time.sleep(0.01)

# ============================================================
# 4. 움직임 제어 함수
# ============================================================
def control_motor(action, speed=100):
    """
    action: 'forward', 'backward', 'left', 'right', 'stop'
    speed: 0-255
    """
    global omnwheel
    
    if omnwheel is None:
        try:
            omnwheel = OmniWheel()
            print("✅ OmniWheel 초기화 완료")
        except Exception as e:
            print(f"❌ OmniWheel 초기화 실패: {e}")
            return False
    
    try:
        # OmniWheel의 3개 바퀴 제어
        # wheel(id, value): id=1,2,3 / value: 음수(역방향), 양수(정방향)
        
        if action == 'stop':
            omnwheel.wheel(1, 0)
            omnwheel.wheel(2, 0)
            omnwheel.wheel(3, 0)
        
        elif action == 'forward':
            omnwheel.wheel(1, speed)
            omnwheel.wheel(2, speed)
            omnwheel.wheel(3, speed)
        
        elif action == 'backward':
            omnwheel.wheel(1, -speed)
            omnwheel.wheel(2, -speed)
            omnwheel.wheel(3, -speed)
        
        elif action == 'left':
            # 좌회전: 1번 바퀴는 역방향, 나머지 정방향
            omnwheel.wheel(1, -speed)
            omnwheel.wheel(2, speed)
            omnwheel.wheel(3, speed)
        
        elif action == 'right':
            # 우회전: 1번 바퀴는 정방향, 나머지 역방향
            omnwheel.wheel(1, speed)
            omnwheel.wheel(2, -speed)
            omnwheel.wheel(3, -speed)
        
        return True
    
    except Exception as e:
        print(f"❌ 모터 제어 오류: {e}")
        return False

# ============================================================
# 5. 팬-틸트 제어 함수
# ============================================================
def control_pantilt(pan, tilt):
    """
    카메라 팬-틸트 서보 제어 (0-180도)
    TODO: 실제 서보 핀 설정 필요
    """
    global pan_angle, tilt_angle
    
    try:
        pan = max(0, min(180, int(pan)))
        tilt = max(0, min(180, int(tilt)))
        
        # GPIO를 사용한 서보 제어 (Jetson Nano 기준)
        # 예: GPIO 핀 설정 후 PWM으로 각도 제어
        # 지금은 상태만 업데이트
        
        pan_angle = pan
        tilt_angle = tilt
        print(f"📹 팬-틸트 설정: Pan={pan}, Tilt={tilt}")
        
        # 실제 서보 제어 코드 추가 필요
        # GPIO.setmode(GPIO.BCM)
        # servo_pan.ChangeDutyCycle(...) 등
        
        return True
    
    except Exception as e:
        print(f"❌ 팬-틸트 제어 오류: {e}")
        return False

# ============================================================
# 6. TTS 음성 출력 함수
# ============================================================
def speak_text(text):
    """
    텍스트를 음성으로 변환하여 재생
    선택지:
    1. piper-tts (빠름, 오프라인)
    2. gTTS (온라인, 느림)
    3. espeak (가장 가벼움)
    """
    try:
        # 방법 1: piper-tts 사용 (권장)
        if os.path.exists('/home/soda/pop/piper_tts_text.py'):
            print(f"🗣️ Piper TTS로 음성 출력: {text}")
            # subprocess 호출
            subprocess.run(['python3', '/home/soda/pop/piper_tts_text.py', text], 
                         timeout=10)
        
        # 방법 2: espeak 사용 (대체)
        elif os.path.exists('/usr/bin/espeak'):
            print(f"🗣️ espeak으로 음성 출력: {text}")
            subprocess.run(['espeak', '-v', 'ko', text])
        
        # 방법 3: gTTS 사용
        else:
            print(f"🗣️ gTTS로 음성 출력: {text}")
            from gtts import gTTS
            tts = gTTS(text=text, lang='ko', slow=False)
            tts.save('/tmp/tts_output.mp3')
            subprocess.run(['ffplay', '-nodisp', '-autoexit', '/tmp/tts_output.mp3'])
        
        return True
    
    except Exception as e:
        print(f"❌ TTS 오류: {e}")
        return False

# ============================================================
# 7. Flask 라우트
# ============================================================

@app.route('/video')
def video_feed():
    """비디오 스트리밍 엔드포인트"""
    return Response(generate_video(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/control', methods=['GET', 'POST'])
def api_control():
    """
    움직임 제어 API
    GET: /api/control?action=forward&speed=100
    POST: /api/control with JSON {"action": "forward", "speed": 100}
    """
    try:
        if request.method == 'POST':
            data = request.get_json()
            action = data.get('action', 'stop')
            speed = data.get('speed', 100)
        else:
            action = request.args.get('action', 'stop')
            speed = int(request.args.get('speed', 100))
        
        if action not in ['forward', 'backward', 'left', 'right', 'stop']:
            return jsonify({'error': '유효하지 않은 action'}), 400
        
        success = control_motor(action, speed)
        
        return jsonify({
            'success': success,
            'action': action,
            'speed': speed,
            'message': f"{'성공' if success else '실패'}: {action}"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pantilt', methods=['POST'])
def api_pantilt():
    """
    카메라 팬-틸트 제어 API
    POST: /api/pantilt with JSON {"pan": 90, "tilt": 90}
    """
    try:
        data = request.get_json()
        pan = data.get('pan', 90)
        tilt = data.get('tilt', 90)
        
        success = control_pantilt(pan, tilt)
        
        return jsonify({
            'success': success,
            'pan': pan,
            'tilt': tilt,
            'message': f"{'성공' if success else '실패'}: Pan={pan}, Tilt={tilt}"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio', methods=['POST'])
def api_audio():
    """
    음성 출력 API
    POST: /api/audio with JSON {"type": "tts", "text": "안녕하세요"}
    """
    try:
        data = request.get_json()
        audio_type = data.get('type', 'tts')
        text = data.get('text', '')
        
        if audio_type == 'tts' and text:
            success = speak_text(text)
            return jsonify({
                'success': success,
                'type': 'tts',
                'text': text,
                'message': f"{'성공' if success else '실패'}: {text}"
            })
        else:
            return jsonify({'error': '유효하지 않은 요청'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """서버 상태 조회"""
    return jsonify({
        'server': 'running',
        'camera': output_frame is not None,
        'pan': pan_angle,
        'tilt': tilt_angle,
        'motor': omnwheel is not None
    })

@app.route('/')
def index():
    """웹 대시보드 페이지"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>오토카 대시보드</title>
        <meta charset="utf-8">
    </head>
    <body style="font-family: sans-serif; margin: 20px;">
        <h1>🤖 오토카 제어 대시보드</h1>
        <p>UI는 /uv_test/autocar/pop/ui.html 에서 보세요</p>
        <ul>
            <li><a href="/video">📹 비디오 스트리밍</a></li>
            <li><a href="/api/status">📊 서버 상태</a></li>
        </ul>
        <p>API 엔드포인트:</p>
        <ul>
            <li>GET /api/control?action=forward&speed=100</li>
            <li>POST /api/pantilt - {"pan": 90, "tilt": 90}</li>
            <li>POST /api/audio - {"type": "tts", "text": "안녕하세요"}</li>
        </ul>
    </body>
    </html>
    '''

# ============================================================
# 8. 메인 실행
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 오토카 통합 제어 서버 시작")
    print("=" * 60)
    
    # 백그라운드 카메라 스레드 시작
    camera_thread = threading.Thread(target=capture_frames, daemon=True)
    camera_thread.start()
    print("📹 카메라 스레드 시작")
    
    # Flask 서버 실행
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n⚠️ 서버 종료")
    except Exception as e:
        print(f"❌ 서버 오류: {e}")
