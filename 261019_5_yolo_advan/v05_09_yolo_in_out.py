from ultralytics import solutions
import cv2

# 1. 비디오 경로 설정
cap = cv2.VideoCapture("https://cctvsec.ktict.co.kr/6572/G4K8/J1Z+jkF45854aYp6TFbo32Tg3uQJ8BrrQbzOVGm7IzCHz1w48tVb/93yRyB")

# 2. 카운팅 선 설정 (2점 - 시작점 -> 끝점)
count_points = [
    [(67, 367),(360, 360)],     # 선 1
    [(80, 400),(500, 500)]      # 선 2
]

# 3. 모델 로드 및 카운터 객체 생성 (ObjectCounter는 선 1개만 받으므로 선마다 1개씩)
counter1 = solutions.ObjectCounter(
    model = "yolo11n.pt",   # YOLO 11 nono 모델 -> 속도우선
    show = False,           # 솔루션 내부 창 끔 (직접 imshow로 표시)
    region = count_points[0]   # 2점 리스트 -> 가상 선 (4점 주면 다각형 영역으로 카운트)
)
counter2 = solutions.ObjectCounter(
    model = "yolo11n.pt",   # YOLO 11 nono 모델 -> 속도우선
    show = False,           # 솔루션 내부 창 끔 (직접 imshow로 표시)
    region = count_points[1]   # 2점 리스트 -> 가상 선 (4점 주면 다각형 영역으로 카운트)
)

# 4. 프레임 처리
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("프레임 확인 바람")
        break
    
    # 4-1. 프레임 리사이즈 (선 좌표계와 일치 필수)
    re_frame = cv2.resize(frame,(640, 480))
    
    # 4-2. 탐지 + 트래킹 + 선 통고 판정 + IN/OUT 카운트(한 줄에서 모두처리)
    r1 = counter1(re_frame)         # 원본 프레임으로 선 1 카운트
    r2 = counter2(r1.plot_im)       # 선 1 결과 이미지 위에 선 2 카운트 덧그리기

    # 4-3. 처리된 프레임 표시
    cv2.imshow("IN/OUT COUNT", r2.plot_im)
    
    # 4-4. q 키로 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("q 키로 종료")
        break
    
# 5. 자원 해제
cap.release()
cv2.destroyAllWindows()     # imshow로 연 창 정리
