# App4SHM Server - Typewriter
#
# This class will allow us to write files, in the specified format specified
# by the Professors of ULHT's Civil Engineering department.
#
# Nuno Penim, Paulo Oliveira, 2021
#
# No tabs allowed for the safety of the entire project
# Use 4 spaces as indentation (I KNOW, BUT THAT'S HOW PYTHON ROLLS, I AM SORRY)

import app4shm.sys_helpers.time_aux_funcs as tf
from app4shm.entities.data import Data

buffer = ""


# Internal use functions, buffer manipulators
def __clear_buffer():
    global buffer
    buffer = ""
    return


def __is_buffer_empty() -> bool:
    global buffer
    if buffer is None or buffer == "":
        return True
    return False


def __write_header_to_buffer(station: str, sampling: float, start_date: str, start_time: str):
    global buffer
    buffer += "Station_code    " + station + "\n\n"
    buffer += "Sampling_rate   " + str(sampling) + "\n\n"
    buffer += "Start_date      " + start_date + "\n\n"
    buffer += "Start_time      " + start_time + "\n\n"
    buffer += "Time   X,g    Y,g    Z,g \n\n"
    return


def __write_reading_to_buffer(time: str, x: str, y: str, z: str):
    global buffer
    buffer += time + " " + x + " " + y + " " + z + "\n\n"
    return


# External use functions
def data_stream_to_buffer(data_stream: list[Data]) -> bool:
    # Assumingly, it is sorted!
    if len(data_stream) == 0:
        return False
    try:
        __clear_buffer()
        sample_obj = data_stream[0]
        station = sample_obj.identifier + "/" + sample_obj.group
        sampling = 50.0  # Hardcoded 50Hz, for now as we would need to change object format in both py and kt
        start_date = tf.get_str_date_from_millis(sample_obj.timestamp)
        start_time = tf.get_time_of_measuring_from_millis(sample_obj.timestamp)
        __write_header_to_buffer(station, sampling, start_date, start_time)
        for i in data_stream:
            __write_reading_to_buffer(tf.get_time_of_measuring_from_millis(i.timestamp), str(i.x), str(i.y), str(i.z))
            return True
    except:
        return False
