# 파일 새로 만들기
# with open("memo02.txt","x", encoding="utf-8") as f:

#     f.write("추가 작업입니다")


# 이미지 읽기
#  with open("monaliza.jpg", "rb") as f:
#     data = f.read()

#     print(data[0])
#     print(list(data[:4]))
#     print("완료")

# 이미지 읽기
# with open("monaliza.jpg", "rb") as f:
#     numbers = list(f.read())

#     print(numbers[:4])

# 이미지 쓰기
# with open("monaliza_copy.jpg", "wb") as f:
#     f.write(bytes(numbers))

# 이미지 읽기와 쓰기
# memo.txt 파일 깨진 상태라 제거 후 다시 생성했음
with open("memo.txt", "w", encoding="utf-8") as f:
    f.write("Hello Python")

with open("memo.txt", "r+", encoding="utf-8") as f:
    print(f.read())
    f.seek(0)
    f.write("REHELLO")
    # replace로 제거 후 가능

with open("memo.txt", "r", encoding="utf-8") as f:
    print(f.read())

print("완료")
