# import cv2
# from ultralytics import YOLO

# # 1. 모델 로드
# model = YOLO("261014_2_yolo_basic/yolo11n.pt")

# # 2. 모델 추론
# results = model("261014_2_yolo_basic/yolo_det_video.mp4")

# # 3. 결과 시각화
# results_image = results[0].plot()

# # 4. 결과 이미지 저장
# cv2.imwrite("./output_det_n_video.jpg", results_image)
# print(f"예측 결과 이미지가 저장되었습니다.")

# # 5. 결과 영상 저장
# cap = cv2.VideoCapture("261014_2_yolo_basic/yolo_det_video.mp4")
# fps = cap.get(cv2.CAP_PROP_FPS)
# cap.release()

# height, width = results[0].orig_shape
# fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# writer = cv2.VideoWriter("./output_det_n_video.mp4", fourcc, fps, (width, height))

# for result in results:
#     writer.write(result.plot())

# writer.release()
# print(f"예측 결과 영상이 저장되었습니다.")


from pathlib import Path

from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent


def main():
    # 1. 분류용 사전학습 모델 불러오기
    model = YOLO("yolo11n-cls.pt")

    # 2. 학습 (경로는 모두 절대 경로로)
    model.train(
        data=str(BASE_DIR / "dataset"),  # train/ val/ 이 있는 폴더
        epochs=50,
        imgsz=224,
        project=str(BASE_DIR / "runs_emotion"),  # 절대 경로 → runs/classify 로 안 감
        name="exp1",
    )


# 3. 윈도우용 보호 구문
if __name__ == "__main__":
    main()
