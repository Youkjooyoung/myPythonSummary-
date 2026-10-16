import cv2
from ultralytics import solutions

# 1. 비디오/스트림 경로 설정(RTSP, 파일 ,웹캠 확인가능)
stream_url = "http://210.99.70.120:1935/live/cctv009.stream/playlist.m3u8"
cap = cv2.VideoCapture(stream_url)
assert cap.isOpened(), "스트림 열기 실패 - 경로 / 네트워크 확인"

# 2. 이메일 정보 설정
from_email = "yjy6234000@gmail.com"
password = "pvoz iene yszq ocup"
to_email = "yjy6234000@gmail.com"


# 3. 모델 로드(알람 객체 생성)
google_alarm = solutions.SecurityAlarm(
    model="yolo11n.pt",
    show=False,
    records=2,  # 2개 이상 탐지되면 메일 1회 전송
    classes=[2],
)


# 이메일 문구 변경
from email.mime.image import MIMEImage  #   사진 첨부용
from email.mime.multipart import MIMEMultipart  # 글 + 사진을 담는 봉투
from email.mime.text import MIMEText


def my_sendmail(im0, records=5):
    msg = MIMEMultipart()
    msg["From"], msg["To"], msg["Subject"] = from_email, to_email, "SecurityAlert"
    msg.attach(MIMEText("현재 경고이므로 주의해주세요", "plain", "utf-8"))  # 글 넣기
    msg.attach(MIMEImage(cv2.imencode(".jpg", im0)[1].tobytes(), name="alert.jpg"))
    google_alarm.server.send_message(msg)


google_alarm.send_email = my_sendmail


# 4. SMTP 서버 인증
google_alarm.authenticate(from_email, password, to_email)

# 5. 비디오 프레임 처리
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("스트림 읽기 실패")
        break

    # 탐지 -> 추적 -> 임계치 도달 시 메일 발송
    results = google_alarm(frame)

    # 처리된 프레임 표시 (show = False -> 우리가 직접  창을 띄움)
    cv2.imshow("SECURITY ALARM", results.plot_im)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("q 키를 눌러 종료")
        break

# 6. 자원 해제
cap.release()
cv2.destroyAllWindows()


# 메일 알림올때 문구를 수정 ==>"현재 경고이므로 주의해주세요"
