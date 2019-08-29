class MapIndex:

    def __init__(self):
        self.mt = []
        self.map = {}
        self.index = {}

    def mapping(self, source, cities):
        self.mt = [[0 for i in range(len(cities))] for i in range(len(cities))]
        self.map = {}
        self.index = {}
        for i in range(len(cities)):
            self.map[i] = cities[i]
            self.index[cities[i]] = i

        for i in cities:
            for j in cities:
                self.mt[self.index_of(i)][self.index_of(j)] = source[i][j]

        return map

    def name_of(self, source):
        return self.map[source]

    def index_of(self, source):
        return self.index[source]

    def from_name(self, source, destination):
        return self.mt[self.index_of(source)][self.index_of(destination)]
