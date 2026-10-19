from ultralytics    import FastSAM
import cv2

# 1. 입력 이미지 경로 지정
source = "demo_data/puppyandpeople.jpg"

# 2. FasSAM 소형 모델로드 (s = small , 가장 가벼움)
model = FastSAM("FastSAM-s.pt")

# 3. 텍스트 프롬프트로 "강아지"만 골라서 세그먼트
results = model(source,texts = "girl")

# 4. 결과 마스크를 원본 위에 그려서 이미지로 만들기
output_path = "./output_result.jpg"
output_image = results[0].plot()    # 마스크가 합성된 numpy 이미지 배열

# 5. 결과 저장
cv2.imwrite(output_path, output_image)

# 6. output_image는 이미지 "배열" 이라 그대로 출력하면 숫자가 수천 줄 쏟아짐 -> 경로를 출력
print(f"결과 이미지가 저장 됐습니다. {output_path}")

