from pylab import *
from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
import time
import pandas as pd


def progbar(i,N,size,starttime):
    fraction = float(i+1)/float(N)
    current = int(fraction*size)
    remain = size - current
    bar = current*'█' + remain*'░'
    percent = fraction*100.0
    elapsed = time.time() - starttime
    unit = 'sec'
    if elapsed > 59.99:
        elapsed = elapsed / 60.0
        unit = 'min'
    sys.stdout.write('\rProgress: |%s| %s%% Complete   Elapsed time: %s %s  ' % (bar, round(percent, 1),round(elapsed, 1),unit))
    sys.stdout.flush()

def getmag(targetname,savefile):

    # target name (obviously)
    target = targetname  # must be resolvable by Simbad

    # Use astropy Skycoord to get RA and Dec of object in degrees
    coords = SkyCoord.from_name(target)
    RA = coords.ra.deg
    Dec = coords.dec.deg

    # Query Simbad for magnitudes
    SimbadMag = Simbad()
    SimbadMag.remove_votable_fields('coordinates')
    for i in ['B', 'V', 'R', 'I', 'J', 'K']:
        SimbadMag.add_votable_fields('flux({0})'.format(i))
        magtable = SimbadMag.query_object(target)

    if magtable['FLUX_B'][0] == True:
        B = magtable['FLUX_B'][0]
    else: B = 16.6
    if magtable['FLUX_V'][0] == True:
        V = magtable['FLUX_V'][0]
    else: V = 15.6

    #If B and V magnitudes are known but aren't on Simbad, uncomment the next two lines and enter them here
    # B = 16.6
    # V = 15.6

    # Calculate the Kepler magnitude because of course Kepler has its own magnitude to calculate
    g = 0.54 * B + 0.46 * V - 0.07
    r = -0.44 * B + 1.44 * V + 0.12

    if (g - r) <= 0.8:
        kepmag = 0.2 * g + 0.8 * r

    if (g - r) > 0.8:
        kepmag = 0.1 * g + 0.9 * r

    #print comma-separated values to console to copy and paste into .csv file for K2Fov
    print('Target: '+target)
    print(str(RA)+' '+str(Dec)+' '+str(kepmag))
    print(' ')

    fileid = open(savefile, 'a+')
    fileid.write('%0.5f, %0.5f, %0.5f\n' % (RA, Dec, kepmag))
    fileid.close()

    #return RA, Dec, kepmag


readfile = 'Douglas_YSO_Presape_EPICS.csv'
savefile = 'Douglas_Presape.csv'

data = pd.read_csv(readfile)

targets = []
epics = []
for targ in data['EPIC']:
    targets.append('EPIC ' + str(targ))
    epics.append(str(targ))

[getmag(x,savefile) for x in targets]
