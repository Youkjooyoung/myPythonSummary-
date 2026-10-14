class Cat:
    def __init__(self, name, color, month):
        self.name = name
        self.color = color
        self.month = month

    # 1. 행동을 출력하는 메서드
    def info(self):
        print(f"이 고양이의 이름은 {self.name}이고 색은 {self.color}이며 개월수는 {self.month}개월 입니다.")

    def meow(self):
        print(f"{self.name}: 야옹~")

    def sleep(self):
        print(f"{self.name}이(가) 쿨쿨 자고 있습니다.")

    # 2. 매개변수를 받는 메서드
    def eat(self, food):
        print(f"{self.name}이(가) {food}을(를) 먹습니다.")

    def play(self, toy):
        print(f"{self.name}이(가) {toy}(으)로 놀고 있습니다.")

    # 3. 객체의 값을 바꾸는 메서드
    def grow(self, months=1):
        self.month += months
        print(f"{self.name}이(가) {months}개월 자라서 {self.month}개월이 되었습니다.")

    def rename(self, new_name):
        print(f"{self.name} → {new_name}(으)로 이름이 바뀌었습니다.")
        self.name = new_name

    # 4. 값을 판단해서 돌려주는 메서드
    def is_kitten(self):
        return self.month < 12


cat1 = Cat("고먐미", "하얀색", 9)
cat2 = Cat("반려묘", "검은색", 1)
cat3 = Cat("냐옹이", "베이지색", 3)

print("=== 처음 정보 ===")
cat1.info()
cat2.info()
cat3.info()

print("\n=== 행동 ===")
cat1.meow()
cat1.eat("츄르")
cat2.play("낚싯대")
cat3.sleep()

print("\n=== 값 바꾸기 ===")
cat2.grow(3)
cat3.rename("나비")

print("\n=== 판단 ===")
print(cat1.name, "아기 고양이?", cat1.is_kitten())
if cat3.is_kitten():
    print(f"{cat3.name}은(는) 아기 고양이예요!")

print("\n=== 바뀐 정보 ===")
cat1.info()
cat2.info()
cat3.info()
