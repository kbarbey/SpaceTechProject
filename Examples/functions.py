import astropy
from sunpy.coordinates import get_body_heliographic_stonyhurst
from sunpy.coordinates import frames
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.table import Table

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
    plt.title('Venus position in the sky between {} and the {} in the ICRS frame'.format(venus_times[0].utc_strftime(), venus_times[-1].utc_strftime()))
def login():
    import getpass
    token = getpass.getpass('insert your token: ')
    import oda_api.token
    oda_api.token.decode_oda_token(token)
    import logging
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger('oda_api').addHandler(logging.StreamHandler())
    return token
def query_jemx_from_table(table,e1,e2,token):
    scw_list = []
    for i in range(len(table)):
        scw_list.append(str(table['SCW_ID'][i])+'.'+str(table['SCW_VER'][i]))
    from oda_api.api import DispatcherAPI

    disp = DispatcherAPI(url="https://www.astro.unige.ch/mmoda/dispatch-data", instrument="mock")
    for scw in scw_list:
        par_dict = {
        "E1_keV": e1,
        "E2_keV": e2,
        "detection_threshold": "5",
        "instrument": "jemx",
        "osa_version": "OSA11.2",
        "product": "jemx_image",
        "product_type": "Real",
        "scw_list": [scw],
        "integral_data_rights": "all-private",#all-private or public
        "token": token
        }

        data_collection = disp.get_product(**par_dict)
        data_collection.mosaic_image_0_mosaic.write_fits_file(str(scw)+'.fits',overwrite=True)
def query_jemx_from_scw(scw,e1,e2,token):
    from oda_api.api import DispatcherAPI
    disp = DispatcherAPI(url="https://www.astro.unige.ch/mmoda/dispatch-data", instrument="mock")
    par_dict = {
    "E1_keV": e1,
    "E2_keV": e2,
    "detection_threshold": "5",
    "instrument": "jemx",
    "osa_version": "OSA11.2",
    "product": "jemx_image",
    "product_type": "Real",
    "scw_list": [scw],
    "integral_data_rights": "all-private",#all-private or public
    "token": token
    }

    data_collection = disp.get_product(**par_dict)
    data_collection.mosaic_image_0_mosaic.write_fits_file(str(scw)+'.fits',overwrite=True)
# def search_hek():
#     # todo : define this function
#     return 0
def get_lc_jemx(table, fits_data, coord_list):

    from datetime import timedelta
    from datetime import datetime
    import math
    import numpy as np
    import pytz
    from astropy.wcs import WCS

    lc_times = []
    lc_fluxes = []
    lc_errors = []
    time_errors = []
    timezone = pytz.timezone('UTC')

    for scw,coord in zip(fits_data.keys(),coord_list):

        wcs = WCS(fits_data[str(scw)][2].header)
        row = table[table['SCW_ID'] == scw]
        t_start=str(row['START_DATE'][0].replace(' ','T'))
        t_end = str(row['END_DATE'][0].replace(' ','T'))
        delta_t = datetime.fromisoformat(t_end) - datetime.fromisoformat(t_start)
        x_start,y_start = wcs.wcs_world2pix(coord[0].ra.deg,coord[0].dec.deg,0)
        x_end,y_end = wcs.wcs_world2pix(coord[1].ra.deg,coord[1].dec.deg,0)
        flux_error = np.sqrt(fits_data[str(scw)][3].data[int(y_start),int(x_start)])
        travel_x, travel_y = np.linspace(x_start,x_end,fits_data[str(scw)][2].data.shape[0]), np.linspace(y_start,y_end,fits_data[str(scw)][2].data.shape[0])
        flux_values = fits_data[str(scw)][2].data[travel_y.astype(int), travel_x.astype(int)]
        flux_values = [x for x in flux_values if not math.isnan(x)]
        unique_flux_values, counts = np.unique(flux_values, return_counts=True)
        flux_counter = dict(zip(unique_flux_values, counts))
        flux_times = []
        time_error = []
        #define the time errors as the time interval where the flux value is present
        total_time = datetime.strptime(t_start,'%Y-%m-%dT%H:%M:%S').replace(tzinfo= timezone)
        print(t_start,t_end, delta_t.total_seconds())
        for flux in flux_counter.keys():
            #flux_times.append(total_time + timedelta(seconds=delta_t.total_seconds() * (flux_counter[flux]/len(flux_values)/2)))
            print(flux_counter[flux],len(flux_values))
            flux_times.append(total_time + delta_t * (flux_counter[flux]/len(flux_values)/2))
            print(total_time + delta_t * (flux_counter[flux]/len(flux_values)/2))
            total_time = total_time + timedelta(seconds=delta_t.total_seconds() * (flux_counter[flux]/len(flux_values)))
            time_error.append((delta_t.total_seconds() * (flux_counter[flux]/len(flux_values)))/86400/2)

        lc_fluxes.append(unique_flux_values)
        lc_errors.append(flux_error)
        lc_times.append(flux_times)
        time_errors.append(time_error)

    return lc_times, lc_fluxes, lc_errors, time_errors
def get_average_jemx()