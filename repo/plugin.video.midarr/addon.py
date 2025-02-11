import sys
import xbmcgui
import xbmcplugin
from urllib.parse import urlencode, parse_qsl

URL, HANDLE = sys.argv[0], int(sys.argv[1])

def get_url(**kwargs):
    return f"{URL}?{urlencode(kwargs)}"

def home():
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=get_url(action="search"), listitem=xbmcgui.ListItem(label="Search"), isFolder=True)
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=get_url(action="movies"), listitem=xbmcgui.ListItem(label="Movies"), isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)

def router(param_string):
    params = dict(parse_qsl(param_string))
    if not params:
        home()
    else:
        raise ValueError(f"Invalid param_string: {param_string}!")

if __name__ == "__main__":
    router(sys.argv[2][1:])