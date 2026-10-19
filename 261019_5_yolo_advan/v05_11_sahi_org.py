from ultralytics import YOLO
import cv2
import os

# 1. 모델 로드
model = YOLO("yolo11n.pt")

# 2. 이미지 경로
input_image_path = "demo_data/small-vehicles1.jpeg"

# 3. 모델 예측
results = model(input_image_path)

# 4. 결과 시각화
annotated_frame = results[0].plot()

# 5. 결과 저장
os.makedirs("sahi", exist_ok=True)  # 폴더없으면 만들고 있으면 사용
output_image_path = "sahi/result_org.jpg"
cv2.imwrite(output_image_path,annotated_frame)

# 6. 탐지 개수 출력
detected = len(results[0].boxes)

print("===================")
print(f"기본 YOLO 추론 완료 : {output_image_path}")
print(f"탐지수 : {detected}")

