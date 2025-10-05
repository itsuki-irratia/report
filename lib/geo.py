import os
import json
import requests

script_folder  = os.path.dirname(os.path.abspath(__file__))
geo_cache_file = f"{script_folder}/geo.cache.json"

class Geo:

    @staticmethod
    def get(ip):
        _geo = Geo.getCache(ip)
        if _geo != False:
            return _geo

        url = f"http://ip-api.com/json/{ip}"
        try:
            res = requests.get(url).json()

            if res['status'] != 'success':
                return {}
            
            keys_to_remove = ['status', 'district', 'currency', 'isp', 'org', 'as', 'asname', 'mobile', 'proxy', 'hosting', 'query']

            for key in keys_to_remove:
                res.pop(key, None)

            if res['regionName'] in ['Navarre', 'Basque Country']:
                res['country'] = 'Euskal Herria'
                res['countryCode'] = 'EH'
            
            if res['regionName'] == 'Navarre':
                res['regionName'] = 'Nafarroa'

            if res['regionName'] == 'Basque Country':
                res['regionName'] = 'Euskal Autonomi Erkidegoa'

            Geo.setCache(ip, res)

            return res
        except Exception as e:
            return get(ip)

    @staticmethod
    def getCacheFile():
        with open(geo_cache_file, "r") as f:
            j = json.loads(f.read())
        return j

    @staticmethod
    def getCache(ip):
        j = Geo.getCacheFile()
        if ip in j:
            return j[ip]
        else:
            return False

    @staticmethod
    def setCache(ip, res):
        try:
            j = Geo.getCacheFile()
            j[ip] = res

            with open(geo_cache_file, "w") as f:
                json.dump(j, f, indent=4)
            return True
        except Exception as e:
            return False

    @staticmethod
    def getCities(logs):
        ips  = []
        geos = {}
        for log in logs:
            if log['remote_ip'] in ips:
                continue
            else:
                ips.append(log['remote_ip'])

            if 'city' in log['geo']:
                key = f"{log['geo']['city']} / {log['geo']['regionName']} / {log['geo']['country']}"
                if key in geos:
                    geos[key] = geos[key] + 1
                else:
                    geos[key] = 1
            else:
                if '-' in geos:
                    geos['-'] = geos['-'] + 1
                else:
                    geos['-'] = 1

        return geos

    @staticmethod
    def getRegions(logs):
        ips  = []
        geos = {}
        for log in logs:
            if log['remote_ip'] in ips:
                continue
            else:
                ips.append(log['remote_ip'])

            if 'regionName' in log['geo']:
                key = f"{log['geo']['regionName']} / {log['geo']['country']}"
                if key in geos:
                    geos[key] = geos[key] + 1
                else:
                    geos[key] = 1
            else:
                if '-' in geos:
                    geos['-'] = geos['-'] + 1
                else:
                    geos['-'] = 1

        return geos

    @staticmethod
    def getCountries(logs):
        ips  = []
        geos = {}
        for log in logs:
            if log['remote_ip'] in ips:
                continue
            else:
                ips.append(log['remote_ip'])

            if 'country' in log['geo']:
                key = f"{log['geo']['country']}"
                if key in geos:
                    geos[key] = geos[key] + 1
                else:
                    geos[key] = 1
            else:
                if '-' in geos:
                    geos['-'] = geos['-'] + 1
                else:
                    geos['-'] = 1

        return geos