import webview
from flask import Flask, request, jsonify

# Flask 설정 (front 폴더 연결)
app = Flask(__name__, static_folder='front', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('text.html')

# 조종 명령을 받는 주소
@app.route('/api/control')
def control_car():
    action = request.args.get('action')
    print(f"🚗 자동차 명령 수신: {action}")
    return jsonify({"status": "success", "command_received": action})

# 배터리 상태를 알려주는 주소
@app.route('/api/status')
def get_status():
    current_battery = 85 
    return jsonify({"battery": current_battery})

if __name__ == '__main__':
    # Flask 앱을 pywebview를 사용해 데스크톱 창으로 띄우기! (이 부분이 핵심입니다)
    window = webview.create_window('AutoCar 리모컨', app, width=400, height=600)
    
    # 프로그램 실행
    webview.start()