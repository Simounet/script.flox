import base64
import urllib.request
import urllib.parse
import json
import xbmc
import xbmcgui
from urllib.error import HTTPError, URLError
from typing import TypedDict, Literal

class ExternalId(TypedDict):
    imdbId: str
    tmdbId: int

class ProgressPayload(TypedDict):
    mediaType: Literal["movie", "tv"]
    id: ExternalId
    seasonNumber: int
    episodeNumber: int
    action: Literal["playing", "paused"]
    progress: float
    duration: float

class MarkAsSeenPayload(TypedDict):
    mediaType: Literal["movie", "tv"]
    id: ExternalId
    seasonNumber: int
    episodeNumber: int
    duration: float

class Flox:
    def __init__(self, url: str, username: str, password: str) -> None:
        self.url = url
        self.username = username
        self.password = password

    def markAsSeen(self, payload: MarkAsSeenPayload):
        url = urllib.parse.urljoin(
            self.url, '/api/episode/seen')

        try:
            putJson(url, self.username, self.password, payload)
            notify('Episode marked as seen', 'Episode marked as seen')
        except HTTPError as error:
            if error.status == 401:
                notify('Unauthorized user', 'Unauthorized user')
            elif error.status == 404:
                notify('unknown TV Show', 'Flox doesn\'t know this TV Show yet. Add it!')
            else:
                notify('unknown error', 'Unknown error')

def putJson(url: str, username: str, password: str, data: dict):
    postdata = json.dumps(data).encode()

    headers = {"Content-Type": "application/json; charset=UTF-8"}

    httprequest = urllib.request.Request(
        url,
        data=postdata,
        headers=headers,
        method="PUT")

    credentials = f"{username}:{password}".encode('utf-8')
    base64_credentials = base64.b64encode(credentials).decode('utf-8')
    httprequest.add_header('Authorization', f'Basic {base64_credentials}')

    response = urllib.request.urlopen(httprequest)

def notify(log: str, text: str):
    xbmc.log(
        f"Flox: {log}", xbmc.LOGINFO)
    dialog = xbmcgui.Dialog()
    dialog.notification('Flox', text, xbmcgui.NOTIFICATION_INFO, 10000)
