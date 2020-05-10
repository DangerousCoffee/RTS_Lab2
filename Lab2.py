import numpy as np
import matplotlib.pyplot as plt
import random
from math import pi, sqrt

def signal(n, Wm, N, step):
    A = 0
    fi = 0
    W = np.arange(0, Wm, Wm/n)
    signal = [0 for i in range(N)]
    t = np.arange(0, N*step, step)
    for i in range(n):
        A = random.random()
        fi = random.uniform(0, pi*2)
        signal += A*np.sin(W[i]*t+fi)
    return t, signal

def correlation(arr1, arr2, M1, M2):
    N=len(arr1)
    corr=np.empty(N)
    sum=0
    for tau in range(N-1):
        sum=0
        for i in range(N-tau):
            sum+=(arr1[i]-M1)*(arr2[i+tau]-M2)
        corr[tau]=sum/(N-tau-1)
    corr[N-1]=corr[N-2]
    return corr


def expectation(arr):
    sum = 0
    for val in arr:
        sum+=val
    return sum/len(arr)

def variance(arr):
    M = expectation(arr)
    sum = 0
    for val in arr:
        sum+=(val-M)**2
    return sum/len(arr)

def autocorr(x, y, len):
    return np.array([1]+[np.corrcoef(x[:-tau], y[tau:])[0, 1] for tau in range(1, len)])

if __name__ == "__main__":
    n = 6
    Wm = 1500
    N = 1024
    step = 0.0001
    t, signal1 = signal(n, Wm, N, step)
    t, signal2 = signal(n, Wm, N, step)

    M1 = expectation(signal1)
    M2 = expectation(signal2)
    D1 = variance(signal1)
    D2 = variance(signal2)

    signal1ahead = list(signal1)
    signal1ahead.pop(0)
    signal1behind = signal1

    CORRxx = correlation(signal1, signal1, M1, M1)
    CORRxy = correlation(signal1, signal2, M1, M2)

    CORRxx_np = autocorr(signal1, signal1, len(signal1))
    CORRxy_np = autocorr(signal1, signal2, len(signal1))


    print("First signal expectation: {}\nFirst signal variance {}".format(M1, D1))
    print("Second signal expectation: {}\nSecond signal variance {}".format(M2, D2))

    fig2, (ax3, ax4) = plt.subplots(2)
    fig2.suptitle('Correlation')

    ax3.set_ylabel('xx')
    ax3.plot(t, CORRxx, color='red', linewidth=0.5)
    ax3.plot(t, CORRxx_np, color='green', linewidth=0.5)
    ax3.grid(True)

    ax4.set_xlabel('tau')
    ax4.set_ylabel('xy')
    ax4.plot(t, CORRxy, color='red', linewidth=0.5)
    ax4.plot(t, CORRxy_np, color='green', linewidth=0.5)
    ax4.grid(True)


    fig1, (axis1, axis2) = plt.subplots(2)
    fig1.suptitle("Signals")
    axis1.set_ylabel("signal 1")
    axis2.set_ylabel("signal 2")
    axis1.plot(t, signal1)
    axis1.grid(True)
    axis2.plot(t, signal2)
    axis2.grid(True)

    plt.show()

