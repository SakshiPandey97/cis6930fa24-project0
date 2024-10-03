from unittest.mock import MagicMock, patch
from urllib.error import HTTPError
import main
import pytest

@patch('project0.urllib.request.urlopen')
def test_fi(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = b"Example normanpd"
    mock_urlopen.return_value = mock_response

    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-05_daily_incident_summary.pdf"
    result = main.project0.fetchincidents(url)
    assert result == b"Example normanpd"
    print("Data Test Passed!")
    
@patch('project0.urllib.request.urlopen')
def test_fi_404(mock_urlopen):
    mock_urlopen.side_effect = HTTPError(
        url="https://www.normanok.gov/fail.pdf", code=404, msg="Not Found", hdrs=None, fp=None
    )
    url = "https://www.normanok.gov/fail.pdf" 
    result = main.project0.fetchincidents(url)
    assert result is None
    print("404 Error Test Passed!")
