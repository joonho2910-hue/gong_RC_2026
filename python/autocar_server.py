from flask import Flask, request, jsonify, render_template
import threading
from gtts import gTTS
import os
import Util  # 사용 중인 제어 라이브러리

app = Flask(__name__, template_folder='templates')

# [메인 페이지] 대시보드 로딩
@app.route('/')
def index():
    return render_template('dashboard.html')

# [기능 1] 조이스틱 모터 제어
@app.route('/api/control', methods=['GET'])
def control_manual():
    action = request.args.get('action')
    print(f"🎮 명령 수신: {action}")
    
    if action == 'forward': Util.forward()
    elif action == 'backward': Util.backward()
    elif action == 'left': Util.left()
    elif action == 'right': Util.right()
    elif action == 'stop': Util.stop()
    
    return jsonify({"status": "success", "action": action})

# [기능 2] 카메라 팬/틸트 제어
@app.route('/api/pantilt', methods=['POST'])
def control_pantilt():
    data = request.json
    pan = data.get('pan')
    tilt = data.get('tilt')
    print(f"📷 카메라 조절 - Pan: {pan}, Tilt: {tilt}")
    
    # Util의 카메라 제어 함수 호출 (Util에 해당 함수가 있다는 가정)
    Util.set_pan_tilt(pan, tilt)
    return jsonify({"status": "success"})

# [기능 3] 오디오 및 TTS 제어
@app.route('/api/audio', methods=['POST'])
def control_audio():
    data = request.json
    audio_type = data.get('type')
    
    if audio_type == 'tts':
        text = data.get('text', '안내 음성입니다.')
        print(f"🗣️ TTS 재생: {text}")
        
        def run_tts(msg):
            tts = gTTS(text=msg, lang='ko')
            tts.save("tts_output.mp3")
            os.system("mpg321 tts_output.mp3")
            
        threading.Thread(target=run_tts, args=(text,)).start()
        
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # 0.0.0.0으로 설정해야 외부(대시보드)에서 접속 가능합니다.
    app.run(host='0.0.0.0', port=5000, debug=True)