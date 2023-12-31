#! /usr/bin/env python
"""Determine Andromeda location in ra/dec degrees"""

from math import cos, pi
from random import uniform

# from wikipedia
RA_STR = '00:42:44.4'
DEC_STR = '41:16:08'
NSRC = 1_000_000
RADIUS = 1

def make_positions():
    
    # convert to decimal degrees

    d, m, s = DEC_STR.split(':')
    dec = int(d)+int(m)/60+float(s)/3600

    h, m, s = RA_STR.split(':')
    ra = 15*(int(h)+int(m)/60+float(s)/3600)
    ra = ra/cos(dec*pi/180)

    # make 1000 stars within 1 degree of Andromeda

    ras = []
    decs = []
    for i in range(NSRC):
        ras.append(ra + uniform(-1,1))
        decs.append(dec + uniform(-1,1))

    # apply our filter
    ras, decs = crop_to_circle(ras,decs, ra, dec, RADIUS)

    return ras, decs

def crop_to_circle(ras, decs, ref_ra, ref_dec, radius):
    """
    Crop an input list of positions so that they lie within radius of
    a reference position

    Parameters
    ----------
    ras,decs : list(float)
        The ra and dec in degrees of the data points
    ref_ra, ref_dec: float
        The reference location
    radius: float
        The radius in degrees
    Returns
    -------
    ras, decs : list
        A list of ra and dec coordinates that pass our filter.
    """
    ra_out = []
    dec_out = []
    for i in range(len(ras)):
        if (ras[i]-ref_ra)**2 + (decs[i]-ref_dec)**2 < radius**2:
            ra_out.append(ras[i])
            dec_out.append(ras[i])
    return ra_out, dec_out

# now write these to a csv file for use by my other program
def save_positions(ras, decs):
    with open('catalog.csv', 'w', encoding='utf-8') as f:
        print("id,RA,DEC", file=f)
        for i in range(len(ras)):
            print(f"{i:07d}, {ras[i]:12f}, {decs[i]:12f}", file=f)

def main():
    ras, decs = make_positions()
    save_positions(ras, decs)

if __name__ == "__main__":
    main()
