from typing import Tuple
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from submodules.pytox.utils.decorators import validate_arguments


@validate_arguments
def compute_latitude_longitude(city: str) -> Tuple[float, float]:
    # Initialize the geolocator
    geolocator = Nominatim(user_agent='carsnatch-geo')

    # Get the latitude and longitude of the first city
    location1 = geolocator.geocode(city)
    if location1 is None:
        lat1, lon1 = None, None
    else:
        lat1, lon1 = location1.latitude, location1.longitude
    return lat1, lon1


@validate_arguments
def distance_2_cities(city1: Tuple[float, float],
                      city2: Tuple[float, float]) -> float:

    # City1: (latitude, longitude)
    # City2: (latitude, longitude)

    # Calculate the distance between the two points
    distance = geodesic(city1, city2).km

    #print(f"The distance between  {location1} and {location2} is {distance:.2f} km")
    return distance
