Redefined models.py


# models.py

Defined two models:

-   NearEarthObject and
-   OrbitalPath


## NearEarthObject

Attributes:

-   **`id`:** Identifier
-   **`name`:** name of the object (str)
-   **`orbits`:** list of orbits (list)
-   **`orbit_dates`:** list of orbit dates (list)
-   **`magnitude`:** magnitude of the object (float)
-   **`dim_min`:** minimum estimated diameter in km (float)
-   **`dim_max`:** maximum estimated diameter in km (float)
-   **`hazard`:** whether it is potentially hazardous (bool)

Functions:

-   **`update_orbits`:** ads an orbit path information to a NEO list of Orbits.
-   Print functions to output the `neo_id` (`print_neo_id`), `neo_name` (`print_neo_name`), `orbits` (`print_orbits`) and `orbit_dates` (`print_orbit_dates`).

-   Added `__str__` and `__repr__` methods.


## OrbitaPath

Attributes:

-   **`neo_name`:** name of the object the orbit corresponds to (str)
-   **`orbit_date`:** close approach date (datetime)
-   **`miss`:** miss distance in kilometers (float)

Functions

-   Print functions to output the `neo_ame` of the orbit's object (`print_neo_ame`), `miss` (`print_miss`) and `orbit_date` (`print_orbit_date`).
-   Added `__str__` and `__repr__` functions.
