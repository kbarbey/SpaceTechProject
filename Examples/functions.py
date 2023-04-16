import astropy
from sunpy.coordinates import get_body_heliographic_stonyhurst
from sunpy.coordinates import frames
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u

def plot_event_direction(time, event_coord1, event_coord2,frame):
    # todo : define this function
    # should plot the direction of the event in the sky in a polar HGS plot.
    obstime = astropy.time.Time(time)
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
# def get_venus_position(tin,tend):
#     # todo : define this function
#     return 0
# def get_scw_list(coord,radius,start_date,end_date ):
#     # todo : define this function
#     # should give a list of scw for every venus/jupiter position in that time interval
#     return 0
# def search_hek():
#     # todo : define this function
#     return 0
