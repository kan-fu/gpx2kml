import filecmp
from textwrap import dedent

from gpx2kml.util import (
    _extract_from_csv,
    gpx2kml_cmd,
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
    dcmp = filecmp.dircmp(tmp_path, "test/archive")
    assert not dcmp.diff_files and not dcmp.left_only and not dcmp.right_only


def test_gpx_archive(tmp_path):
    gpx_archive(gpx_folder="test/gpx", archive_folder=tmp_path)
    dcmp = filecmp.dircmp(tmp_path, "test/archive")
    assert not dcmp.diff_files and not dcmp.left_only and not dcmp.right_only


def test_kml_generate(tmp_path):
    kml_generate(archive_folder=r"test/archive", kml_folder=tmp_path)
    dcmp = filecmp.dircmp(tmp_path, "test/kml")
    assert not dcmp.diff_files and not dcmp.left_only  # dcmp.right_only is not needed


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
                Speed:      0.97 km/h"""
            ),  # noqa: W291
        }
    }


def test_gpx2kml_cmd_runs_kml_generate_with_filter(monkeypatch):
    calls: list[str] = []
    inputs = iter(["2", "Cycling", "q"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(
        "gpx2kml.util.kml_generate", lambda filter_type=None: calls.append(filter_type)
    )

    gpx2kml_cmd()

    assert calls == ["Cycling"]


def test_gpx2kml_cmd_rejects_missing_zip_file(monkeypatch, capsys):
    inputs = iter(["1", "not_found.zip", "q"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    gpx2kml_cmd()

    output = capsys.readouterr().out
    assert "should exist" in output


def test_gpx2kml_cmd_requires_kml_combine_name(monkeypatch, capsys):
    calls: list[str] = []
    inputs = iter(["3", "", "3", "demo", "q"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("gpx2kml.util.kml_combine", lambda name: calls.append(name))

    gpx2kml_cmd()

    output = capsys.readouterr().out
    assert "Please input the name of the combined file!" in output
    assert calls == ["demo"]
