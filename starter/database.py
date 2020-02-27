import csv
from models import OrbitPath, NearEarthObject


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all
    orbit date paths to the Near Earth Objects recorded on a given
    day is maintained. Additionally, all unique instances of
    a Near Earth Object are contained in a dict mapping the
    Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the
        filename containing the Near Earth Object data
        """
        self.filename = filename
        self.db = {}

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects
        and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single
             instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename
        # Using a set to check whether a NEO is in the DB
        # to check memebership in O(1).
        checked_names = set()
        db = {}

        with open(filename, newline='') as csvfile:
            # Read CSV
            neo_data = csv.reader(csvfile, delimiter=',')

            for row in neo_data:
                neo_name = row[2]  # Extract name to check membership.
                # Get the relevant elements
                args = {'neo_id': row[0],
                          'neo_name': neo_name,
                          'magnitude': row[4],
                          'diam_min': row[5],
                          'diam_max': row[6],
                          'hazard': row[13],
                          'orbit_date': row[17],
                          'miss': row[21]}

                # If this object is already in the DB
                if neo_name in checked_names:
                    # Make a new Orbit Object
                    orbit = OrbitPath(**args)
                    # and update the orbits with the Object.
                    db[neo_name].update_orbits(orbit)

                else:
                    # Add the name to the set
                    checked_names.add(neo_name)
                    # and create the NEO
                    db[neo_name] = NearEarthObject(**args)

        self.db = db
        return None
