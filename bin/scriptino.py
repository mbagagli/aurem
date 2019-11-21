#!/usr/bin/env python3

from aurem import REC
# from aurem import plotting
from obspy import read
from obspy import UTCDateTime


def miniproc(st):
    prs = st.copy()
    prs.detrend('demean')
    prs.detrend('simple')
    prs.taper(max_percentage=0.05, type='cosine')
    prs.filter("bandpass",
               freqmin=1,
               freqmax=30,
               corners=2,
               zerophase=True)
    return prs

# ==========
print("READ")
st = read()
# st.trim(UTCDateTime("2009-08-24T00:20:05"), UTCDateTime("2009-08-24T00:20:12"))
prs = miniproc(st)

print("INIT + CALC")
daje = REC(prs, channel="*Z")
daje.work()

print(daje.get_pick())

daje.plot()
