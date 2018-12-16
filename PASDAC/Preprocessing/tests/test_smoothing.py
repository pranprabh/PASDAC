import os
import sys
import pandas as pd
import numpy as np
from numpy.testing import assert_array_almost_equal
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from smoothing import smooth_boxcar, smooth_gaussian
import matplotlib.pyplot as plt



def test_smooth_gaussian_immutability():
    Fs = 10
    f = 0.01
    sample = 1000
    x = np.arange(sample)
    y = np.sin(2 * np.pi * f * x / Fs)

    data = pd.DataFrame(data=y*20, columns=["Sensor1"], dtype = float)

    plt.title('Before smoothing')
    plt.plot(data['Sensor1'])
    plt.show()
    
    smoothed = smooth_gaussian(data, ["Sensor1"], 30, 1)

    plt.title('After smoothing')
    plt.plot(smoothed['Sensor1'])
    plt.show()

    assert_array_almost_equal(data['Sensor1'].values, smoothed['Sensor1'].values, decimal=1)



def test_smooth_boxcar_immutability():
    Fs = 10
    f = 0.01
    sample = 1000
    x = np.arange(sample)
    y = np.sin(2 * np.pi * f * x / Fs)

    data = pd.DataFrame(data=y*20, columns=["Sensor1"], dtype = float)

    plt.title('Before smoothing')
    plt.plot(data['Sensor1'])
    plt.show()
    
    smoothed = smooth_gaussian(data, ["Sensor1"], 30, 1)

    plt.title('After smoothing')
    plt.plot(smoothed['Sensor1'])
    plt.show()

    assert_array_almost_equal(data['Sensor1'].values, smoothed['Sensor1'].values, decimal=1)



def test_smooth_boxcar():
    Fs = 10
    f = 0.1
    sample = 1000
    x = np.arange(sample)
    y = np.sin(2 * np.pi * f * x / Fs)

    data = pd.DataFrame(data=y*20+np.random.randint(0,10,size=(1000)), columns=["Sensor1"], dtype = float)

    plt.title('Before smoothing')
    plt.plot(data['Sensor1'])
    plt.show()
    
    smoothed = smooth_boxcar(data, ["Sensor1"], 30)

    plt.title('After smoothing')
    plt.plot(smoothed['Sensor1'])
    plt.show()



def test_smooth_gaussian():
    Fs = 10
    f = 0.1
    sample = 1000
    x = np.arange(sample)
    y = np.sin(2 * np.pi * f * x / Fs)

    data = pd.DataFrame(data=y*20+np.random.randint(0,10,size=(1000)), columns=["Sensor1"], dtype = float)

    plt.title('Before smoothing')
    plt.plot(data['Sensor1'])
    plt.show()
    
    smoothed = smooth_gaussian(data, ["Sensor1"], 30, 1)

    plt.title('After smoothing')
    plt.plot(smoothed['Sensor1'])
    plt.show()



if __name__ == '__main__':
	
    print('==================================================\n')
    print('test boxcar:')
    test_smooth_boxcar()

    print('==================================================\n')
    print('test gaussian:')
    test_smooth_gaussian()
    
    print('==================================================\n')
    print('test boxcar_immutability:')
    test_smooth_boxcar_immutability()
    
    print('==================================================\n')
    print('test gaussian_immutability:')
    test_smooth_gaussian_immutability()


