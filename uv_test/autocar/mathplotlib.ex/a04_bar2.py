import matplotlib.pyplot as plt
import numpy as np


def main():
    x = np.arange(10)
    data = np.random.random(10)
    plt.barh(range(len(data)), data)
    plt.bar(x, data)
    fig = plt.figure(figsize=(5, 5))
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ax1.barh(x, data, width=0.1)
    ax2.barh(x, data, align="edge")
    fig2 = plt.figure(figsize=(5, 5))
    ax1 = fig2.add_subplot(2, 1, 1)
    data = np.random.random(30).reshape(3,10)
    ax1.barh(np.arange(10), data[0], color="lightgray")
    ax1.barh(np.arange(10), data[1], color="gray")
    ax1.barh(np.arange(10), data[2], color="black")
    ax2 = fig2.add_subplot(2, 1, 2)
    ax2.barh(np.arange(0, 50, 5), data[0], color="lightgray")
    ax2.barh(np.arange(0, 50, 5) + 1, data[1], color="gray")
    ax2.barh(np.arange(0, 50, 5) + 2, data[2], color="black")
    fig3 = plt.figure(figsize=(5, 5))
    ax1 = fig3.add_subplot(2, 1, 1)
    ax1.bar(np.arange(10), data[0], color="gray")
    ax1.bar(np.arange(10), data[1], color="lightgray", bottom=data[0])
    ax1.bar(np.arange(10), data[2], color="black", bottom=[1])
    plt.show()
    
if __name__ == "__main__":
    main()
    
   