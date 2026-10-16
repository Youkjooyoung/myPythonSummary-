def meters_to_feet(meters: float) -> float:
    """
    미터를 피트로 환산
    """

    return meters * 3.28084


while True:
    user_input = input("피트로 환산할 미터값을 입력해주세요 : ")
    try:
        user_meters = float(user_input)
        feet = meters_to_feet(user_meters)
        print(f"{user_meters}m는 {feet} ft 입니다.")
        break  # 성공하면 루프종료
    except ValueError:
        print("숫자만 입력해주세요.")
