import sys
import unittest
from unittest.mock import MagicMock, patch

sys.argv = ["plugin.video.midarr", "1", ""]

mock_xbmcgui = MagicMock()
mock_xbmcplugin = MagicMock()
mock_xbmcaddon = MagicMock()

sys.modules["xbmcgui"] = mock_xbmcgui
sys.modules["xbmcplugin"] = mock_xbmcplugin
sys.modules["xbmcaddon"] = mock_xbmcaddon

from addon import list_libraries, router, HANDLE

class TestKodiPlugin(unittest.TestCase):

    @patch("xbmcplugin.addDirectoryItem")
    @patch("xbmcplugin.addSortMethod")
    @patch("xbmcplugin.endOfDirectory")
    @patch("xbmcgui.ListItem")
    def test_list_libraries(self, mock_list_item, mock_end_of_directory, mock_add_sort_method, mock_add_directory_item):
        """Test that list_libraries correctly adds a directory item."""
        mock_item = MagicMock()
        mock_list_item.return_value = mock_item

        list_libraries()

        mock_list_item.assert_called_once()
        mock_add_directory_item.assert_called_with(HANDLE, 'plugin.video.midarr?action=movies', mock_item, isFolder=True)
        mock_add_sort_method.assert_called_once_with(HANDLE, sys.modules["xbmcplugin"].SORT_METHOD_LABEL_IGNORE_THE)
        mock_end_of_directory.assert_called_once_with(HANDLE)

    @patch("addon.list_libraries")
    def test_router_no_params(self, mock_list_libraries):
        """Test that router calls list_libraries when no params are given."""
        router("")
        mock_list_libraries.assert_called_once()

    def test_router_invalid_param(self):
        """Test that router raises an exception for invalid params."""
        with self.assertRaises(ValueError):
            router("action=invalid")

if __name__ == "__main__":
    unittest.main()
