colors = ["red", "green", "blue"] # 리스트(순서 있음, 수정이 가능)
# print(colors[0]) # 'red'
# print(colors[-1]) # 'blue'
# print(colors[0:2]) # 'red' and 'green'

# colors[-1] = "black" # 리스트 수정
# print(colors) # ['red', 'green', 'black']

# colors.append("pink") # 리스트에 요소 추가
# print(colors) # ['red', 'green', 'blue', 'pink']

# colors.insert(0, "white") # 리스트에 요소 삽입
# print(colors) # ['white', 'red', 'green', 'blue']
# colors.remove("white") # 리스트에서 요소 제거/

numbers = [8, 5, 3, 2, 7]# umbers.sort() # 리스트 정렬(오름차)
# numbers.sort() # 리스트 정렬(오름차)
# print(numbers) # [2, 3, 5, 7, 8]

# numbers.sort(reverse=True) # 리스트 정렬(내림차)
# print(numbers) # [8, 7, 5, 3, 2]
# numbers.reverse() # 리스트 뒤집기
# print(numbers) # [7, 2, 3, 5, 8]
print(2 in numbers) # True