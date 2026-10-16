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