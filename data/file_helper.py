import json
import os


class Helper(object):
    @staticmethod
    def add(entity, ref):
        Helper.exists(ref)
        if Helper.contains(entity, ref):
            return False
        data = Helper.read(ref)
        data[entity['name']] = entity
        with open(ref, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=True)
        return True

    @staticmethod
    def update(entity, ref):
        Helper.exists(ref)
        if Helper.contains(entity, ref):
            data = Helper.read(ref)
            data[entity['name']] = entity
            with open(ref, 'w') as outfile:
                json.dump(data, outfile, ensure_ascii=True)
            return True

        return False

    @staticmethod
    def read(ref):
        Helper.exists(ref)
        with open(ref) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def contains(entity, ref):
        Helper.exists(ref)
        data = Helper.read(ref)
        return entity['name'] in data

    @staticmethod
    def exists(ref):
        if not os.path.exists(ref):
            with open(ref, 'w+') as f:
                f.write('{}')
