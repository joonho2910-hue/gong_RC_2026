import numpy as np


def main():
    x =  np.arange(40).reshape(8, 5)
    print(x)
    y = np.arange(39, -1, -1).reshape(8,5)
    print(y)
    # linspace 내부 원소의 갯수를 확정
    z = np.linspace(30, 100, 40).reshape(8, 5)
    print(z)
    s1 = x + y
    print(s1)
    s2 = x - z
    print(s2)
    s3 = x / z
    print(s3)


if __name__ == '__main__':
    main()