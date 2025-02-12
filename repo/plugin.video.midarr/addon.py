import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import json
import urllib.request
from urllib.parse import urlencode, parse_qsl

URL = sys.argv[0]
HANDLE = int(sys.argv[1])
SETTINGS = xbmcaddon.Addon().getSettings()

BASEURL = f"{SETTINGS.getString('baseurl')}/api"
TOKEN = SETTINGS.getString('apitoken')

def get_url(**kwargs):
    return f"{URL}?{urlencode(kwargs)}"

def get_url_images(url):
    return f"{BASEURL}/images?url={url}&token={TOKEN}"

def get_videos():
    request = urllib.request.Request(f"{BASEURL}/movies?token={TOKEN}")

    with urllib.request.urlopen(request) as response:
        data = response.read()
        response_data = json.loads(data.decode("utf-8"))
        videos = response_data.get("items", [])

        return videos

def show_media():

    videos = get_videos()

    for video in videos:
        list_item = xbmcgui.ListItem(label=video.get("title", "Title"))

        list_item.setInfo("video", {
            "plot": video.get("overview", "Plot"),
            "year": video.get("year", 1900),
        })

        list_item.setArt({
            "thumb": get_url_images(video.get('poster')),
            "poster": get_url_images(video.get('poster')),
            "fanart": get_url_images(video.get('background')),
        })
        
        xbmcplugin.addDirectoryItem(handle=HANDLE, url=get_url(action=""), listitem=list_item, isFolder=False)

    xbmcplugin.endOfDirectory(HANDLE)

def home():
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=get_url(action="search"), listitem=xbmcgui.ListItem(label="Search"), isFolder=True)
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=get_url(action="movies"), listitem=xbmcgui.ListItem(label="Movies"), isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)

def router(param_string):
    params = dict(parse_qsl(param_string))
    if not params:
        home()
    elif params['action'] == 'movies':
        show_media()
    else:
        raise ValueError(f"Invalid param_string: {param_string}!")

if __name__ == "__main__":
    router(sys.argv[2][1:])