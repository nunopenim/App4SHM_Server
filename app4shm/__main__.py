# App4SHM Server - Main script
#
# In here, all the data stream related and webservice related functions are present
#
# Nuno Penim, Paulo Oliveira, 2021
#
# No tabs allowed for the safety of the entire project
# Use 4 spaces as indentation (I KNOW, BUT THAT'S HOW PYTHON ROLLS, I AM SORRY)

import flask
import operator
import app4shm.typewriter as tw
from app4shm.entities.data import Data
import os

ZIP_FILE = "../deliverable.zip"

# Web Service properties
app = flask.Flask(__name__)
app.config["DEBUG"] = False

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


# Webservice itself
@app.route('/diag')
def legacy():
    """
    This is just a legacy method, just to redirect people to the new page, in the root, just in case
    someone is evaluating our report and the server looks "dead". Expect it to be removed in future
    iterations of the project
    """
    return flask.redirect(flask.url_for('diag'))


@app.route('/', methods=['GET'])
def diag():
    datalist = ""
    for i in data_stream:
        datalist += i.to_string()
    return flask.render_template("diag.html", datalist=datalist)


@app.route('/cleanup')
def cleanup():
    clear_stream()
    return flask.redirect(flask.url_for('diag'))


@app.route('/data/reading', methods=['POST'])
def receive():
    received = flask.request.get_json()
    for i in received:
        data = Data(identifier=i['id'],
                    timestamp=int(i['timeStamp']),
                    x=float(i['x']),
                    y=float(i['y']),
                    z=float(i['z']),
                    group=i['group'])
        push_to_stream(data)
    sort_stream()
    return ""

@app.route('/generate')
def write_files():
    global data_stream
    os.remove(ZIP_FILE)
    dict = {}
    for i in data_stream:
        key = i.identifier
        if dict.get(key) == None:
            dict[key] = []
        dict[key].append(i)
    for i in dict.keys():
        tw.data_stream_to_buffer(dict[i])
        tw.buffer_to_file(i)
    tw.zip_file()
    return flask.send_file(ZIP_FILE, "deliverable.zip")

app.run(host="0.0.0.0", port="8080")  # change to port 80 on the server or use iptables, idk
