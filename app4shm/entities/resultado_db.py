class Resultado:
    def __init__(self, ident, timestamp_start, id_group):
        self.ident = ident  # primary key para a estrutura
        self.timestamp_start = timestamp_start
        self.id_group = id_group  # id do group como foreign key
