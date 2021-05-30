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
import os
import shutil

WRITEDIR = "temp/"
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
    buffer += "Station_code    " + station + "\n"
    buffer += "Sampling_rate   " + str(sampling) + "\n"
    buffer += "Start_date      " + start_date + "\n"
    buffer += "Start_time      " + start_time + "\n"
    buffer += "Time(s)   X,g(m*s^-2)    Y,g(m*s^-2)    Z,g(m*s^-2) \n\n"
    return


def __write_reading_to_buffer(time: str, x: str, y: str, z: str):
    global buffer
    buffer += time + " " + x + " " + y + " " + z + "\n"
    return


# External use functions
def data_stream_to_buffer(data_stream: list[Data]) -> bool:
    # Assumingly, it is sorted!
    if len(data_stream) == 0:
        return False
    try:
        __clear_buffer()
        sample_obj = data_stream[0]
        start_tstamp = sample_obj.timestamp
        station = sample_obj.identifier + "/" + sample_obj.group
        sampling = 50.0  # Hardcoded 50Hz, for now as we would need to change object format in both py and kt
        start_date = tf.get_str_date_from_millis(sample_obj.timestamp)
        start_time = tf.get_time_of_measuring_from_millis(sample_obj.timestamp)
        __write_header_to_buffer(station, sampling, start_date, start_time)
        for i in data_stream:
            tstamp = i.timestamp - start_tstamp
            __write_reading_to_buffer(tf.millis_to_sec(tstamp), str(i.x), str(i.y), str(i.z))
        return True
    except:
        return False


def clear_write_output(writedir=WRITEDIR):
    shutil.rmtree(writedir)


def buffer_to_file(filename: str, writedir=WRITEDIR) -> bool:
    if not os.path.exists(writedir):
        os.mkdir(writedir)
    if os.path.exists(writedir + filename + ".txt"):
        os.remove(writedir + filename + ".txt")
    try:
        file = open(writedir + filename + '.txt', "w")
        file.write(buffer)
        file.close()
        return True
    except:
        return False


def zip_file(name_str, writedir=WRITEDIR):
    if os.path.exists(name_str + ".zip"):
        os.remove(name_str + ".zip")
    shutil.make_archive(name_str, "zip", writedir)
    return
