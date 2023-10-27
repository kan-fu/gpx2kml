import filecmp
from textwrap import dedent

from gpx2kml.util import (
    _extract_from_csv,
    gpx_archive,
    gpx_archive_with_zipfile,
    kml_combine,
    kml_generate,
)

kml_file = "test/kml/2023-08.kml"


def test_gpx_archive_with_zip(tmp_path):
    gpx_archive_with_zipfile(
        gpx_zip_file="test/01-runkeeper-data-export.zip", archive_folder=tmp_path
    )
    assert filecmp.dircmp(tmp_path, "test/archive")


def test_gpx_archive(tmp_path):
    gpx_archive(gpx_folder="test/gpx", archive_folder=tmp_path)
    assert filecmp.dircmp(tmp_path, "test/archive")


def test_kml_generate(tmp_path):
    kml_generate(archive_folder=r"test/archive", kml_folder=tmp_path)
    assert filecmp.dircmp(tmp_path, "test/kml")


def test_kml_combine(tmp_path):
    kml_combine(kml_combine_name="test", from_folder=r"test/kml", to_folder=tmp_path)
    assert filecmp.cmp(tmp_path / "test.kml", "test/kml_combine/test.kml")


def test_extract_from_csv():
    assert _extract_from_csv("test/gpx/cardioActivities.csv") == {
        "2023-08-03-121238.gpx": {
            "type": "Walking",
            "desc": dedent(
                """\
                Type:       Walking
                Notes:      
                Distance:   0.68 km
                Duration:   41:54
                Pace:       62:04 min/km
                Speed:      0.97 km/h"""  # noqa: W291
            ),
        }
    }
