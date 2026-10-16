import cv2
from ultralytics import solutions

# 1. 비디오 경로 설정
cap = cv2.VideoCapture("261016_4_yolo_advan/heatmap_video.mp4")

# 2. 모델 로드
heatmap = solutions.Heatmap(model="yolo11n.pt", show=False, colormap=cv2.COLORMAP_JET)

# 3. 프레임 처리
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("비디오 읽기 실패...")
        break

    # 3-1. 모델 추론
    results = heatmap(frame)

    # 3-2. 처리된 프레임 표시
    cv2.namedWindow("HEATMAP", cv2.WINDOW_NORMAL)
    cv2.imshow("HEATMAP", results.plot_im)

    # 3-3. q키를 눌러서 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("q 키 눌러 종료")
        break

# 4. 자원 해제
cap.release()
cv2.destroyAllWindows()
