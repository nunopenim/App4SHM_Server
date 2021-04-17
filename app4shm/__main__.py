# App4SHM Initial Server Python Port
#
# Nuno Penim, Paulo Oliveira, 2021
#
# No tabs allowed for the safety of the entire project
# Use 4 spaces (I KNOW, BUT THAT'S HOW PYTHON ROLLS, I AM SORRY)

import flask
from app4shm.entities.data import Data

# Webstuff properties
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Data we get from the internet and management functions of such data
data_stream = []

def clear_stream():
    global data_stream
    data_stream = []

def sort_stream():
    global data_stream
    data_stream.sort()


# Webservice itself
@app.route('/', methods=['GET'])
def diag():
    return flask.render_template("diag.html")


app.run()
