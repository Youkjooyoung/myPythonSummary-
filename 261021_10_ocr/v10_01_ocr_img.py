# import pytesseract          # OCR 사용
# from PIL    import Image    # 이미지 처리도구
# import os

# # 1. Tesseract 실행 파일 경로 지정
# pytesseract.pytesseract.tesseract_cmd = "c:/Program Files/Tesseract-OCR/tesseract.exe"

# # 2. 이미지 불러오기
# # image = Image.open("261021_10_ocr/input.jpg")
# # image = Image.open("261021_10_ocr/input_kor.jpg")
# image = Image.open("261021_10_ocr/car_number.jpg")

# # 3. OCR 수행
# results = pytesseract.image_to_string(
#     image,
#     lang='kor+eng'
# )

# # 4. 결과 출력
# print(results)
# """
#  결과내용(영어) :
# This is a lot of 12 point text to test the
# ocr code and see if it works on all types
# of file format.

# The quick brown dog jumped over the
# lazy fox. The quick brown dog jumped
# over the lazy fox. The quick brown dog
# jumped over the lazy fox. The quick
# brown dog jumped over the lazy fox.

# """

# """
# 결과내용(한국어) :
# Ｌ스트스때스56<1때

# 이수진

# 팀장 / 제품개발팀

# +123-456-7890
# 1『6110@「62117/8「620[5166.0007
# 123 40616 56, 407 다, 51 12345

# """


# """
# 결과내용(한국어 + 영어) : 
# LARANASKIN

# 이수진

# 팀장 / 제품개발팀

# +123-456-7890
# hello@reallygreatsite.com
# 123 Anywhere St., Any City, ST 12345
    
# """


# # 1. 차 번호판 인식
import easyocr

# 1) 리더 생성 (한국어 + 영어), 처음 실행 때 모델 자동 다운로드
reader = easyocr.Reader(['ko', 'en'])

# 2) OCR 수행 → [(좌표, 글자, 신뢰도), ...]
plate_results = reader.readtext("261021_10_ocr/car_number.jpg")

# 3) 결과 출력
for box, text, conf in plate_results:
    print(f"번호판 : {text}  (신뢰도 {conf:.2f})")

"""
결과내용(번호판) :
번호판 : 68오 8269  (신뢰도 0.64)
"""
