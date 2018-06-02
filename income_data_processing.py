from models import IncomeClass, IncomeDataProcessingResult, MetroArea, CensusTract, Place
from random import random


def process_income_data(place: Place,
                        census_tracts: [CensusTract],
                        metro_area: MetroArea,
                        calculate_max_min_index: bool) -> IncomeDataProcessingResult:
    result: IncomeDataProcessingResult = IncomeDataProcessingResult(place, census_tracts, metro_area)

    assign_income_classes(census_tracts, metro_area, result)
    calculate_cluster_indices(census_tracts, result)
    if calculate_max_min_index:
        calculate_maximal_cluster_index(census_tracts, result)
        calculate_minimal_cluster_index(census_tracts, result)
    calculate_random_cluster_indices(census_tracts, result)
    calculate_additional_statistics(census_tracts, result)

    return result


def assign_income_classes(census_tracts: [CensusTract],
                          metro_area: MetroArea,
                          result: IncomeDataProcessingResult):
    result.num_high_income_census_tracts = 0
    result.num_middle_income_census_tracts = 0
    result.num_low_income_census_tracts = 0

    for census_tract in census_tracts:
        comparison: float = census_tract.medium_income / metro_area.medium_income * 100

        if comparison < 80:
            result.num_low_income_census_tracts += 1
            census_tract.income_class = IncomeClass.LOW_INCOME
        elif comparison < 125:
            result.num_middle_income_census_tracts += 1
            census_tract.income_class = IncomeClass.MIDDLE_INCOME
        else:
            result.num_high_income_census_tracts += 1
            census_tract.income_class = IncomeClass.HIGH_INCOME


def calculate_cluster_indices(census_tracts: [CensusTract], result: IncomeDataProcessingResult):
    result.cluster_index = calculate_cluster_index(census_tracts)


def calculate_maximal_cluster_index(census_tracts: [CensusTract], result: IncomeDataProcessingResult):
    original_index = calculate_cluster_index(census_tracts)
    result.highest_cluster_index = maximal_cluster_index_helper(census_tracts, original_index)


def maximal_cluster_index_helper(census_tracts: [CensusTract], original_index: float) -> float:
    for n1 in census_tracts:
        for n2 in census_tracts:
            switch_income_classes(n1, n2)
            new_index = calculate_cluster_index(census_tracts)
            if original_index < new_index:
                return maximal_cluster_index_helper(census_tracts, new_index)
            else:
                switch_income_classes(n1, n2)

    return original_index


def calculate_minimal_cluster_index(census_tracts: [CensusTract], result: IncomeDataProcessingResult):
    original_index = calculate_cluster_index(census_tracts)
    result.lowest_cluster_index = minimal_cluster_index_helper(census_tracts, original_index)


def minimal_cluster_index_helper(census_tracts: [CensusTract], original_index: float) -> float:
    for n1 in census_tracts:
        for n2 in census_tracts:
            switch_income_classes(n1, n2)
            new_index = calculate_cluster_index(census_tracts)
            if original_index > new_index:
                return minimal_cluster_index_helper(census_tracts, new_index)
            else:
                switch_income_classes(n1, n2)

    return original_index


def switch_income_classes(n1: CensusTract, n2: CensusTract):
    cached_income_class = n1.income_class
    n1.income_class = n2.income_class
    n2.income_class = cached_income_class


def calculate_random_cluster_indices(census_tracts: [CensusTract], result: IncomeDataProcessingResult):
    total_high = result.num_high_income_census_tracts
    total_middle = result.num_middle_income_census_tracts
    total_low = result.num_low_income_census_tracts
    total = total_high + total_middle + total_low

    index_sum = 0
    num_tries = 10000

    for i in range(num_tries):
        remaining_high = total_high
        remaining_middle = total_middle
        remaining_low = total_low

        for census_tract in census_tracts:
            income_class_found: bool = False
            while not income_class_found:
                random_number = random() * total
                income_class_found = True

                if random_number < total_low and remaining_low > 0:
                    remaining_low -= 1
                    census_tract.income_class = IncomeClass.LOW_INCOME
                elif random_number < total_low + total_middle and remaining_middle > 0:
                    remaining_middle -= 1
                    census_tract.income_class = IncomeClass.MIDDLE_INCOME
                elif remaining_high > 0:
                    remaining_high -= 1
                    census_tract.income_class = IncomeClass.HIGH_INCOME
                else:
                    income_class_found = False

        index = calculate_cluster_index(census_tracts)
        index_sum += index

    result.random_cluster_index = index_sum / num_tries


def calculate_cluster_index(census_tracts: [CensusTract]) -> float:
    counter_same = 0
    counter_total = 0

    for census_tract in census_tracts:
        for adjacent_census_tract in census_tract.adjacent_census_tracts:
            counter_total += 1
            counter_same += 1 if adjacent_census_tract.income_class == census_tract.income_class else 0

    return (counter_same / counter_total) * 100


def calculate_additional_statistics(census_tracts: [CensusTract],
                                    result: IncomeDataProcessingResult):
    num_adjacent_census_tracts: int = 0
    total_income: float = 0
    richest_census_tract: CensusTract = None
    poorest_census_tract: CensusTract = None

    for census_tract in census_tracts:
        if richest_census_tract is None or richest_census_tract.medium_income < census_tract.medium_income:
            richest_census_tract = census_tract
        if poorest_census_tract is None or poorest_census_tract.medium_income > census_tract.medium_income:
            poorest_census_tract = census_tract

        num_adjacent_census_tracts += len(census_tract.adjacent_census_tracts)
        total_income += census_tract.medium_income

    result.num_shared_borders = num_adjacent_census_tracts / 2
    result.richest_census_tract = richest_census_tract
    result.poorest_census_tract = poorest_census_tract
    result.medium_income_total = total_income / len(census_tracts)
