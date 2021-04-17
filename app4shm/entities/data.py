class Data:
    def __init__(self, identifier, timestamp, x, y, z, group):
        self.identifier = str(identifier)
        self.timestamp = int(timestamp)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.group = str(group)

    # eww snakecase
    def jsoner(self):
        return "{\"id\": \"" + self.identifier + "\", \"timeStamp\": " + str(self.timestamp) + ", \"x\": " + str(self.x) + ", \"y\": " + str(self.y) + ", \"z\": " + str(self.z) + ", \"group\": \"" + self.group + "\"}"

    def to_string(self):
        return "ID: " + self.identifier + " | group: " + self.group + " | Timestamp: " + str(self.timestamp) + " | X: " + str(self.x) + " | Y: " + str(self.y) + " | Z: " + str(self.z) + "\n"
