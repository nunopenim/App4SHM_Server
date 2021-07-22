# App4SHM Server - Mathematics
#
# This class will allow us to do the needed mathematic operations, such as
# Interpolation, in order to synchronize readings to the required time.
#
# Nuno Penim, Paulo Oliveira, 2021
#
# No tabs allowed for the safety of the entire project
# Use 4 spaces as indentation (I KNOW, BUT THAT'S HOW PYTHON ROLLS, I AM SORRY)
import traceback

from scipy.interpolate import interpn as interpn
from app4shm.entities.data import Data
from scipy.stats import norm
import numpy as np
from scipy import signal

# Constants and Parameters
INTERPOLATION_TYPE = 'linear'
TIME_INCREMENT = 10  # 10 ms


def interpolate_data_stream(data_stream: list[Data]):
    data_device = data_stream[0].identifier
    data_group = data_stream[0].group
    data_times = []
    counter = 0
    data_x = []
    data_y = []
    data_z = []
    data_stream.sort(key=lambda x: x.timestamp)
    for i in data_stream:
        data_times.append(float(i.timestamp))
        data_x.append(i.x)
        data_y.append(i.y)
        data_z.append(i.z)
    while counter < len(data_times) - 1:
        count = data_times.count(data_times[counter])
        if count > 1:
            data_times.remove(data_times[counter])
            data_x.remove(data_x[counter])
            data_y.remove(data_y[counter])
            data_z.remove(data_z[counter])
            counter -= 1
        counter += 1
    t_start = data_times[0]
    t_end = data_times[len(data_times) - 1]
    t_interval_array = []
    start_me = t_start
    while start_me < t_end:
        t_interval_array.append(start_me)
        start_me += TIME_INCREMENT
    t_interval = np.array(t_interval_array)
    try:
        x_nd = interpn((np.array(data_times),), np.array(data_x), t_interval, INTERPOLATION_TYPE)
        y_nd = interpn((np.array(data_times),), np.array(data_y), t_interval, INTERPOLATION_TYPE)
        z_nd = interpn((np.array(data_times),), np.array(data_z), t_interval, INTERPOLATION_TYPE)
        inter_x = x_nd.tolist()
        inter_y = y_nd.tolist()
        inter_z = z_nd.tolist()
        ret_stream = []
        for i in range(0, len(t_interval)):
            ret_stream.append(Data(identifier=data_device,
                                   timestamp=t_interval[i],
                                   x=inter_x[i],
                                   y=inter_y[i],
                                   z=inter_z[i],
                                   group=data_group))
        return ret_stream
    except ValueError:
        track = traceback.format_exc()
        print(track)
        print("---------------------")
        print(data_times)
        return []


def calculate_welch_from_array(time: list[float], accelerometer_input: list[float]):
    delta_times = 0.01  # 10ms
    measuring_frequency = delta_times ** (-1)
    total_sample_number = len(time)  # measuring_frequency*len(time)
    n_segments = 3
    ls = int(np.round(total_sample_number / n_segments))
    overlap_perc = 50
    overlaped_samples = int(np.round(ls * overlap_perc / 100))
    discrete_fourier_transform_points = ls
    f, pxx = signal.welch(accelerometer_input, fs=measuring_frequency, nperseg=ls, noverlap=overlaped_samples,
                          nfft=discrete_fourier_transform_points)
    return f, pxx
    # f1 = np.reshape(f, (1, len(f)))
    # fs = 10e3
    # N = 1e5
    # amp = 2*np.sqrt(2)
    # freq = 1234
    # noise_power = 0.001 * fs / 2
    # time = np.arange(N) / fs
    # x = amp*np.sin(2*np.pi*freq*time)
    # x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
    # f, Pxx_den = signal.welch(x, fs, nperseg=1024)


def scoreMahalanobis_shm(x, mean, cov):
    mahalanobis = []
    mahalanobis.append(np.dot(np.dot((x - mean), np.linalg.inv(cov)), np.transpose((x - mean))))
    return mahalanobis


def mahalanobis(group, x):
    m = 3
    # n = len(group)

    testPoint = np.array([x.z_freq1, x.z_freq2, x.z_freq3])

    PFA = 0.05
    degFreedom = m
    # UCL = 3.8415 # m = 1
    # UCL = 5.9915 # m = 2
    UCL = 7.8147  # m = 3
    # print(UCL)
    values = np.array([])

    for freq in group:
        values = np.append(values, freq.z_freq1)
        values = np.append(values, freq.z_freq2)
        values = np.append(values, freq.z_freq3)

    values = np.reshape(values, (-1, 3))
    #print(values)
    covMatrix = np.cov(np.transpose(values), bias=True)
    #print(covMatrix)
    mean = np.mean(values, axis=0)
    #print(mean)

    DI = scoreMahalanobis_shm(testPoint, mean, covMatrix)
    #print(DI)
    for i in DI:
        if i <= UCL:
            return True
        else:
            return False
