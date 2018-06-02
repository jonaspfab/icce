from income_data_processing import process_income_data
from datausa import get_census_tracts, search_for_place, get_medium_income
from models import MetroArea, Place
import os


def main():
    place = request_place('Metro area')
    medium_income = get_medium_income(place.geo_id)
    metro_area = MetroArea(place.geo_id, place.name, medium_income)
    place = request_place('Place')
    calculate_max_min_index = request_answer('Do you want to calculate the max/min cluster index?')

    print('Fetching census tract data...', end='', flush=True)
    census_tracts = get_census_tracts(place.geo_id)
    print('Done')

    print('Processing income data...', end='', flush=True)
    result = process_income_data(place,
                                 census_tracts,
                                 metro_area,
                                 calculate_max_min_index)
    print('Done')

    result_file_name = get_result_file_name(place)
    with open(result_file_name, 'w+') as result_file:
        result_file.write(str(result))

    os.system('open ' + result_file_name)


def request_place(description: str) -> Place:
    possible_places: [Place] = search_for_place(input(description + ' name: '))
    for i in range(0, len(possible_places) - 1):
        possible_place = possible_places[i]
        print(str(i) + ': ' + possible_place.geo_id + ', ' + possible_place.name)

    while True:
        try:
            user_input = input('Indicate which place is the correct one (Type \'none\' for none of the above): ')
            if user_input == 'none':
                return request_place(description)

            i = int(user_input)
            if i < 0 or i >= len(possible_places):
                raise ValueError

            return possible_places[i]
        except ValueError:
            print('Invalid input')


def request_answer(question: str) -> bool:
    while True:
        answer = input(question + ' (y/n): ')
        if answer != 'y' and answer != 'n':
            print('Invalid input')
        else:
            return answer == 'y'


def get_result_file_name(place: Place) -> str:
    directory = './results/'
    formatted_name = place.name.lower().replace(' ', '_').replace(',', '')
    extension = '.txt'

    if not os.path.isdir(directory):
        os.makedirs(directory)

    os.system('open ' + directory)

    return directory + formatted_name + extension


if __name__ == "__main__":
    main()
