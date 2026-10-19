from ultralytics import SAM
import time
import cv2

# 1. 모델 로드
model = SAM("sam_b.pt")
# sam_b(빠름), 1(정확)

# 2. 이미지 경로 설정
image_path = "demo_data/coins.jpg"

# 2-1. 이미지 읽기
input_image = cv2.imread(image_path)

# 2-2. 이미지 리사이즈
re_input_path = cv2.resize(input_image,(640,480))

# 3. 추론 시간 측정 시작
start_time = time.time()

# 4. 모델 추론
model(re_input_path,
      save = True,
    show_boxes=False
    # show_labels = False
      )

# 5. 추론 시간 측정 종료
end_time = time.time()

# 6. 결과 로그 출력
model_time = end_time - start_time
print(f"총 추론 시간 : {model_time:.2f}")
print("SAM 추론 종료")

