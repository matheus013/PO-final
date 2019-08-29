import json
from random import randrange

import pandas as pd
from tqdm import tqdm
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from data.file_helper import Helper


class MatrixLoad:
    cities = []
    data = {}

    @staticmethod
    def rand_city():
        return randrange(len(MatrixLoad.cities))

    @staticmethod
    def getStateName(coord):
        geo_locator = Nominatim()
        location = geo_locator.reverse(str(coord[0]) + ', ' + str(coord[1]))

        state = location.raw['address']['state']
        return state

    @staticmethod
    def loadCities(ul):
        json_name = 'coordinates.json'
        json_check_city = 'check_city.json'
        result = {}
        valid_cities = []
        geo_locator = Nominatim(user_agent="specify_your_app_name_here")

        geocode = RateLimiter(geo_locator.geocode, min_delay_seconds=1)

        for i in tqdm(MatrixLoad.cities, desc='getting coordinates'):
            if Helper.contains({'name': i}, json_name) or Helper.contains({'name': i}, json_check_city):
                check = Helper.read(json_check_city)
                if check[i]['state'] == ul:
                    valid_cities.append(i)
                    data = Helper.read(json_name)
                    result[i] = tuple(data[i]['coordinates'])

                continue

            partial_result = geocode(i)
            state = MatrixLoad.getStateName(partial_result[1])
            Helper.add({'name': i, 'state': state}, json_check_city)

            if state != ul:
                continue

            entity = {'name': i, 'coordinates': list(partial_result[1])}

            Helper.add(entity, json_name)

            valid_cities.append(i)
            result[i] = partial_result[1]
        MatrixLoad.cities = valid_cities
        return result

    @staticmethod
    def distance(origin, destination):
        return geodesic(origin, destination).km

    @staticmethod
    def get_matrix(only_read=False, ul='AL', uf=True):
        json_dist = 'dist.json'
        dist = {}
        df = MatrixLoad.loadCities(ul)
        for i in MatrixLoad.cities:
            if not (i in df):
                continue
            if not Helper.contains({'name': i}, json_dist):
                entity = {'name': i, 'dists': {}}
                Helper.add(entity, json_dist)

            dist[i] = {}

        if only_read:
            data = Helper.read(json_dist)
            for i in tqdm(MatrixLoad.cities, desc='calculating distances'):
                for j in MatrixLoad.cities:
                    dist[i][j] = data[i]['dists'][j]
            return dist

        for i in tqdm(MatrixLoad.cities, desc='calculating distances'):
            if not (i in df):
                continue
            for j in MatrixLoad.cities:
                if not (j in df):
                    continue
                data = Helper.read(json_dist)
                entity = {'name': i, 'dists': data[i]['dists']}
                if data[i]['dists'][j]:
                    dist[i][j] = data[i]['dists'][j]
                    continue
                dist[i][j] = MatrixLoad.distance(df[i], df[j])
                entity['dists'][j] = dist[i][j]
                Helper.update(entity, json_dist)

        MatrixLoad.data = dist

        return dist
