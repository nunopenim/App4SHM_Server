# App4SHM Server - Main script
#
# In here, all the data stream related and webservice related functions are present
#
# Nuno Penim, Paulo Oliveira, 2021
#
# No tabs allowed for the safety of the entire project
# Use 4 spaces as indentation (I KNOW, BUT THAT'S HOW PYTHON ROLLS, I AM SORRY)
import traceback

import flask
import numpy as np
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
import random

ZIP_FILE = "deliverable.zip"
PREFIX = "/app4shm"

# Web Service properties
app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TXT_UPLOADS'] = str(pathlib.Path(__file__).parent.resolve()) + "/txt"

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
        infrastructure = request.form['infrastructure']

        # infrastructure name error checks
        groups = gdb.showCol()
        if infrastructure == "":
            return flask.render_template("db.html", datalist="please enter an infrastructure name")
        for group in groups:
            if group.username != infrastructure and group.username.upper() == infrastructure.upper():
                return flask.render_template("db.html",
                                             datalist="infrastructure already exists with different capitalization")

        if request.files:
            txt = request.files['txt']
            txt.save(os.path.join(app.config['TXT_UPLOADS'], txt.filename))

            count = -1
            data = []
            with open(os.path.join(app.config['TXT_UPLOADS'] + "/" + txt.filename), 'r') as f:
                for line in f:
                    count = count + 1
                    words = line.split()

                    d = DataPoint(
                        identifier='Server',
                        z_freq1=float(words[0]),
                        z_freq2=float(words[1]),
                        z_freq3=float(words[2]),
                        group=infrastructure,
                        testing=True
                    )
                    data.append(d)
                    mdb.add_group(mdb.get_id() + 1, d.z_freq1, d.z_freq2, d.z_freq3, d.identifier, d.group)
                    datalist += words[0]
                    datalist += words[1]
                    datalist += words[2] + "\n"

            f.close()

            try:
                gdb.add_group(gdb.get_id() + 1, data[0].group)
            except:
                # python has forced my hand, except should be empty
                data

            # group = mt.mahalanobis(data)
            os.remove(os.path.join(app.config['TXT_UPLOADS'] + "/" + txt.filename))
            # return flask.render_template("db.html", datalist=group)
            datalist = ""
    for user in mdb.showCol():
        datalist += "id:" + str(user.id) + "   z_freq1:" + str(user.z_freq1) + "   z_freq2:" + str(
            user.z_freq2) + "   z_freq3:" + str(
            user.z_freq3) + "   username:" + user.username + "   infrastructure:" + user.usernameGroup + '\n'
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
    mean = []
    try:
        values = mdb.showColx(received[0]['group'])
        count = 0.0
        meanValue1 = 0.0
        meanValue2 = 0.0
        meanValue3 = 0.0
        for i in values:
            meanValue1 += i.z_freq1
            meanValue2 += i.z_freq2
            meanValue3 += i.z_freq3
            count += 1
        meanValue1 = meanValue1 / count
        meanValue2 = meanValue2 / count
        meanValue3 = meanValue3 / count
        mean.append(meanValue1)
        mean.append(meanValue2)
        mean.append(meanValue3)
    except:
        print(traceback.format_exc())
        mean = [0, 0, 0]

    for i in interpolated:
        time_array.append(i.timestamp)
        x_array.append(i.x)
        y_array.append(i.y)
        z_array.append(i.z)
    welch_x_f, welch_x_pxx = mt.calculate_welch_from_array(time_array, x_array)
    welch_y_f, welch_y_pxx = mt.calculate_welch_from_array(time_array, y_array)
    welch_z_f, welch_z_pxx = mt.calculate_welch_from_array(time_array, z_array)
    json = flask.jsonify(mean, welch_x_f.tolist(), welch_x_pxx.tolist(), welch_y_pxx.tolist(), welch_z_pxx.tolist())
    return json


@app.route(f"{PREFIX}/db/delete", methods=['GET', 'POST'])
def dbDelete():
    names = []
    infrastructures = gdb.showCol()
    for i in infrastructures:
        names.append(i)
    return flask.render_template("delete_db.html", datalist=names)


@app.route(f"{PREFIX}/db/<int:id>/<string:username>", methods=['GET', 'POST'])
def dbDeleteX(id: int, username: str):
    gdb.delCol(id)
    mdb.delCol(username)
    return flask.redirect(f"{PREFIX}/db")


@app.route(f"{PREFIX}/data/points", methods=['POST'])
def receivePoints():
    received = flask.request.get_json()
    testing = False
    frequencies = [received[0]['t'], received[1]['t'], received[2]['t']]

    data = DataPoint(identifier=received[0]['id'],
                     z_freq1=float(frequencies[0]),
                     z_freq2=float(frequencies[1]),
                     z_freq3=float(frequencies[2]),
                     group=received[0]['group'],
                     testing=bool(received[0]['testing']))

    if data.testing:
        testing = True
        mdb.add_group(mdb.get_id() + 1, data.z_freq1, data.z_freq2, data.z_freq3, data.identifier, data.group)

    if testing:
        return ''

    return flask.jsonify(mt.mahalanobis(mdb.showColx(data.group), data))


@app.route(f"{PREFIX}/structure")
def structure():
    local_stream = []
    groups = gdb.showCol()
    for group in groups:
        local_stream.append({'name': group.username, 'count': len(mdb.showColx(group.username))})
    json = flask.jsonify(local_stream)
    return json


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


# example of malahanobis
# x = np.array([[3.1, 7.5, 14.6]])
# mean = np.array([[3.1, 7.5, 14.6]])
# freq1 = []
# freq2 = []
# freq3 = []
#
# freq1.append(0.990099)
# freq1.append(6.93069)
# freq1.append(9.90099)
#
# freq2.append(19.0909)
# freq2.append(20.0)
# freq2.append(20.9091)
#
# freq3.append(8.64198)
# freq3.append(9.87654)
# freq3.append(11.1111)
#
# # treino = np.transpose(np.array([[2, 2, 3], [1, 3, 3], [1, 2, 4], [1, 3, 5]]))
# treino = [[3.1, 7.1, 14.2], [3.0, 7.3, 14.1], [3.2, 7.4, 14.5], [3.5, 7.9, 14.8]]
# print(treino)
# print(mean)
# print("Matrix de covariancia")
# print(np.cov(np.transpose(treino), bias=True))
# covariancia = np.cov(np.transpose(treino), bias=True)
# print("\n")
# print((x - mean))
# print(np.transpose((x - mean)))
# print(np.dot(x - mean, np.linalg.inv(covariancia)))
#
# print(np.dot(np.dot((x - mean), np.linalg.inv(covariancia)), np.transpose((x - mean))))

app.run(host="0.0.0.0", port="8080")  # change to port 80 on the server or use iptables, idk
