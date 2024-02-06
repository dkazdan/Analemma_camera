"""
Find eclipse times given lat/lon/elev
Uses JPL database
Adopted from https://stackoverflow.com/questions/75268690/using-astropy-to-generate-solar-eclipse-conditions-based-on-my-location
Started 29 January 2024
DK
"""

import numpy as np
import scipy.optimize
import astropy.units as u
import astropy.time
import astropy.constants
import astropy.coordinates


def distance_contact(
        location: astropy.coordinates.EarthLocation,
        time: astropy.time.Time,
        eclipse_type: str,
) -> u.Quantity:

    radius_sun = astropy.constants.R_sun
    radius_moon = 1737.4 * u.km

    coordinate_sun = astropy.coordinates.get_sun(time)
    coordinate_moon = astropy.coordinates.get_moon(time)

    frame_local = astropy.coordinates.AltAz(obstime=time, location=location)

    alt_az_sun = coordinate_sun.transform_to(frame_local)
    alt_az_moon = coordinate_moon.transform_to(frame_local)

    angular_radius_sun = np.arctan2(radius_sun, alt_az_sun.distance).to(u.deg)
    angular_radius_moon = np.arctan2(radius_moon, alt_az_moon.distance).to(u.deg)

    if eclipse_type == 'total':
        separation_max = angular_radius_moon - angular_radius_sun
    elif eclipse_type == 'partial':
        separation_max = angular_radius_moon + angular_radius_sun
    else:
        raise ValueError("Unknown eclipse type")

    return (alt_az_moon.separation(alt_az_sun).deg * u.deg) - separation_max


def calc_time_start(
        location: astropy.coordinates.EarthLocation,
        time_search_start: astropy.time.Time,
        time_search_stop: astropy.time.Time,
        eclipse_type: str = 'partial'
) -> astropy.time.Time:

    astropy.coordinates.solar_system_ephemeris.set("de430")

    # If we're only looking for a partial eclipse, we can accept a coarser search grid
    if eclipse_type == "partial":
        step = 1 * u.hr
    elif eclipse_type == "total":
        step = 1 * u.min
    else:
        raise ValueError("Unknown eclipse type")

    # Define a grid of times to search for eclipses
    time = astropy.time.Time(np.arange(time_search_start, time_search_stop, step=step))

    # Find the times that are during an eclipse
    mask_eclipse = distance_contact(location=location, time=time, eclipse_type=eclipse_type) < 0

    # Find the index of the first time that an eclipse is occuring
    index_start = np.argmax(mask_eclipse)

    # Search around that time to find when the eclipse actually starts
    time_eclipse_start = scipy.optimize.root_scalar(
        f=lambda t: distance_contact(location, astropy.time.Time(t, format="unix"), eclipse_type=eclipse_type).value,
        bracket=[time[index_start - 1].unix, time[index_start].unix],
    ).root
    time_eclipse_start = astropy.time.Time(time_eclipse_start, format="unix")

    return time_eclipse_start


def test_calc_time_start():

    location = astropy.coordinates.EarthLocation(lat=41.4940166 * u.deg, lon=-81.5803615 * u.deg, height=300 * u.m)
    eclipse_type = 'total'
    time_start = calc_time_start(
        location=location,
        time_search_start=astropy.time.Time.now(),
        time_search_stop=astropy.time.Time.now() + 0.9 * u.yr,
        eclipse_type=eclipse_type,
    )
    print(time_start.isot)
    
if __name__=="__main__":
    test_calc_time_start()