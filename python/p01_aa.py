def main():
    # 1. 정보 입력받기
    product_name = input("상품명을 입력하세요: ")
    price_input = input("상품 가격을 입력하세요: ")
    discount_input = input("할인율(%)을 입력하세요: ")

    try:
        # 2. 문자열을 숫자로 변환 시도 (실수형 float 사용)
        price = float(price_input)
        discount_rate = float(discount_input)
    except ValueError:
        # 숫자로 변환할 수 없는 값(문자 등)이 입력되었을 때 실행
        print("가격과 할인율은 숫자로 입력해야 합니다.")
        return

    # 3. 할인 금액 및 최종 가격 계산
    discount_amount = price * discount_rate / 100
    final_price = price - discount_amount

    # 4. 결과 출력 (f-string 사용, 금액은 보기 좋게 천 단위 콤마 추가 및 소수점 제거)
    print("\n=== 결제 정보 ===")
    print(f"상품명: {product_name}")
    print(f"원래 가격: {price:,.0f}원")
    print(f"할인율: {discount_rate}%")
    print(f"할인 금액: {discount_amount:,.0f}원")
    print(f"최종 가격: {final_price:,.0f}원")

if __name__ == "__main__":
    main()