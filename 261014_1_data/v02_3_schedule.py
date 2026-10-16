import os
import time
from datetime import datetime

import cv2
import schedule

# 사진 캡쳐 간격 설정
interval_time = 5


def capture_image():
    save_dir = "./capture_images"
    os.makedirs(save_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)

    success, frame = cap.read()
    if success:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(save_dir, f"{timestamp}.jpg")
        cv2.imwrite(file_path, frame)
        print(f"사진이 저장되었습니다. {file_path}")
    else:
        print("카메라 읽기 실패")

    cap.release()


capture_image()


# 스케쥴러 설정
schedule.every(interval_time).seconds.do(capture_image)

while True:
    schedule.run_pending()
    time.sleep(1)
