def main():
    number = int(input("정수를 입력하시오"))

    #if number % 2 == 0:
     #   print(f"{number}는 짝수입니다.")
    #else:
     #   print(f"{number}는 홀수입니다.")
    print("짝수" if number % 2 == 0 else "홀수","입니다.")
if __name__ == "__main__":
    main()