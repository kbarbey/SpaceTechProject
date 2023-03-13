# Project progress

## Week 1 :  
Installed oda-api package. Encountered some troubles with pyerfa as it needed MS Visual C++ in a weird way. Managed to do it with some googling help.

Created a virtual environment with all useful packages: spacetech_env

Began the tutorial up to the end of the "Quickstart".
## Week 2 :    
Continued tutorial:

1. In Quickstart : encountered some trouble with the LC plot. Error: "no instrument". Changed the format but looks useless to define lc variable now...

2. Couldn't plot with POLAR instrument: timeout everytime. Tried to constrain search by adding DEC and RA but it didn't change anything. Will have to look through that...

3. SPIACS LC works fine. What's the green line for ? Average probably.
4. Couldn't get ISGRI's spectra: output exceeds size limit.
5. Idem for jemx.
6. threeML : ran into some troubles with the installation. Conda command didn't work. Probably because in spacetech_env, I'm using python 3.11. Tried to install threeML in spacetech_env, didn't work. Created a new virtual environment instead as advised in installation instrutions. Couldn't install astromodels with any of the options propose.
Can't install a load of packages with 3.11 version of python...
Tried to install following instructions but impossible to install XSPEC on windows...

Tried the option without installing HEASOFT but failed :

$ `conda create --name threeml -c conda-forge -c xpsecmodels python=3.9 xpsec-modelsonly numpy scipy matplotlib`
Collecting package metadata (current_repodata.json): ...working... failed

UnavailableInvalidChannel: HTTP 404 NOT FOUND for channel xpsecmodels <https://conda.anaconda.org/xpsecmodels>

The channel is not accessible or is invalid.

You will need to adjust your conda configuration to proceed.
Use `conda config --show channels` to view your configuration's current state,
and use `conda config --show-sources` to view config file locations.

Tried the token identification: didn't work->timeout

### TO DO with supervisor :
Timeout on light curves.

Install 3ML, astromodels, xspec.

Check that token thing

## Week 3:

Coordinate system: ICRS with Solar system Barycenter as origin.
Time format: ISDC Julian Date(IJD) based on TT. But in notebook Carlo says ISOT format... Looks like utc_iso function should do the trick or just use utc.

Useful links: 
1. https://heasarc.gsfc.nasa.gov/W3Browse/integral/intscw.html
2. https://docs.astropy.org/en/stable/time/index.html
3. https://heasarc.gsfc.nasa.gov/xamin/index.jsp
4. https://rhodesmill.org/skyfield/planets.html
5. https://ssd.jpl.nasa.gov/horizons/app.html#/ great to find ephemerides. Don't know why the results are slightly different than skyfield. Maybe something to do with date format ?
6. https://www.imcce.fr/content/medias/recherche/equipes/asd/calceph/html/c/calceph.naifid.html -> NAIF ID numbers

What's Simbad -> looks like it's only for outside of the solar system objects so we don't care.

### Next steps are:

1. Compute positions of Venus when is was maximally elongated in a certain timerange
2. Select a science window list for these positions with a certain radius: https://oda-api.readthedocs.io/en/latest/user_guide/ScienceWindowList.html
3. "Plot"

Find coord. venus, timerange(where did integral observe venus), scw