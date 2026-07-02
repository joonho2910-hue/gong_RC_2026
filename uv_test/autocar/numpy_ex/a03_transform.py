import numpy as np


def main():
    arr = np.arange(100)
    print(arr)
    reshp = arr.reshape((2, 5, 5, 2))
    print(reshp, reshp.shape)
    
    print(reshp[1][3][3][1])   # 다차원 리스트 방식
    print(reshp[1, 3, 3, 1])   # np 에서 접근 하는 방식
    print(reshp[1, :, 2:4, 1], reshp[1, :, 2:4, 1].shape)   
    f1 = reshp.flatten()  
    print(f1, f1.shape)
    
if __name__ == '__main__':
    main()