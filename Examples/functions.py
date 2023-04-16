import astropy
from sunpy.coordinates import get_body_heliographic_stonyhurst
from sunpy.coordinates import frames
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u

from skyfield.api import load
from astropy.time import Time

import astroquery.heasarc
from astroquery.heasarc import Heasarc, Conf


def plot_event_direction(time, event_coord1, event_coord2,frame):
    # todo : define this function
    # should plot the direction of the event in the sky in a polar HGS plot.
    obstime = Time(time)
    planet_list = ['venus', 'sun','earth']
    planet_coord = [get_body_heliographic_stonyhurst(
        this_planet, time=obstime) for this_planet in planet_list]
    if frame == 'helioprojective':
        event_coord = SkyCoord(event_coord1*u.arcsec, event_coord2*u.arcsec,rsun=6695700.0*u.km , frame=frame, observer='earth',obstime=obstime)
    else:
        event_coord = SkyCoord(event_coord1*u.arcsec, event_coord2*u.arcsec , frame=frame, observer='earth',obstime=obstime)
    event_coord = event_coord.transform_to(frames.HeliographicStonyhurst)
    plt.figure()
    plt.figure().add_subplot(projection='polar')
    for this_planet, this_coord in zip(planet_list, planet_coord):
        plt.plot(this_coord.lon.to('rad'), this_coord.radius, 'o', label=this_planet)
    plt.plot(event_coord.lon.to('rad'), event_coord.radius, 'o', label='event')
    plt.arrow(0,0,event_coord.lon.to('rad').value,event_coord.radius.value*10,lw=2)
    plt.legend(loc = 'upper right')
    plt.title('Event direction on {}'.format(obstime))
    plt.show()
    return 0
def get_venus_position(year,month,day,amount,delta_t):
    # todo : define this function
    # Create a timescale and initialise beggining time, amount of days and delta_t between positions wanted.
    ts = load.timescale()
    t = ts.utc(year, month, range(day,amount,delta_t))

    # Load the JPL ephemeris DE421 (covers 1900-2050).
    eph = load('de421.bsp')
    sun, earth, venus = eph['sun'], eph['earth'], eph['venus']

    # Compute the position of Venus in the ICRS frame.
    venus_positions = []
    venus_times = []
    for t in t:
        venus_pos = venus.at(t)
        ra, dec, distance = venus_pos.radec() 
        dec = dec.to(u.deg)
        ra = ra.to(u.deg)
        venus_times.append(t)
        c = SkyCoord(ra, dec, frame='icrs')
        venus_positions.append(c)  
    return venus_times,venus_positions




def get_scw_list(coord,radius,start_date,end_date ):
    Heasarc = astroquery.heasarc.Heasarc()
    Conf.server.set('https://www.isdc.unige.ch/browse/w3query.pl')
    R = Heasarc.query_region(
            coord,
            mission = 'integral_rev3_scw',
            radius=radius,
            time = start_date + ' .. ' + end_date,
            good_jemx = ">1000",
        )
    assert astroquery.__version__ >= '0.4.2.dev6611'

    #it means it's our fork
    assert 'isdc' in astroquery.heasarc.Conf.server.cfgtype

    return R
def plot_venus_position(venus_times,venus_positions):
    plt.figure()
    for this_time,this_position in zip(venus_times,venus_positions):
        plt.scatter(this_position.ra.to('deg'),this_position.dec.to('deg'),s=10,marker = 'o',color='red')
    plt.xlabel('RA')
    plt.ylabel('Dec')
    plt.title('Venus position in the sky between {} and the {} in the ICRS frame'.format(venus_times[0].utc_iso(), venus_times[-1].utc_iso()))
# def search_hek():
#     # todo : define this function
#     return 0
