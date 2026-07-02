import threading
import webview
import os

# Runs the Flask server (autocar_server.main) in a background thread and opens pywebview window

def run_server():
    try:
        from pop import autocar_server
        autocar_server.main()
    except Exception as e:
        print('서버 실행 오류:', e)

if __name__ == '__main__':
    # start server thread
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    # open webview pointing to local server
    url = 'http://127.0.0.1:5000'
    webview.create_window('오토카 대시보드', url, width=1000, height=700)
    webview.start()
