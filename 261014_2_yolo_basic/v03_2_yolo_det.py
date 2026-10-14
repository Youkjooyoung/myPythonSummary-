from ultralytics import YOLO
import cv2

# 1. 모델 로드 
model = YOLO("261014_2_yolo_basic/yolo11n.pt")

# 2. 모델 추론
results = model("261014_2_yolo_basic/yolo_det_video.mp4")

# 3. 결과 시각화
results_image = results[0].plot()

# 4. 결과 이미지 저장
cv2.imwrite("./output_det_n_video.jpg", results_image)
print(f"예측 결과 이미지가 저장되었습니다.")

# 5. 결과 영상 저장
cap = cv2.VideoCapture("261014_2_yolo_basic/yolo_det_video.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
cap.release()

height, width = results[0].orig_shape
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter("./output_det_n_video.mp4", fourcc, fps, (width, height))

for result in results:
    writer.write(result.plot())

writer.release()
print(f"예측 결과 영상이 저장되었습니다.")