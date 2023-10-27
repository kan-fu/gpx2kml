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


def test_unarchived_add_meta(unarchived_gpx, tmp_path):
    unarchived_gpx.add_meta({"desc": "testing desc", "type": "testing type"})
    unarchived_gpx.export(tmp_path / "tmp.gpx")
    exported_gpx = GPX(tmp_path / "tmp.gpx")

    assert exported_gpx.get_desc() == "testing desc"
    assert exported_gpx.get_type() == "testing type"


def test_unarchived_extract_latlon(unarchived_gpx):
    assert list(unarchived_gpx.extract_latlon()) == [
        [
            ("38.303185000", "-123.064900000"),
            ("38.303160000", "-123.064896000"),
            ("38.303196000", "-123.065010000"),
            ("38.303290000", "-123.064980000"),
            ("38.303380000", "-123.064960000"),
            ("38.303307000", "-123.064880000"),
            ("38.303368000", "-123.064780000"),
        ],
        [
            ("38.305190000", "-123.057720000"),
            ("38.305134000", "-123.057670000"),
            ("38.305115000", "-123.057550000"),
            ("38.305042000", "-123.057480000"),
            ("38.304943000", "-123.057450000"),
            ("38.304870000", "-123.057380000"),
            ("38.304787000", "-123.057330000"),
            ("38.304690000", "-123.057335000"),
        ],
    ]


def test_archived_extract_latlon(archived_gpx):
    assert list(archived_gpx.extract_latlon()) == [
        [
            ("38.303185000", "-123.064900000"),
            ("38.303160000", "-123.064896000"),
            ("38.303196000", "-123.065010000"),
            ("38.303290000", "-123.064980000"),
            ("38.303380000", "-123.064960000"),
            ("38.303307000", "-123.064880000"),
            ("38.303368000", "-123.064780000"),
        ],
        [
            ("38.305190000", "-123.057720000"),
            ("38.305134000", "-123.057670000"),
            ("38.305115000", "-123.057550000"),
            ("38.305042000", "-123.057480000"),
            ("38.304943000", "-123.057450000"),
            ("38.304870000", "-123.057380000"),
            ("38.304787000", "-123.057330000"),
            ("38.304690000", "-123.057335000"),
        ],
    ]
