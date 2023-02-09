import datetime

from astropy.coordinates import EarthLocation, SkyCoord, AltAz, TEME, ICRS#, TETE
import astropy.coordinates
# Coordinate systems as described here:
# https://docs.astropy.org/en/stable/coordinates/index.html
# TEME: A coordinate or frame in the True Equator Mean Equinox frame (TEME).
# TETE: An equatorial coordinate or frame using the True Equator and True Equinox (TETE).
# I don't know the difference, but I guess one of them is what you want?
# TETE is not available in my version of astropy so we'll go with TEME.

from astropy.time import Time
from astropy import units as u

def get_here():
    penn_state_harrisburg = EarthLocation(40.2042 * u.degree, lon=-(76.7452 * u.degree))
    return penn_state_harrisburg

def get_now():
    current_time = datetime.datetime.utcnow()
    return current_time

def get_coordinate_systems():
    all_attributes = (getattr(astropy.coordinates, attribute_name) for attribute_name in dir(astropy.coordinates))
    frame_type = type(AltAz)
    return [attribute for attribute in all_attributes if type(attribute) == frame_type]
    
def local_sidereal_time(time_utc, earth_location):
    observing_time = Time(time_utc, scale='utc', location=observing_location)
    return observing_time.sidereal_time('mean')

def utc_to_sidereal_example():
    # Approximately matches the example numbers here:
    # https://phys.libretexts.org/Bookshelves/Astronomy__Cosmology/Celestial_Mechanics_(Tatum)/06%3A_The_Celestial_Sphere/6.04%3A_Conversion_Between_Equatorial_and_Altazimuth_Coordinates

    # The numbers are off by 2 "minutes" I think because they were calculating from an almanac,
    #  and maybe also because we're using the "mean" sidereal time, whatever that is.
    victoria_canada = EarthLocation(lat=48.4284 * u.degree, lon=-(123 * u.degree + 25 * u.arcminute))

    example_time = datetime.datetime(2002, 11, 24, 22, 0, 0)
    example_time = example_time + datetime.timedelta(hours=8) # adjust time zone manually

    lst = local_sidereal_time(example_time, victoria_canada)
    print('Example sidereal time at Victoria in 2002:', lst)

#ICRS_STELLARIUM_RADIANS_OFFSET = 75.70248806714645 * u.degree
#ICRS_STELLARIUM_DECLINATION_OFFEST = 0.06576016939274254 * u.degree
ICRS_STELLARIUM_RADIANS_OFFSET = 0 * u.degree
ICRS_STELLARIUM_DECLINATION_OFFEST = 0 * u.degree
def altaz_to_equatorial_example():
    # Example values were taken from the program "stellarium"
    #  which is really nifty; I like it a lot.
    # For alt az, you need your observing location in latitude and longitude,
    #  the altitude and azimuth of your observed point,
    # and the time you made the observation.

    #latitude = 25 * u.degree
    #longitude = 25 * u.degree
    latitude = 50 * u.degree
    longitude = 100 * u.degree
    height = 38 * u.meter

    #azimuth = 239 * u.degree + 41 * u.arcminute + 44 * u.arcsecond 
    #altitude = 22 * u.degree + 24 * u.arcminute + 48 * u.arcsecond
    azimuth = 121 * u.degree + 43 * u.arcminute + 9 * u.arcsecond 
    altitude = 53 * u.degree + 15 * u.arcminute + 51 * u.arcsecond

    #python_time = datetime.datetime(2023, 1, 1, 12, 0, 0)
    python_time = datetime.datetime(1980, 1, 1, 12, 0, 0)

    # Wrap your location and utc first.
    astropy_location = EarthLocation(lat=latitude, lon=longitude, height=height)
    astropy_time = Time(python_time, scale='utc', location=astropy_location)
    frame = AltAz(az=azimuth, alt=altitude, obstime=astropy_time, location=astropy_location)

    observation = frame.transform_to(ICRS)

    #expected_radians = (21 * 3600 + 41 * 60 + 55) / (3600 * 24) * 360 * u.degree
    #expected_declination = -(15 * u.degree + 11 * u.arcminute + 16 * u.arcsecond)
    expected_radians = (2 * 3600 + 7 * 60 + 10) / (3600 * 24) * 360 * u.degree
    expected_declination = (23 * u.degree + 27 * u.arcminute + 48.4 * u.arcsecond)
    observed_radians = observation.ra + ICRS_STELLARIUM_RADIANS_OFFSET
    observed_declination = observation.dec - ICRS_STELLARIUM_DECLINATION_OFFEST

    print(expected_radians, expected_declination)
    print(observed_radians, observed_declination)

    print('Error:')
    print((observed_radians - expected_radians) / u.degree)
    print((observed_declination - expected_declination) / u.degree)

    return (observed_radians, observed_declination)

def degree_to_hms(n):
    n = n.value
    degrees_per_hour = 360 / 24
    degrees_per_minute = degrees_per_hour / 60
    degrees_per_second = degrees_per_minute / 60

    hours, remainder = divmod(n, degrees_per_hour)
    minutes, remainder = divmod(remainder, degrees_per_minute)
    seconds = remainder / degrees_per_second
    return '{}h{}m{}s'.format(hours, minutes, round(seconds, 2))

def main():
    #altaz_to_equatorial_example()
    import json
    with open('data.txt') as file_in:
        test_data = json.load(file_in)
    for sample in test_data:
        print('Test for {}.'.format(sample['name']))

        location = EarthLocation(lat=sample['latitude'], lon=sample['longitude'], height=sample['height'])
        time = Time(sample['time'], scale='utc', location=location)
        frame = AltAz(az=sample['az'], alt=sample['alt'], obstime=time, location=location)
        
        observation = frame.transform_to(ICRS)
        print(observation)
        print(degree_to_hms(observation.ra), observation.dec)
        print(sample['ra'], sample['de'])

        #units_example()

if __name__ == '__main__':
    main()

