import sys
import xbmcgui
import xbmcplugin
from urllib.parse import urlencode, parse_qsl

URL, HANDLE = sys.argv[0], int(sys.argv[1])

def get_url(**kwargs):
    return f"{URL}?{urlencode(kwargs)}"

def list_libraries():
    list_item = xbmcgui.ListItem("Movies")

    xbmcplugin.addDirectoryItem(HANDLE, get_url(action="movies"), list_item, isFolder=True)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(HANDLE)

def router(param_string):
    params = dict(parse_qsl(param_string))
    if not params:
        list_libraries()
    else:
        raise ValueError(f"Invalid param_string: {param_string}!")

if __name__ == "__main__":
    router(sys.argv[2][1:])