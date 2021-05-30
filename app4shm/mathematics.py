# App4SHM Server - Mathematics
#
# This class will allow us to do the needed mathematic operations, such as
# Interpolation, in order to synchronize readings to the required time.
#
# Nuno Penim, Paulo Oliveira, 2021
#
# No tabs allowed for the safety of the entire project
# Use 4 spaces as indentation (I KNOW, BUT THAT'S HOW PYTHON ROLLS, I AM SORRY)

from scipy.interpolate import interpn as interpn
from app4shm.entities.data import Data
import numpy as np

# Constants and Parameters
INTERPOLATION_TYPE = 'linear'
TIME_INCREMENT = 10  # 10 ms

def interpolate_data_stream(data_stream: list[Data]):
    data_device = data_stream[0].identifier
    data_group = data_stream[0].group
    start_time = data_stream[0].timestamp
    data_times = []
    data_x = []
    data_y = []
    data_z = []
    for i in data_stream:
        data_times.append(float(i.timestamp))
        data_x.append(i.x)
        data_y.append(i.y)
        data_z.append(i.z)
    t_start = data_times[0]
    t_end = data_times[len(data_times)-1]
    t_interval_array = []
    start_me = t_start
    while start_me < t_end:
        t_interval_array.append(start_me)
        start_me += TIME_INCREMENT
    t_interval = np.array(t_interval_array)
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
