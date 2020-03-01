class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    :param id: Identifier
    :param name: name of the object (str)
    :param orbits: list of orbits (list)
    :param orbit_dates: list of orbit dates (list)
    :param magnitude: magnitude of object (float)
    :param dim_min: minimum diamater in km (float)
    :param dim_max: maximum diameter im km (float)
    :param hazard: whether it is potentially hazardous (bool)
    """

    def __init__(self, **kwargs):
        """
        Init functon for NearEarthObjects
        :param kwargs:    dict of attributes about a given Near Earth Object,
        only a subset of attributes used
        """
        self.neo_id = kwargs['neo_id']
        self.name = kwargs['name']
        self.orbits = [OrbitPath(**kwargs), ]
        self.orbit_dates = [kwargs['orbit_date'], ]
        self.diam_min = kwargs['diam_min']
        self.diam_max = kwargs['diam_max']
        self.hazard = kwargs['hazard']

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """
        self.orbits.append(orbit)
        self.orbit_dates.append(orbit.orbit_date)

    def print_neo_id(self):
        return(self.neo_id)

    def print_name(self):
        return(self.name)

    def print_orbits(self):
        return([orbit.__str__() for orbit in self.orbits])

    def print_orbit_dates(self):
        return(self.orbit_dates)

    def __repr__(self):
        return {'name': self.name, 'id': self.neo_id}

    def __str__(self):
        return f'NEO: name = {self.name}, id = {self.neo_id}'


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    :param name: name of the object (str)
    :param orbit_date: close approach date (datetime)
    :param miss: miss distance in kilometers (float)
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit,
        only a subset of attributes used
        """
        self.name = kwargs['name']
        self.orbit_date = kwargs['orbit_date']
        self.miss = kwargs['miss']

    def print_name(self):
        print(self.name)

    def print_miss(self):
        return(self.miss)

    def print_orbit_date(self):
        return(self.orbit_date)

    def __repr__(self):
        orbit = f'Orbit on {self.orbit_date.strftime("%Y-%m-%d")}. '
        miss = f'Miss distance (km): {round(self.miss, 2)}'
        return orbit + miss

    def __str__(self):
        return f'Orbit on {self.orbit_date}. Miss distance (km)): {self.miss}'
