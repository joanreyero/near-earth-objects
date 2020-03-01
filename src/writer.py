from models import NearEarthObject, OrbitPath
from enum import Enum
import csv


class OutputFormat(Enum):
    """
    Enum representing supported output formatting options for search
    results.
    """
    display = 'display'
    csv_file = 'csv_file'

    @staticmethod
    def list():
        """
        :return: list of string representations of OutputFormat enums
        """
        return list(map(lambda output: output.value, OutputFormat))


class NEOWriter(object):
    """
    Python object use to write the results from supported output
    formatting options.
    """

    def __init__(self):
        pass

    def write(self, format, data, **kwargs):
        """
        Generic write interface that, depending on the OutputFormat
        selected calls the appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for
                       formatting output e.g. filename
        :return: bool representing if write successful or not
        """
        # Boolean variable to see if the data contains NEOs or OrbitPaths
        neo_p = type(data[0]) == NearEarthObject

        if OutputFormat(format) == OutputFormat.display:
            if neo_p:  # If it is NEOs
                return NEOWriter._write_neo_display(data)
            else:  # If it is Orbit Paths
                return NEOWriter._write_orbit_display(data)
        elif OutputFormat(format) == OutputFormat.csv_file:
            if neo_p:  # If it is NEOs
                return NEOWriter._write_neo_csv(data, **kwargs)
            else:  # If it is Orbit Paths
                return NEOWriter._write_orbit_csv(data, **kwargs)

    @staticmethod
    def _write_neo_display(data):
        if not data:
            print('No objects found')
        for neo in data:
            id_name = f'ID: {neo.neo_id}, Name: {neo.name}, '
            orbits = f'Orbits: {neo.orbits}, '
            dates = f'Orbit dates: {NEOWriter._dates_to_str(neo.orbit_dates)}'
            print(id_name + orbits + dates)
        return True

    @staticmethod
    def _dates_to_str(dates):
        return list(map(lambda d: d.strftime('%Y-%m-%d'), dates))

    @staticmethod
    def _write_orbit_display(data):
        if not data:
            print('No objects found')
        for orbit in data:
            name = f'Name: {orbit.name}, '
            miss = f'Miss ditance (km): {round(orbit.miss, 2)}, '
            date = f'Date: {NEOWriter._dates_to_str([orbit.orbit_date])[0]}'
            print(name + miss + date)
        return True

    @staticmethod
    def _write_neo_csv(data, **kwargs):
        if 'filename' in kwargs.keys():
            filename = kwargs['filename']
        else:
            filename = 'neo.csv'
        out = 'out/' + filename

        with open(out, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            # Writing headers
            writer.writerow(['ID', 'Name', 'Orbits', 'Orbit dates'])
            for neo in data:
                writer.writerow([neo.neo_id, neo.name, neo.orbits,
                                 NEOWriter._dates_to_str(neo.orbit_dates)])
        return True

    @staticmethod
    def _write_orbit_csv(data, **kwargs):
        if 'filename' in kwargs.keys():
            filename = kwargs['filename']
        else:
            filename = 'orbit.csv'
        out = 'out/' + filename

        with open(out, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            # Writing headers
            writer.writerow(['Name', 'Miss distance (km)', 'Orbit date'])
            for orbit in data:
                writer.writerow([orbit.name, round(orbit.miss, 2),
                                 NEOWriter._dates_to_str(
                                     [orbit.orbit_date])[0]])
        return True
