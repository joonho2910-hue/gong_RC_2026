import random

def main():
    hanguls = list("김나박이승상주허유류곽지")
    hanguls2 = list("가나다라윤화섭석흥민규성준상동혁와파타하길으아어기호")
    for _ in range(100):
        name = random.choice(hanguls) + str().join(random.choices(hanguls,k=2))
        print(name)
        
    mu = 3
    sigma = 5
    print(random.gauss(mu, sigma))
    print(random.normal)
        
        
if __name__ == "__main__":
    main()