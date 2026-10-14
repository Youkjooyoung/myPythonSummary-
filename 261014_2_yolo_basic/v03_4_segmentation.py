from ultralytics import YOLO
import cv2

# 1. 모델로드
model = YOLO("yolo11n-seg.pt")
# 탐지(dept) = 물체 주변에 네모 박스만 생성
# 분할(seg) = 물체 모양 그대로 색칠(픽셀단위)

# 2. 모델 추론
model("261014_2_yolo_basic/pose_video.mp4",save = True)