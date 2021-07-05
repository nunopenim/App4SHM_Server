class Medicao:
    def __init__(self, identifier, timestamp, x, y, z, group, resultado_id):
        self.identifier = str(identifier)
        self.timestamp = int(timestamp)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.resultado_id = resultado_id
        self.group = str(group)
