class DataPoint:
    def __init__(self, identifier, t, x, y, z, group, testing):
        self.identifier = str(identifier)
        self.t = float(t)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.group = str(group)
        self.testing = bool(testing)

    # eww snakecase
    def jsoner(self):
        return "{\"id\": \"" + self.identifier + "\", \"timeStamp\": " + str(self.t) + ", \"x\": " + str(self.x) + ", \"y\": " + str(self.y) + ", \"z\": " + str(self.z) + ", \"group\": \"" + self.group + ", \"testing\": \"" + str(self.testing) + "\"}"

    def to_string(self):
        return "ID: " + self.identifier + " | group: " + self.group + " | Timestamp: " + str(self.t) + " | X: " + str(self.x) + " | Y: " + str(self.y) + " | Z: " + str(self.z) + "\n"
