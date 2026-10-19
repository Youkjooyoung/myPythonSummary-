from sahi.predict import get_sliced_prediction
from sahi import AutoDetectionModel

# 1. 모델경로
model_path = "yolo11n.pt"

# 2. 모델로드
detection_model = AutoDetectionModel.from_pretrained(
    model_type="ultralytics",
    model_path=model_path,
    confidence_threshold=0.4
)

# 3. SAHI 적용
results = get_sliced_prediction(
    "demo_data/highway.jpg",
    detection_model,
    slice_height =50,
    slice_width = 50,
    overlap_height_ratio=0.1,
    overlap_width_ratio=0.1
)

# 4. 결과 저장
results.export_visuals(export_dir="sahi/")

# 5.탐지 개수 출력
print(f"탐지 객체 수 : {len(results.object_prediction_list)}")
print("모든 코드가 성공적으로 수행됐습니다.")
