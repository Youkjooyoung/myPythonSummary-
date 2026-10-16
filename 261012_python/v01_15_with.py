# 새롭게 생성, 기존 내용이 있다면 덮어씀
# with open("memo.txt","w", encoding="utf-8") as f:
#     f.write("안녕, 파이썬!\n")
#     f.write("with문이 자동으로 닫아줌 \n")

# 파일 읽기
# with open("memo.txt", "r", encoding="utf-8") as f:
#     text = f.read()

#     # print(text) # 새로운 한 줄 추가

# 파일 이어 쓰기
with open("memo.txt", "a", encoding="utf-8") as f:
    f.write("파일 이어쓰기 진행")

    print("완료")
# 블록을 빠져나오면 파일은 알아서 닫힘
