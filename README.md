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

`$ conda create --name threeml -c conda-forge -c xpsecmodels python=3.9 xpsec-modelsonly numpy scipy matplotlib`
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
4. https://rhodesmill.org/skyfield/planets.html Skyfield: to compute planets positions, transform coordinate systems, manipulate dates etc...
5. https://ssd.jpl.nasa.gov/horizons/app.html#/ great to find ephemerides. Don't know why the results are slightly different than skyfield. Maybe something to do with date format ?
6. https://www.imcce.fr/content/medias/recherche/equipes/asd/calceph/html/c/calceph.naifid.html -> NAIF ID numbers
7. https://rhodesmill.org/skyfield/positions.html#icrs -> Positions in skyfield

What's Simbad -> looks like it's only for outside of the solar system objects so we don't care.

### Next steps are:

1. Compute positions of Venus when is was maximally elongated in a certain timerange
2. Select a science window list for these positions with a certain radius: https://oda-api.readthedocs.io/en/latest/user_guide/ScienceWindowList.html
3. "Plot"

Find coord. venus, timerange(where did integral observe venus), scw

## Week 4-5-6
-
## Week 7

What was done:

1. Finding some interesting processes: fluorescence essentially.
    1. X-Ray processes in the limits of instruments: fluorescence of heavy metals such as Pb(88kev) or argon(+3kev), calcium K-alpha(3.69 kev), iron, nickel, copper, zinc etc... Every metal essentially. But will be very weak.
    2. Gamma-ray: 
        1. Bremsstrahlung emission: When high-energy electrons in the solar flare interact with atmospheric particles in Venus' upper atmosphere, they can be slowed down and lose energy, emitting gamma rays in the process. This type of emission is called bremsstrahlung, or "braking radiation".
        2. Nuclear de-excitation: Solar flares can also produce high-energy particles such as protons and alpha particles, which can collide with atmospheric atoms and cause them to become excited or ionized. When these atoms return to their ground state, they can emit gamma rays through a process called nuclear de-excitation.
        3. Pion production: In some cases, high-energy protons from a solar flare can interact with atmospheric nuclei and produce pions, which are unstable particles that quickly decay into gamma rays.
        4. Neutron capture: If solar flare particles interact with atmospheric nuclei and produce neutrons, these neutrons can be captured by other nuclei in the atmosphere, producing gamma rays in the process.
2. Sunpy: understanding frames, locating events, going through hek, helioviewer databases.
3. Functions: getting scw, direction of event, venus times and positions.

### List of all useful links(continuously updated)

#### Astropy

https://docs.astropy.org/en/stable/table/index.html -> tables

https://docs.astropy.org/en/stable/table/access_table.html -> accessing a table

https://www.astrobetter.com/blog/2013/07/29/python-tip-storing-data/#:~:text=As%20a%20general%20rule%20of,are%20easy%20to%20work%20with -> handling files

#### Sunpy

https://docs.sunpy.org/en/stable/guide/acquiring_data/fido.html -> Querying databases using FIDO

https://sdac.virtualsolar.org/cgi/show_details?keyword=INSTRUMENT -> all instruments vso supports

https://docs.sunpy.org/en/stable/guide/acquiring_data/helioviewer.html Getting image of the sun and movies at a certain moment querying the Helioviewer project.

https://docs.sunpy.org/en/stable/generated/gallery/units_and_coordinates/planet_locations -> locating planets in STO or other

https://docs.sunpy.org/en/stable/generated/api/sunpy.coordinates.frames.html -> coordinate frames

https://docs.sunpy.org/en/stable/generated/api/sunpy.coordinates.frames.Helioprojective.html#sunpy.coordinates.frames.Helioprojective -> Helioprojective HPO

https://www.lmsal.com/hek/VOEvent_Spec.html -> HEK event types definition /!\ super important

https://www.lmsal.com/heksearch/ -> frontend HEK search, useful with images and everything


#### Space weather

https://www.spaceweatherlive.com/en/archive/2022/08/30/xray.html -> good generalist website

https://www.swpc.noaa.gov/products/solar-cycle-progression -> solar cycle progression

https://data.nas.nasa.gov/helio/portals/solarflares/datasources.html -> Solar flares datasources

https://student.helioviewer.org/ -> student helioviewer. Find events and make movies/screenshots.

#### Integral

https://heasarc.gsfc.nasa.gov/W3Browse/integral/intscw.html -> science windows

https://oda-api.readthedocs.io/en/latest/user_guide -> ODA-API

https://www.cosmos.esa.int/web/integral/instruments-ibis -> IBIS specs

https://www.cosmos.esa.int/web/integral/instruments-jemx -> JEM-X specs

#### Venus

##### Literature

https://www.britannica.com/place/Venus-planet/The-atmosphere -> Atmosphere

10.1007/s11214-017-0362-8 -> Solar wind interaction with Venus's atmosphere. Very thorough.

##### Events

https://www.esa.int/Enabling_Support/Operations/Coronal_mass_ejection_hits_Solar_Orbiter_before_Venus_flyby -> 30.08.22 event

https://www.space.com/venus-battered-sun-eruption-space-weather -> 05.09.22 event

https://www.space.com/14834-solar-storm-blinds-venus-express-spacecraft.html -> 06.03.2012 event


#### Miscellaneous

https://www.vercalendario.info/en/how/convert-ra-degrees-hours.html -> RA, degrees <-> hour

https://physics.nist.gov/PhysRefData/XrayTrans/Html/search.html -> X-Ray transition energy database to find fluorescence

## Week 8

TODO: 

- Retrieve fits of each scw
- Find venus in each one of them -> careful with the duration of the scw. It won't be a single point but a trace.
- Plot the lightcurve of venus for this scw. Careful to check the dates.

## Week 9

- Retrieved every scw from 18.04, 20.04, 22.04, 24.04
- Checked suitable data: if target is in the field etc...

## Week 10 - 12

- Started analysis of data, check report for details.

## Week 13

-

## Week 14

-

## End of Semester

- Finished analysis
- Added sunspot locator
- Writing of report