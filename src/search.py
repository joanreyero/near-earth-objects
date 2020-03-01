from collections import namedtuple
from enum import Enum
import operator as op
from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath
from datetime import datetime
from collections import defaultdict


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

        # Removing entries with None values to make parsing cleaner.
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        # Now, not all keys are in the dict, we need to check which ones are
        keys = kwargs.keys()
        if 'start_date' and 'end_date' in keys:
            self.date_search = Query.DateSearch(type=DateSearchType.between,
                                                values=[kwargs['start_date'],
                                                        kwargs['end_date']])
        else:
            self.date_search = Query.DateSearch(type=DateSearchType.equals,
                                                values=[kwargs['date']])

        self.return_object = Query.ReturnObjects[kwargs['return_object']]
        self.number = kwargs['number']

        if 'filter' in keys:
            self.filters = kwargs['filter']
        else:
            self.filters = []

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
                               number=self.number,
                               filters=self.filters)


class Filter(object):
    """
    Object representing optional filter options to be used in the date
    search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field
    to filter on a value.
    """
    Options = {
        'diameter': ('NearEarthObject', 'diam_min'),
        'is_hazardous': ('NearEarthObject', 'hazard'),
        'distance': ('OrbitPath', 'miss')
    }

    Operators = {
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        '>': op.ge,
        '<': op.le
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
    def _parse_filter(filter_str):
        """
        Parse a string filter.
        :param: filter_str:  a string representing the filter
        :returns: filter

        Diameter does not have a given value, but it is given as
        upper and lower bounfd.
        To play it safe if the operator is larger or equal the
        large diameter estimate will be used.
        Otherwise, the minimum diameter estimate.
        """
        field, oper, value = filter_str.split(':')
        return Filter(Filter.Options[field][1],
                      Filter.Options[field][0],
                      oper, value)

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format
                      ["filter_option:operation:value_of_option", ...]
        :return: list with key of NearEarthObject
                 or OrbitPath and value of empty list or list of Filters
        """
        return [Filter._parse_filter(filter_str) for
                filter_str in filter_options]

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        return list(filter(self._filter_p, results))

    def _filter_p(self, neo):
        # Converting the value from a string to something usable,
        # either int or bool
        try:
            value = float(self.value)
        except Exception:
            value = self.value == 'True'

        # Getting the operation to perform
        operation = Filter.Operators[self.operation]

        # If the filter applies to a NEO object:
        if self.object == 'NearEarthObject':
            return operation(getattr(neo, self.field), value)
        # If the filter applies to a OrbitPath object:
        else:
            # See if any of the orbit paths can work
            return any(operation(getattr(orbit, self.field), value)
                       for orbit in neo.orbits)


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects
    exposed by a generic search interface get_objects, which, based on the
    query specifications, determines how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances
        and their OrbitPath instances
        """
        self.db = db

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the
        QueryBuilder (query) calls the appropriate instance search function,
        then appliess any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of
        requested objects in the query.return_object specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """

        filters = Filter.create_filter_options(query.filters)

        # Get results of NEOs with required dates
        results = [neo for neo in self.db.db.values()
                   if NEOSearcher._date_match(neo.orbit_dates,
                                              query.date_search)]
        # Apply filters
        for filt in filters:
            results = filt.apply(results)

        if query.return_object == OrbitPath:
            return NEOSearcher._get_orbits(results, query.date_search)

        return results[:query.number]

    @staticmethod
    def _date_match(orbit_dates, date_search):
        """ Check if any date in a list of dates passes the date search
        :param: orbit_dates:  list of dates as string
        :param: date_search:  DateSearch namedtuple
        :returns: Bool
        """
        str_format = '%Y-%m-%d'
        # For between returns list of datetimes [start_date, end_date]
        # For equal simply [date]
        dates = list(map(lambda d: datetime.strptime(d, str_format),
                         date_search.values))
        if date_search.type == DateSearchType.between:
            # Check whether any date of the object is bwtween
            # the desired dates.
            return any(date >= dates[0] and date <= dates[1] for
                       date in orbit_dates)
        else:
            # Check whether any date of the object is the desired date
            return any(date == dates[0] for date in orbit_dates)

    @staticmethod
    def _get_orbits(results, date_search):
        """ For all NEOs, get the orbit with the required date. """
        return [orbit for neo in results for orbit in neo.orbits
                if NEOSearcher._date_match([orbit.orbit_date], date_search)]
