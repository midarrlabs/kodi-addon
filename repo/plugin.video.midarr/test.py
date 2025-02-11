import sys
import unittest
from unittest.mock import MagicMock, patch, call

sys.argv = ["plugin.video.midarr", "1", ""]

mock_xbmcgui = MagicMock()
mock_xbmcplugin = MagicMock()
mock_xbmcaddon = MagicMock()

sys.modules["xbmcgui"] = mock_xbmcgui
sys.modules["xbmcplugin"] = mock_xbmcplugin
sys.modules["xbmcaddon"] = mock_xbmcaddon

from addon import home, router, HANDLE

class TestKodiPlugin(unittest.TestCase):

    @patch("xbmcplugin.addDirectoryItem")
    @patch("xbmcplugin.addSortMethod")
    @patch("xbmcplugin.endOfDirectory")
    @patch("xbmcgui.ListItem")
    def test_home(self, mock_list_item, mock_end_of_directory, mock_add_sort_method, mock_add_directory_item):

        mock_item_search = MagicMock()
        mock_item_movies = MagicMock()
    
        mock_list_item.side_effect = [mock_item_search, mock_item_movies]

        home()

        mock_add_directory_item.assert_has_calls([
            call(handle=HANDLE, url='plugin.video.midarr?action=search', listitem=mock_item_search, isFolder=True),
            call(handle=HANDLE, url='plugin.video.midarr?action=movies', listitem=mock_item_movies, isFolder=True)
        ], any_order=False)

        mock_end_of_directory.assert_called_once_with(HANDLE)

    @patch("addon.home")
    def test_router_no_params(self, mock_home):
        """Test that router calls home when no params are given."""
        router("")
        mock_home.assert_called_once()

    def test_router_invalid_param(self):
        """Test that router raises an exception for invalid params."""
        with self.assertRaises(ValueError):
            router("action=invalid")

if __name__ == "__main__":
    unittest.main()
