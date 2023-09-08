from textwrap import dedent

import pytest

from gpx2kml.gpx import GPX

unarchived = "test/gpx/2023-08-03-121238.gpx"
archived = "test/archive/2023-08-03-121238.gpx"


@pytest.fixture
def unarchived_gpx():
    return GPX(unarchived)


@pytest.fixture
def archived_gpx():
    return GPX(archived)


def test_unarchived_get_info(unarchived_gpx):
    assert unarchived_gpx.get_type() == ""
    assert unarchived_gpx.get_name() == "Walking 8/3/23 12:12 pm"
    assert unarchived_gpx.get_desc() == ""


def test_archived_get_info(archived_gpx):
    assert archived_gpx.get_type() == "Walking"
    assert archived_gpx.get_name() == "Walking 8/3/23 12:12 pm"

    assert archived_gpx.get_desc() == dedent(
        """\
        Type:       Walking
        Notes:      
        Distance:   0.68 km
        Duration:   41:54
        Pace:       62:04 min/km
        Speed:      0.97 km/h"""  # noqa: W291
    )
