from ultralytics import solutions
import cv2

# 1. 비디오 경로 설정
cap = cv2.VideoCapture("http://210.99.70.120:1935/live/cctv009.stream/playlist.m3u8")

# 2. 모델 로드 및 거리 계산 객체 생성
distance = solutions.DistanceCalculation(
    model = "yolo11n.pt",
    conf = 0.2,
    show = False          # 창 표시는 직접 처리
)

# 2-1. 창 생성 + 마우스 클릭 콜백 등록 (한 번만)
cv2.namedWindow("Distance")
cv2.setMouseCallback("Distance", distance.mouse_event_for_distance)

# 3. 프레임 처리 루프
while cap.isOpened():
    success, frame = cap.read()
    if not success:
            print("프레임 읽기 실패")
            break

    # 3-1. 탐지 + 클릭 대상 중심점 거리 계산(내부처리)
    results = distance.process(frame)
    cv2.imshow("Distance", results.plot_im)   # 결과 화면 직접 표시

     # 픽셀 거리 단위에 따른 상태 정의 (0 = 두 객체 미선택)
    d = results.pixels_distance
    if d > 0:
        state = "Danger" if d <= 100 else "Warning" if d <= 250 else "Safe"
        print(f"거리: {d:.1f}px → {state}")

    # 3-2. q 키로 종료
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        print("q 키를 눌러 종료")
        break

# 4. 자원 해제
cap.release()
cv2.destroyAllWindows()


##픽셀 거리 단위에 따른 상태 정의
