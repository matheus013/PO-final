from pandas import DataFrame

from data.file_helper import Helper


class Reader:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        r = Helper.read(self.filename)
        return r
