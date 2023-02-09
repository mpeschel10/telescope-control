import datetime

# AltAz is the "frame" for altitude and azimuth coordinates (what we measure relative to the ground)
# ICRS is the "Equatorial"/"J2000" location and time agnostic coordinates that we need
from astropy.coordinates import EarthLocation, SkyCoord, AltAz, ICRS

from astropy.time import Time
from astropy import units as u

def get_here():
    penn_state_harrisburg = EarthLocation(40.2042 * u.degree, lon=-(76.7452 * u.degree))
    return penn_state_harrisburg

def get_now():
    current_time = datetime.datetime.utcnow()
    return current_time

def sirius_alt_az_to_equatorial_example():
    print('Computing the location of Sirius...')
    # For alt az, you need your observing location in latitude and longitude,
    #  the altitude and azimuth of your observed point,
    #  and the time you made the observation.

    # Sirius, as observed from Paris, France using Stellarium
    latitude = 48 * u.degree + 51 * u.arcminute + 36 * u.arcsecond
    longitude = 2 * u.degree + 20 * u.arcminute + 24 * u.arcsecond
    # Setting the height may be incorrect; astropy tries to approximate altitude internally (I think) and writing in the height manually may introduce a small error.
    # It's below one arcsecond for the Sirius-Paris example; idk if it matters.
    height = 38 * u.meter 

    azimuth = 208 * u.degree +  9 * u.arcminute + 59 * u.arcsecond 
    altitude = 19 * u.degree + 57 * u.arcminute +  8 * u.arcsecond

    python_time = datetime.datetime(2023, 2, 8, 23, 12, 1)

    # Wrap your location and utc first.
    astropy_location = EarthLocation(lat=latitude, lon=longitude, height=height)
    astropy_time = Time(python_time, scale='utc')
    frame = AltAz(az=azimuth, alt=altitude, obstime=astropy_time, location=astropy_location)

    observation = frame.transform_to(ICRS)

    # Expected right ascension and declination are from wikipedia
    expected_right_ascension = (6 * 3600 + 45 * 60 + 8.917) / (3600 * 24) * 360 * u.degree
    expected_declination = -(16 * u.degree + 42 * u.arcminute + 58.02 * u.arcsecond)

    print('Expected: ', expected_right_ascension, expected_declination)
    print('Observed: ', observation.ra, observation.dec)

    print('Error:')
    print(observation.ra - expected_right_ascension)
    print(observation.dec - expected_declination)

def main():
    sirius_alt_az_to_equatorial_example()

if __name__ == '__main__':
    main()

