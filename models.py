from enum import Enum


class Place:

    def __init__(self, geo_id: str, name: str):
        self.geo_id = geo_id
        self.name = name


class IncomeClass(Enum):
    HIGH_INCOME = 1
    MIDDLE_INCOME = 2
    LOW_INCOME = 3


class MetroArea(Place):

    def __init__(self, geo_id: str, name: str, medium_income: float):
        self.medium_income = medium_income
        super().__init__(geo_id, name)


class CensusTract:

    def __init__(self,
                 year: int,
                 geo_id: str,
                 medium_income: float):
        self.year = year
        self.geo_id = geo_id
        self.medium_income = medium_income
        self.adjacent_census_tracts = []
        self.income_class = None

    def __str__(self):
        return self.geo_id + ' with medium income: ' + str(self.medium_income) + '$'


class IncomeDataProcessingResult:

    def __init__(self,
                 place: Place,
                 census_tracts: [CensusTract],
                 metro_area: MetroArea):
        self.place: Place = place
        self.metro_area_name: str = metro_area.name
        self.metro_area_medium_income: float = metro_area.medium_income
        self.num_census_tracts: int = len(census_tracts)
        self.num_high_income_census_tracts: int = 0
        self.num_middle_income_census_tracts: int = 0
        self.num_low_income_census_tracts: int = 0
        self.cluster_index: float = 0
        self.random_cluster_index: float = 0
        self.highest_cluster_index: float = 0
        self.lowest_cluster_index: float = 0
        self.num_shared_borders: int = 0
        self.richest_census_tract: CensusTract = None
        self.poorest_census_tract: CensusTract = None
        self.medium_income_total: float = 0

    def __str__(self):
        return \
            'Income data evaluation results for ' + str(self.place.name) + \
            '\nMetro area: ' + self.metro_area_name + \
            ' with a medium income of ' + str(self.metro_area_medium_income) + '$' \
            '\n\nNumber of census tracts evaluated: ' + str(self.num_census_tracts) + \
            '\nNumber of high income census tracts: ' + str(self.num_high_income_census_tracts) + \
            '\nNumber of middle income census tracts: ' + str(self.num_middle_income_census_tracts) + \
            '\nNumber of low income census tracts: ' + str(self.num_low_income_census_tracts) + \
            '\n\nCluster Index: ' + str(self.cluster_index) + '%' + \
            '\nAverage cluster index with random income distribution: ' \
            + str(self.random_cluster_index) + '%' + \
            '\nHighest cluster index: ' + str(self.highest_cluster_index) + '%' + \
            '\nLowest cluster index: ' + str(self.lowest_cluster_index) + '%' +\
            '\n\nNumber of shared borders: ' + str(self.num_shared_borders) + \
            '\nRichest census tract: ' + str(self.richest_census_tract) + \
            '\nPoorest census tract: ' + str(self.poorest_census_tract) + \
            '\nTotal medium income: ' + str("%.2f" % self.medium_income_total) + '$'
