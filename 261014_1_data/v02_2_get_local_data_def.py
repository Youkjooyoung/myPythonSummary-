# import cv2 #  카메라 다루는 도구
# import os  # 폴더를 만드는 도구
# from datetime import datetime # 현재시간을 알려주는 도구

# # [1단계] 사진을 저장할 폴더 준비
# save_dir = "./capture_images"
# os.makedirs(save_dir, exist_ok=True)  # 폴더가 없으면 자동생성

# # [2단계] 카메라를 킨다.
# cap = cv2.VideoCapture(0)

# # [3단계] 사진을 한 장 찍기.
# success, frame = cap.read() # success = True면 성공 , frame = 찍힌이미지
# if success:
#     # 사진 파일명 : 찍은 시간을 쓰면 여러 장을 찍어도 이름이 겹치지 않는다.
#      # + 언제 찍었는지 알 수 있다.  
#      timestamp = datetime.now().strftime("%Y%m_%H%M%S")
#      file_path = os.path.join(save_dir, f"{timestamp}.jpg")
     
#      # 파일로 저장
#      cv2.imwrite(file_path, frame)
#      print(f"사진이 저장되었습니다.{file_path}")
     
# else:
#     print("카메라 읽기 실패")

# # [4단계] 카메라 종료    
# cap.release()

#위 코드 함수로 작성
import cv2
import os
from datetime import datetime


def prepare_folder(save_dir):
    os.makedirs(save_dir, exist_ok=True)


def make_file_path(save_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(save_dir, f"{timestamp}.jpg")


def capture_photo(save_dir="./capture_images"):
    prepare_folder(save_dir)

    cap = cv2.VideoCapture(0)
    success, frame = cap.read()

    if success:
        file_path = make_file_path(save_dir)
        cv2.imwrite(file_path, frame)
        print(f"사진이 저장되었습니다. {file_path}")
    else:
        print("카메라 읽기 실패")

    cap.release()


capture_photo()