# App4SHM Initial Server Python Port
#
# Nuno Penim, Paulo Oliveira, 2021
#
# No tabs allowed for the safety of the entire project
# Use 4 spaces as indentation (I KNOW, BUT THAT'S HOW PYTHON ROLLS, I AM SORRY)

import flask
import operator

from app4shm.entities.data import Data

# Webstuff properties
app = flask.Flask(__name__)
app.config["DEBUG"] = False

# datastream and operations on it
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
def recieve():
    recieved = flask.request.get_json()
    for i in recieved:
        data = Data(identifier=i['id'], timestamp=int(i['timeStamp']), x=float(i['x']), y=float(i['y']), z=float(i['z']), group=i['group'])
        push_to_stream(data)
    sort_stream()
    return ""

app.run(host="0.0.0.0", port="8080")  # change to port 80 on the server or use iptables, idk
