class DataPoint:
    def __init__(self, identifier, z_freq1, z_freq2, z_freq3, group, testing):
        self.identifier = str(identifier)
        self.z_freq1 = float(z_freq1)
        self.z_freq2 = float(z_freq2)
        self.z_freq3 = float(z_freq3)
        self.group = str(group)
        self.testing = bool(testing)

    # eww snakecase
    def jsoner(self):
        return "{\"id\": \"" + self.identifier + "\", \"z_freq1\": " + str(self.z_freq1) + ", \"z_freq2\": " + str(self.z_freq2) + ", \"z_freq3\": " + str(self.z_freq3) + ", \"group\": \"" + self.group + ", \"testing\": \"" + str(self.testing) + "\"}"

    def to_string(self):
        return "ID: " + self.identifier + " | group: " + self.group + " | z_freq1: " + str(self.z_freq1) + " | z_freq2: " + str(self.z_freq2) + " | z_freq3: " + str(self.z_freq3) + "\n"
