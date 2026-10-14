from ultralytics import YOLO
import cv2

# 1. 모델 로드
# YOLO("모델명")
model = YOLO("yolo11n-cls.pt")
# n -> 5 -> m -> 1 -> x

# 2. 모델 추론
# results = model("261014_2_yolo_basic/penguins.jpg")
results = model("261014_2_yolo_basic/sandfox.jpg")

# 3. 결과 시각화
results_image = results[0].plot()

# 4. 결과 이미지 저장
# output_result_image_path = "저장할 경로/ 저장할 이미지 파일 이름.jpg"
output_result_image_path = "./output.jpg"
cv2.imwrite(output_result_image_path, results_image)
print(f"에측 결과 이미지가 잘 저장 되었습니다.{output_result_image_path}")