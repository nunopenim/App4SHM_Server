class Data:
    def __init__(self, identifier, timestamp, x, y, z, group):
        self.identifier = str(identifier)
        self.timestamp = int(timestamp)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.group = str(group)

    # eww snakecase
    def to_string(self):
        return "{\"id\": \"" + self.identifier + "\", \"timeStamp\": " + str(self.timestamp) + ", \"x\": " + str(self.x) + ", \"y\": " + str(self.y) + ", \"z\": " + str(self.z) + ", \"group\": \"" + self.group + "\"}"
