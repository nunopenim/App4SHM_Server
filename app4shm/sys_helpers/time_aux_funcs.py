# App4SHM Server - Time-Related Auxiliary Functions
#
# This class will allow us to do time related operations which include, but will not be
# limited to, converting a Epoch milli-second time value to a string timestamp
#
# Nuno Penim, Paulo Oliveira, 2021
#
# No tabs allowed for the safety of the entire project
# Use 4 spaces as indentation (I KNOW, BUT THAT'S HOW PYTHON ROLLS, I AM SORRY)

import datetime as dt


# Internal use functions
# In case you don't know, __ makes it "private"

def __millis_to_str_stamp(millis):
    intermediate_fractionate_time = millis / 1000.0  # we need a fractionate time, more on that later
    time_stamp = dt.datetime.fromtimestamp(intermediate_fractionate_time).strftime('%Y-%m-%d %H:%M:%S.%f')
    # https://stackoverflow.com/questions/11040177/datetime-round-trim-number-of-digits-in-microseconds
    # most times, the last 3 digits are 0s, and I don't know if that messes with the Professors' MATLAB algos
    # So we keep that like normal for now!
    head = time_stamp[:-7]
    tail = time_stamp[-7:]
    f = float(tail)
    temp = "{:.03f}".format(f)
    new_tail = temp[1:]
    return head + new_tail


# External use functions
def get_str_date_from_millis(millis):
    time_stamp = __millis_to_str_stamp(millis)
    date_str = time_stamp.split(" ")[0]
    return date_str


def get_time_of_measuring_from_millis(millis):
    time_stamp = __millis_to_str_stamp(millis)
    time_str = time_stamp.split(" ")[1]
    return time_str


def millis_to_sec(millis):
    secs = float(millis / 1000)
    sec_str = str(secs)
    return str(sec_str)
