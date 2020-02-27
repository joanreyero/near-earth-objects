class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    :param id: Identifier
    :param name: name of the object (str)
    :param orbits: list of orbits (list)
    :param orbit_dates: list of orbit dates (list)
    """

    def __init__(self, **kwargs):
        """
        Init functon for NearEarthObjects
        :param kwargs:    dict of attributes about a given Near Earth Object,
        only a subset of attributes used
        """
        self.neo_id = kwargs['id']
        self.neo_name = kwargs['name']
        self.orbits = kwargs['orbits']
        self.orbit_dates = kwargs['orbit_dates']

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """
        self.orbits.append(orbit)
        self.orbit_dates.append(orbit.orbit_date)


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
        self.neo_name = kwargs['name']
        self.orbit_date = kwargs['orbit_date']
        self.miss = kwargs['miss']
