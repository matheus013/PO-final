import json
from random import randrange

from numpy.random import choice

from pyUFbr.baseuf import ufbr

from data.file_helper import Helper
from data.generator import MatrixLoad

MatrixLoad.cities = ufbr.list_cidades("AL")

mt = MatrixLoad.get_matrix(only_read=True)

nc = 30
n_car = 10

instance_cities = choice(MatrixLoad.cities, size=nc, replace=False).tolist()
instance_demand = choice(instance_cities, size=10, replace=True).tolist()

for i in range(10):
    filename = "instance" + str(i) + '.json'
    Helper.add({'name': filename, 'cities': json.dumps(instance_cities),
                'demand': json.dumps(instance_demand),
                'cars': [randrange(3, 20) for i in range(n_car)]}, filename)
