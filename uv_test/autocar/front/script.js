// 버튼들을 자바스크립트로 가져오기
const btnForward = document.getElementById('btn-forward');
const btnBackward = document.getElementById('btn-backward');
const btnLeft = document.getElementById('btn-left');
const btnRight = document.getElementById('btn-right');
const btnStop = document.getElementById('btn-stop');

// 파이썬 서버로 이동 명령을 보내는 함수
function sendCommand(command) {
    console.log("명령 전송:", command);
    
    // 파이썬 Flask 서버로 데이터 전송 (API 통신)
    fetch(`/api/control?action=${command}`)
        .then(response => response.json())
        .then(data => console.log("서버 응답:", data))
        .catch(error => console.error("통신 에러:", error));
}

// 각 버튼에 클릭 이벤트 연결
btnForward.addEventListener('click', () => sendCommand('forward'));
btnBackward.addEventListener('click', () => sendCommand('backward'));
btnLeft.addEventListener('click', () => sendCommand('left'));
btnRight.addEventListener('click', () => sendCommand('right'));
btnStop.addEventListener('click', () => sendCommand('stop'));

// 주기적으로(예: 3초마다) 배터리와 접속 상태를 파이썬에 물어보는 함수
function checkStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            // 파이썬에서 보내준 배터리 정보로 화면 업데이트
            document.getElementById('battery-status').innerText = `🔋 배터리: ${data.battery}%`;
        })
        .catch(error => {
            // 통신이 끊기면 빨간불로 변경
            document.getElementById('connection-status').innerHTML = '<span class="dot" style="background-color:red; box-shadow: 0 0 8px red;"></span> 연결 끊김';
        });
}

// 3초(3000ms)마다 상태 확인 함수 실행
setInterval(checkStatus, 3000);