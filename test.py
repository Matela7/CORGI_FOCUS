import unittest
from unittest.mock import mock_open, patch, call
from main import block_sites, unblock_sites, hosts_path, sites_to_block, redirect_ip  # zaimportuj swoje funkcje i zmienne

class TestBlockUnblockSites(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="127.0.0.1 localhost\n")
    @patch("main.error_popup")
    def test_block_sites(self, mock_error_popup, mock_open):
        block_sites(hosts_path, sites_to_block, redirect_ip)
        mock_open.assert_called_once_with(hosts_path, 'r+')
        handle = mock_open()
        expected_calls = [call().write(f"{redirect_ip} {site}\n") for site in sites_to_block]
        handle.write.assert_has_calls(expected_calls, any_order=True)
        self.assertFalse(mock_error_popup.called, "Popup shouldn't be called")

    @patch("builtins.open", new_callable=mock_open, read_data="127.0.0.1 localhost\n127.0.0.1 facebook.com\n127.0.0.1 youtube.com\n")
    @patch("main.error_popup")
    def test_unblock_sites(self, mock_error_popup, mock_open):
        unblock_sites(hosts_path, sites_to_block, redirect_ip)
        mock_open.assert_called_once_with(hosts_path, 'r+')
        handle = mock_open()
        handle.write.assert_called_with("127.0.0.1 localhost\n")
        self.assertFalse(mock_error_popup.called, "Popup shouldn't be called")

if __name__ == "__main__":
    unittest.main()
