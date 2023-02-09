import datetime

# Alt Az is for altitude and azimuth coordinates (what we measure relative to the ground)
# ICRS is the "Equatorial"/"J2000" location and time agnostic coordinates
#  that you can compare to other stuff.
from astropy.coordinates import EarthLocation, SkyCoord, AltAz, ICRS
import astropy.coordinates

from astropy.time import Time
from astropy import units as u

def get_here():
    penn_state_harrisburg = EarthLocation(40.2042 * u.degree, lon=-(76.7452 * u.degree))
    return penn_state_harrisburg

def get_now():
    current_time = datetime.datetime.utcnow()
    return current_time

def altaz_to_equatorial_example():
    # For alt az, you need your observing location in latitude and longitude,
    #  the altitude and azimuth of your observed point,
    # and the time you made the observation.

    latitude = 50 * u.degree
    longitude = 100 * u.degree
    height = 38 * u.meter

    azimuth = 121 * u.degree + 43 * u.arcminute + 9 * u.arcsecond 
    altitude = 53 * u.degree + 15 * u.arcminute + 51 * u.arcsecond

    python_time = datetime.datetime(1980, 1, 1, 12, 0, 0)

    # Wrap your location and utc first.
    astropy_location = EarthLocation(lat=latitude, lon=longitude, height=height)
    astropy_time = Time(python_time, scale='utc', location=astropy_location)
    frame = AltAz(az=azimuth, alt=altitude, obstime=astropy_time, location=astropy_location)

    observation = frame.transform_to(ICRS)

    expected_radians = (2 * 3600 + 7 * 60 + 10) / (3600 * 24) * 360 * u.degree
    expected_declination = (23 * u.degree + 27 * u.arcminute + 48.4 * u.arcsecond)
    observed_radians = observation.ra
    observed_declination = observation.dec

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

if __name__ == '__main__':
    main()

