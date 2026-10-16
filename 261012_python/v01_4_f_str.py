name = "King"
age = 99

# 기존방식
# print("저는",name,"입니다.나이는",age,"살입니다.")

# f-string 방식
# print(f"저는 {name}입니다.나이는 {age}살입니다.")


# 표현식
# x = 1
# y = 3
# print(f"{x} + {y} = {x+y}") # 1 + 3 = 4

# .format() 방식
# {} 자리에 순서대로 채움
print("저는 {}입니다.나이는 {}살입니다.".format(name, age))
