# App4SHM Server - Main script
#
# In here, all the data stream related and webservice related functions are present
#
# Nuno Penim, Paulo Oliveira, 2021
#
# No tabs allowed for the safety of the entire project
# Use 4 spaces as indentation (I KNOW, BUT THAT'S HOW PYTHON ROLLS, I AM SORRY)

import flask
from flask import render_template, request, redirect
import operator
import app4shm.typewriter as tw
from app4shm.entities.data import Data
import app4shm.sys_helpers.mathematics as mt
import app4shm.entities.grupo_db as gdb
import app4shm.entities.medicao_db as mdb
from app4shm.entities.dataPoint import DataPoint
import os
import pathlib

ZIP_FILE = "deliverable.zip"
PREFIX = "/app4shm"

# Web Service properties
app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TXT_UPLOADS'] = str(pathlib.Path(__file__).parent.resolve())+"\\txt"

# data stream and operations on it
data_stream = []


def clear_stream():
    global data_stream
    data_stream = []


def sort_stream():
    global data_stream
    data_stream.sort(key=operator.attrgetter("timestamp"))


def push_to_stream(data: Data):
    global data_stream
    data_stream.append(data)


def print_stream():
    global data_stream
    for i in data_stream:
        print(i.to_string())


def clear_repeated(data_stream: list[Data]):
    ds = data_stream.copy()
    indexes_to_rm = []
    for i in range(len(ds)):
        try:
            if ds[i].timestamp == ds[i + 1].timestamp:
                indexes_to_rm.append(i)
        except IndexError:
            pass
    for i in indexes_to_rm:
        try:
            del (ds[i])
        except IndexError:
            pass
    return ds


# Webservice itself
@app.route(f"{PREFIX}/diag")
def legacy():
    """
    This is just a legacy method, just to redirect people to the new page, in the root, just in case
    someone is evaluating our report and the server looks "dead". Expect it to be removed in future
    iterations of the project
    """
    return flask.redirect(flask.url_for('diag'))


@app.route(f"{PREFIX}/", methods=['GET'])
def diag():
    datalist = ""
    for i in data_stream:
        datalist += i.to_string()
    return flask.render_template("diag.html", datalist=datalist)


@app.route(f"{PREFIX}/db", methods=['GET', 'POST'])
def db():
    datalist = ""
    if request.method == "POST":
        if request.files:
            txt = request.files['txt']
            txt.save(os.path.join(app.config['TXT_UPLOADS'], txt.filename))

            count = -1
            group = []
            with open(os.path.join(app.config['TXT_UPLOADS'] + "/" + txt.filename), 'r') as f:
                for line in f:
                    count = count + 1
                    if count < 9:
                        continue
                    if count % 2 != 0:
                        continue
                    words = line.split()
                    group.append(float(words[3]))
                    datalist += words[3] +"\n"

            f.close()
            group = mt.mahalanobis(group)
            os.remove(os.path.join(app.config['TXT_UPLOADS'] + "/" + txt.filename))
            return flask.render_template("db.html", datalist=group)
    else:
        for user in mdb.showCol():
            datalist += "id:" + str(user.id) + "   Frequency:" + str(user.frequency) + "   X:" + str(
                user.x) + "   Y:" + str(user.y) + "   Z:" + str(
                user.z) + "   username:" + user.username + "   usernameGroup:" + user.usernameGroup + '\n'
    return flask.render_template("db.html", datalist=datalist)


@app.route(f"{PREFIX}/cleanup")
def cleanup():
    clear_stream()
    return flask.redirect(flask.url_for('diag'))


@app.route(f"{PREFIX}/data/reading", methods=['POST'])
def receive():
    local_stream = []
    received = flask.request.get_json()
    for i in received:
        data = Data(identifier=i['id'],
                    timestamp=int(i['timeStamp']),
                    x=float(i['x']),
                    y=float(i['y']),
                    z=float(i['z']),
                    group=i['group'])
        try:
            gdb.add_group(gdb.get_id() + 1, data.group)
        except:
            continue
        push_to_stream(data)
        local_stream.append(data)
    sort_stream()
    local_stream.sort(key=operator.attrgetter("timestamp"))
    local_stream = clear_repeated(local_stream)
    interpolated = mt.interpolate_data_stream(local_stream)
    time_array = []
    x_array = []
    y_array = []
    z_array = []
    for i in interpolated:
        time_array.append(i.timestamp)
        x_array.append(i.x)
        y_array.append(i.y)
        z_array.append(i.z)
    welch_x_f, welch_x_pxx = mt.calculate_welch_from_array(time_array, x_array)
    welch_y_f, welch_y_pxx = mt.calculate_welch_from_array(time_array, y_array)
    welch_z_f, welch_z_pxx = mt.calculate_welch_from_array(time_array, z_array)
    json = flask.jsonify(welch_x_f.tolist(), welch_x_pxx.tolist(), welch_y_pxx.tolist(), welch_z_pxx.tolist())
    return json

#TODO enviar verde vermelho para o telemovel
@app.route(f"{PREFIX}/data/results", methods=['POST'])
def results():
    received = flask.request.get_json()
    for i in received:
        data = DataPoint(identifier=i['id'],
                         t=float(i['t']),
                         x=float(i['x']),
                         y=float(i['y']),
                         z=float(i['z']),
                         group=i['group'])
    group = mdb.showColx("testgroup")


@app.route(f"{PREFIX}/data/points", methods=['POST'])
def receivePoints():
    received = flask.request.get_json()
    for i in received:
        data = DataPoint(identifier=i['id'],
                         t=float(i['t']),
                         x=float(i['x']),
                         y=float(i['y']),
                         z=float(i['z']),
                         group=i['group'])

        try:
            mdb.add_group(mdb.get_id() + 1, data.t, data.x, data.y, data.z, data.identifier, data.group)
        except:
            continue
    return ''


@app.route(f"{PREFIX}/generate")
def write_files():
    global data_stream
    dicte = {}
    tw.clear_write_output()
    for i in data_stream:
        key = i.identifier
        if dicte.get(key) is None:
            dicte[key] = []
        dicte[key].append(i)
    for i in dicte.keys():
        tw.data_stream_to_buffer(dicte[i])
        tw.buffer_to_file(i)
    tw.zip_file("deliverable")
    return flask.send_from_directory("..", ZIP_FILE, as_attachment=True, cache_timeout=0)


@app.route(f"{PREFIX}/interpolate")
def crude_interpolate():
    interpolated = mt.interpolate_data_stream(data_stream)
    dicte = {}
    tw.clear_write_output("inter_temp/")
    for i in interpolated:
        key = i.identifier
        if dicte.get(key) is None:
            dicte[key] = []
        dicte[key].append(i)
    for i in dicte.keys():
        tw.data_stream_to_buffer(dicte[i])
        tw.buffer_to_file(i + "_int", "inter_temp/")
    tw.zip_file("interpolated", "inter_temp/")
    return flask.send_from_directory("..", "interpolated.zip", as_attachment=True, cache_timeout=0)

app.run(host="0.0.0.0", port="8080")  # change to port 80 on the server or use iptables, idk
