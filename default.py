import xbmc
from resources.lib.monitor import Monitor
from resources.lib.scrobbler import Scrobbler

xbmc.log("Flox: starting", xbmc.LOGDEBUG)

scrobbler = Scrobbler()
monitor = Monitor(scrobbler)

while not monitor.abortRequested():
    if monitor.waitForAbort(30):
        break

    else:
        if xbmc.Player().isPlaying():
            scrobbler.scrobble(xbmc.Player())


xbmc.log("Flox: exiting", xbmc.LOGDEBUG)
