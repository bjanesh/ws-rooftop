import numpy as np
from astropy.time import Time as time
from astropy.io import ascii as io
from astropy.table import QTable as qt
import astropy.coordinates as co
import astropy.units as u
from datetime import datetime

loc = co.EarthLocation(lat='41.505493d',lon='-81.681290d') # 
# sets our location

now = time.now()

if now.value.hour > 17:
    tonight = time(datetime(int(now.value.year),int(now.value.month),int(now.value.day)+1,3,0,0),location = loc)
else:
    tonight = time(datetime(int(now.value.year),int(now.value.month),int(now.value.day),3,0,0),location = loc)
# gives current time, then the time at about midnight
# if before noon, it gives the "previous" night, so that late-night observing isn't interfered with
# astropy's time routines give UTC time, so this is 11 PM our time

sidnow = now.sidereal_time(kind='apparent',longitude='-81.681290d',model='IAU2000A')
sidereal = tonight.sidereal_time(kind='apparent',longitude='-81.681290d',model='IAU2000A')
# gives sidereal time from those

stars = io.read('brightstars.txt')
starnames = stars['name']
starra = stars['ra']
stardec = stars['dec']

for i in range(0,len(starnames)):
    globals()[starnames[i]] = co.SkyCoord(ra=starra[i]*u.hour,dec=stardec[i]*u.deg)
# this reads in from a list of stars, with Right Ascension in hours and Declination in degrees

merc = co.get_body('mercury',tonight)
ven = co.get_body('venus',tonight)
mars = co.get_body('mars',tonight)
jup = co.get_body('jupiter',tonight)
sat = co.get_body('saturn',tonight)
ura = co.get_body('uranus',tonight)
nep = co.get_body('neptune',tonight)
luna = co.get_body('moon',tonight)

planetlist = ['luna','merc','ven','mars','jup','sat','ura','nep']
planetnames = ['Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune']

for i in range(0,len(planetlist)):
    globals()[planetlist[i]+'co'] = co.SkyCoord(ra=globals()[planetlist[i]].ra,dec=globals()[planetlist[i]].dec)

# finds tonight's coordinates for each planet
# this uses astropy's internal ephemeris
# adding additional ephemera is described in the astropy documentation

starha = sidnow.value - starra
starha[starha < 0] = starha[starha < 0] + 24

planetha = np.zeros_like(starha[:len(planetlist)])
planetdec = np.zeros_like(planetha)
for i in range(0,len(planetlist)):
    planetha[i] = sidnow.value - globals()[planetlist[i]].ra.hour
    planetdec[i] = globals()[planetlist[i]+'co'].dec.value
planetha[planetha < 0] = planetha[planetha < 0] + 24

# gives the current Hour Angle for all relevant bodies, in 0-24 scale
# also adds the declination of the planets, for later output

timespacer = np.linspace(-6,9,901) * u.hour

sunalts = np.zeros(len(timespacer))
sunalts = co.get_body('sun',tonight + timespacer).transform_to(co.AltAz(obstime = tonight + timespacer, location = (loc))).alt
nightsky = (sunalts.value < -5)

trimtime = timespacer[nightsky]

# finds sunrise and sunset, trims the trimtime down to only include the night sky

staralt = np.zeros([len(starnames),len(trimtime)])
planetalt = np.zeros([len(planetlist),len(trimtime)])
gstars = np.zeros(len(starnames))
gplanets = np.zeros(len(planetlist))
starsrs = np.zeros([len(starnames),2])
planetsrs = np.zeros([len(planetlist),2])

for i in range(0,len(starnames)):
    staralt[i,:] = globals()[starnames[i]].transform_to(co.AltAz(obstime = tonight + trimtime,location = loc)).alt
    g = np.greater(staralt[i,:], 30)
    if sum(g) > 1:
        gstars[i] = 1
        starsrs[i,0] = np.where(np.greater(staralt[i,:], 30))[0][0]
        starsrs[i,1] = np.where(np.greater(staralt[i,:], 30))[0][-1]

for i in range(0,len(planetlist)):
    planetalt[i,:] = globals()[planetlist[i]].transform_to(co.AltAz(obstime = tonight + trimtime,location = loc)).alt
    g = np.greater(planetalt[i,:], 30)
    if sum(g) > 1:
        gplanets[i] = 1
        planetsrs[i,0] = np.where(np.greater(planetalt[i,:], 30))[0][0]
        planetsrs[i,1] = np.where(np.greater(planetalt[i,:], 30))[0][-1]

# finds which bodies will be above about 60 degrees from the zenith
# gives the first and last time they are in that position during that night
# this is called rise and set for simplicity

validplanets = gplanets > 0.5
validstars = gstars > 0.5

starrise = []
starset = []
planetrise = []
planetset = []

for i in range(0,len(starnames)):
    r = tonight + trimtime[int(starsrs[i,0])] - (4 * u.hour)
    s = tonight + trimtime[int(starsrs[i,1])] - (4 * u.hour)
    starrise.append('{:02d}:{:02d}'.format(r.value.hour, r.value.minute))
    starset.append('{:02d}:{:02d}'.format(s.value.hour, s.value.minute))

for i in range(0,len(planetnames)):
    r = tonight + trimtime[int(planetsrs[i,0])] - (4 * u.hour)
    s = tonight + trimtime[int(planetsrs[i,1])] - (4 * u.hour)
    planetrise.append('{:02d}:{:02d}'.format(r.value.hour, r.value.minute))
    planetset.append('{:02d}:{:02d}'.format(s.value.hour, s.value.minute))

# if a body will be visible, prints when it will rise and set

# round positions to a useful value
planetha = np.round(planetha, 2)
planetdec = np.round(planetdec, 1)

starha = np.round(starha, 2)
stardec = np.round(stardec, 1)

planetvals = np.array([planetnames,planetha,planetdec,planetrise,planetset])
starvals = np.array([starnames,starha,stardec,starrise,starset])

planetout = qt(planetvals[:,validplanets].T,names=['Object Name','Hour Angle','Declination','Rise Time','Set Time'])
starout = qt(starvals[:,validstars].T,names=['Object Name','Hour Angle','Declination','Rise Time','Set Time'])

io.write(planetout,'nightplanets.csv',format='csv',overwrite=True)
io.write(starout,'nightstars.csv',format='csv',overwrite=True)
