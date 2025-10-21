class DataModel:
    def __init__(self, content=None):
        self.content = content

    def read(self):
        return self.content


class Source(Data):
    pass


class Output(Data):
    pass
