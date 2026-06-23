import datetime

def main():
    now = datetime.datetime.now()
    
    if 9 < now.hour < 12:
        print(f"현재 시간은 {now.hour}시로, 오전 입니다.")
    elif now.hour < 9:
        print(f"현재 시간은 {now.hour}시로, 새벽 입니다.")
    else:
        print(f"현재 시간은 {now.hour}시로, 오후 입니다.")
        
    
        
    print(now.month, type(now.month))
    
    if 0 < now.month < 4 or 11 < now.month < 13:
        print(f"현재 달은 {now.month}월로, 겨울 입니다.")
        
    if 3 < now.month < 6:
        print(f"현재 달은 {now.month}로, 봄 입니다.")
    if 5 < now.month < 9:
        print(f"현재 달은 {now.month}월로, 여름 입니다.")
    if 8 < now.month < 12:
        print(f"현재 달은 {now.month}월로, 가을 입니다.")

if __name__ == "__main__":
    main()