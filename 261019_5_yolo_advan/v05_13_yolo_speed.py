import cv2
from ultralytics import solutions

# 1. 비디오 경로 설정
cap = cv2.VideoCapture("https://cctvsec.ktict.co.kr/6568/VALd7fN0yXqIzLwgqYAnHHB9nJfWC9IdjNjNn2rcOW0/W2zvd/wPH0iHkArEP0mr")

# 2. 속도 추정 객체 생성 및 모델 로드
yolo_speed = solutions.SpeedEstimator(
    model = "yolo11n.pt",
    show = False,
    max_speed = 120,
    meter_per_pixel = 0.1,
    classes = [2],
    line_width = 2
)

# 3. 프레임 처리 루프
while cap.isOpened():
    success , frame= cap.read()
    if not success:
        print("프레임 확인")
        break
    
    # 3-1. 속도 계산 및 추적 수행 ->SolutionResults 반환
    results = yolo_speed(frame)
    
    # 3-2. 처리된 프레임 표시
    cv2.imshow("SPEED", results.plot_im)
    
    # 3-3. q키 입력시 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Q 키 눌러서 종료")
        break
    
# 4. 자원 해제
cap.release()
