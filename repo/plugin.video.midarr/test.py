import sys
import unittest
import json
import urllib.request
from unittest.mock import MagicMock, patch, call

sys.argv = ["plugin.video.midarr", "1", ""]

mock_xbmcgui = MagicMock()
mock_xbmcplugin = MagicMock()
mock_xbmcaddon = MagicMock()

sys.modules["xbmcgui"] = mock_xbmcgui
sys.modules["xbmcplugin"] = mock_xbmcplugin
sys.modules["xbmcaddon"] = mock_xbmcaddon

from addon import home, router, get_url_images, get_videos, show_media, HANDLE, BASEURL, TOKEN

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
    
    def test_get_url_images(self):
        url = "http://image.com/sample.jpg"
        expected = f"{BASEURL}/images?url={url}&token={TOKEN}"
        result = get_url_images(url)
        self.assertEqual(result, expected)
    
    @patch("addon.BASEURL", "http://example.com")
    @patch("addon.TOKEN", "test_token")
    @patch("urllib.request.urlopen")
    def test_get_videos(self, mock_urlopen):

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"items": [{"title": "Movie 1", "overview": "A great movie", "year": 2024, "poster": "poster1.jpg", "background": "bg1.jpg"}]}).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        videos = get_videos()
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos[0].get("title"), "Movie 1")
        self.assertEqual(videos[0].get("year"), 2024)
    
    @patch("addon.get_videos")
    @patch("xbmcplugin.addDirectoryItem")
    @patch("xbmcplugin.endOfDirectory")
    @patch("xbmcgui.ListItem")
    def test_show_media(self, mock_list_item, mock_end_of_directory, mock_add_directory_item, mock_get_videos):
        mock_get_videos.return_value = [{
            "title": "Movie 1",
            "overview": "A great movie",
            "year": 2024,
            "poster": "poster1.jpg",
            "background": "bg1.jpg"
        }]
        mock_item = MagicMock()
        mock_list_item.return_value = mock_item

        show_media()

        mock_list_item.assert_called_with(label="Movie 1")
        mock_add_directory_item.assert_called_once()
        mock_end_of_directory.assert_called_once_with(HANDLE)
if __name__ == "__main__":
    unittest.main()
