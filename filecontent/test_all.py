# Check that the package version can be obtained and evalutes to 'True'
from filecontent import __version__


def test_something():
    assert __version__
