from collections import namedtuple
from enum import Enum

from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath
from datetime import datetime


class DateSearchType(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearchType))


class Query(object):
    """
    Object representing the desired search query operation to build.
    The Query uses the Selectors to structure the query information
    into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search', 'number',
                                         'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine
        which SearchOperation query to use
        """
        if kwargs['start_date'] and kwargs['end_date']:
            self.date_search = Query.DateSearch(type=DateSearchType.between,
                                                values=[kwargs['start_date'],
                                                        kwargs['end_date']])
        elif kwargs['date']:
            self.date_search = Query.DateSearch(type=DateSearchType.equals,
                                                values=[kwargs['date']])

        self.return_object = Query.ReturnObjects[kwargs['return_object']]
        self.number = kwargs['number']


    def build_query(self):
        """
        Transforms the provided query options, set upon initialization,
        into a set of Selectors that the NEOSearcher can use to perform
        the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict
        of query options into a SearchOperation
        """
        return Query.Selectors(date_search=self.date_search,
                               return_object=self.return_object,
                               number=self.number, filters=[])


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
    }

    Operators = {
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """

        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        ds = {}
        found = 0
        # While we have not found yet enough objects
        for neo_name, neo in self.db.db.items():
            if found >= query.number: break
            date_match = NEOSearcher.date_match(neo, query.date_search)
            if date_match:
                ds[neo_name] = NEOSearcher.get_object(neo, date_match,
                                                      query.return_object)
                print(neo.orbit_dates)
                found += 1
        return ds
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors

    @staticmethod
    def date_match(neo, date_search):
        str_format = '%Y-%m-%d'
        dates = list(map(lambda d: datetime.strptime(d, str_format),
                    date_search.values))
        if date_search.type == DateSearchType.between:
            # Check whether any date of the object is bwtween
            # the desired dates.
            for date in neo.orbit_dates:
                if date >= dates[0] and date <= dates[1]:
                    return date
        else:
            # Check whether any date of the object is the desired date
            for date in neo.orbit_dates:
                if date == dates[0]:
                    return date
        return False

    @staticmethod
    def get_object(neo, date, return_object):
        if neo is return_object:
            return neo
        else:
            for orbit in neo.orbits:
                if orbit.orbit_date == date:
                    return orbit
