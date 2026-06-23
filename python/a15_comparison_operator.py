def main():
    print(10 == 100)
    print(10 != 100)
    print(10 < 100)
    print(10 <= 100)
    print(type(True))
    
    print(not True)
    print(not False)
    print(True and True)
    print(False or False)
    
    a = int(input("100 보다 큰 수를 입력하시오"))
    
    if a > 100:
        print("a는 100보다 큽니다.")
    print("프로그램을 종료합니다.")


if __name__ == "__main__":
    main()

