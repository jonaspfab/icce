from models import CensusTract, Place
from typing import Dict
import csv
import requests


def get_data(path: str, parameters: Dict):
    url = 'https://api.datausa.io/' + path

    if parameters:
        url += '?'
        for key, value in parameters.items():
            url += key + '=' + value + '&'
        url = url[:-1]

    response = requests.get(url)
    json = response.json()

    return json['data']


def get_name(geo_id: str) -> str:
    data = get_data('attrs/geo/' + geo_id, {})

    return data[0][1]


def get_census_tracts(geo_id: str) -> [CensusTract]:
    parameters = {
        'show': 'geo',
        'required': 'income',
        'sumlevel': 'tract',
        'year': 'latest',
        'where': 'geo:' + geo_id
    }

    census_tracts: [CensusTract] = []
    for census_tracts_json in get_data('api/', parameters):
        census_tract = CensusTract(census_tracts_json[0],
                                   census_tracts_json[1],
                                   census_tracts_json[2])

        if census_tract.medium_income is not None:
            census_tracts.append(census_tract)

    assign_adjacent_census_tracts(census_tracts)

    return census_tracts


def search_for_place(name: str) -> [Place]:
    parameters = {
        'q': name,
        'kind': 'geo'
    }

    data = get_data('attrs/search/', parameters)
    result: [Place] = []
    for geo in data:
        found_place = Place(geo[0], geo[4])
        result.append(found_place)

    return result


def get_medium_income(geo_id: str) -> float:
    parameters = {
        'show': 'geo',
        'required': 'income,income_moe',
        'sumlevel': 'all',
        'year': 'latest',
        'geo': geo_id
    }

    data = get_data('api/', parameters)

    return float(data[0][2])


def assign_adjacent_census_tracts(census_tracts: [CensusTract]):
    with open('./nlist_2010.csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in csv_reader:
            ctl: CensusTract = find_census_tract(row[0], census_tracts)
            ctr: CensusTract = find_census_tract(row[1], census_tracts)
            if ctl is not None and ctr is not None:
                ctl.adjacent_census_tracts.append(ctr)


def find_census_tract(geo_id: str, census_tracts: [CensusTract]):
    for census_tract in census_tracts:
        if geo_id in census_tract.geo_id:
            return census_tract

    return None
