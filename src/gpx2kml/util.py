import csv
import itertools as it
import sys
import tempfile
from pathlib import Path
from textwrap import dedent
from typing import Iterator
from zipfile import ZipFile

from gpx2kml.gpx import GPX
from gpx2kml.kml import KML

_REQUIRED_CSV_COLUMNS = (
    "Type",
    "Distance (km)",
    "Duration",
    "Average Pace",
    "Average Speed (km/h)",
    "Notes",
    "GPX File",
)


def _extract_from_csv(csv_file: Path | str) -> dict[str, dict[str, str]]:
    meta_info: dict[str, dict[str, str]] = {}

    with open(csv_file, mode="r", encoding="utf8") as f:
        csv_reader = csv.DictReader(f, delimiter=",")
        if csv_reader.fieldnames is None:
            raise ValueError("CSV file is missing header row")

        missing_columns = sorted(
            set(_REQUIRED_CSV_COLUMNS) - set(csv_reader.fieldnames)
        )
        if missing_columns:
            raise ValueError(
                f"Missing required CSV columns: {', '.join(missing_columns)}"
            )

        for row_num, row in enumerate(csv_reader, start=2):
            gpx_filename = (row.get("GPX File") or "").strip()
            if not gpx_filename:
                raise ValueError(f"Missing 'GPX File' in row {row_num}")

            activity_type = (row.get("Type") or "").strip()
            if not activity_type:
                raise ValueError(f"Missing 'Type' in row {row_num}")

            meta_info[gpx_filename] = {}
            meta_info[gpx_filename]["type"] = activity_type
            meta_info[gpx_filename]["desc"] = dedent(f"""\
                Type:       {activity_type}
                Notes:      {row.get('Notes', '')}
                Distance:   {row.get('Distance (km)', '')} km
                Duration:   {row.get('Duration', '')}
                Pace:       {row.get('Average Pace', '')} min/km
                Speed:      {row.get('Average Speed (km/h)', '')} km/h""")
    return meta_info


def gpx_archive_with_zipfile(gpx_zip_file: str | Path, archive_folder=r"./archive"):
    with tempfile.TemporaryDirectory() as tempdir:
        with ZipFile(gpx_zip_file) as myzip:
            myzip.extractall(tempdir)
        gpx_archive(tempdir, archive_folder)


def gpx_archive(gpx_folder: Path | str = r"./gpx", archive_folder=r"./archive"):
    Path(archive_folder).mkdir(exist_ok=True)
    meta_info = _extract_from_csv(Path(gpx_folder) / "cardioActivities.csv")

    for gpx_path in Path(gpx_folder).glob("*.gpx"):
        print(f"Archiving {gpx_path}...")
        gpx = GPX(gpx_path)
        gpx.add_meta(meta_info[gpx_path.name])
        gpx.export(Path(archive_folder) / gpx_path.name)


def kml_generate(
    archive_folder=r"./archive", kml_folder=r"./kml", filter_type: str | None = None
):
    Path(kml_folder).mkdir(exist_ok=True)

    year_month: str
    gpx_sublist: Iterator[Path]
    # GPX filename is like 2015-09-12-183914.gpx, 0 to 7 is 2015-09
    for year_month, gpx_sublist in it.groupby(
        sorted(Path(archive_folder).glob("*.gpx")), key=lambda path: path.name[:7]
    ):
        print(f"Generating {year_month}.kml")
        kml = KML(Path(kml_folder) / f"{year_month}.kml", mode="new")
        kml.add_document()
        styles = [
            ("Cycling", "ff0000ff", 3),
            ("Walking", "ff00ff00", 2),
            ("Running", "ff0000ff", 2),
            ("Other", "ffff0000", 3),
        ]
        for style_id, color, width in styles:
            kml.add_style_to_document(style_id, color, width)
        for gpx_file in gpx_sublist:
            gpx = GPX(gpx_file)
            if filter_type and gpx.get_type() != filter_type:
                continue
            kml.add_gpx_to_document(gpx)
        kml.export()


def kml_combine(kml_combine_name: str, from_folder=r"./kml", to_folder="."):
    Path(to_folder).mkdir(exist_ok=True)

    kml = KML(Path(to_folder) / f"{kml_combine_name}.kml", mode="new")
    kml.add_folder()
    kml_files = sorted(
        (Path(from_folder) / kml_combine_name).glob("*.kml"), key=lambda path: path.name
    )
    for year, kml_sublist in it.groupby(
        kml_files,
        key=lambda path: path.name[:4],
    ):
        print(f"Combing year {year}")

        kml.add_sub_folder(year, kml_sublist)
    kml.export()


def gpx_archive_cmd():
    args = sys.argv[1:]
    if len(args) == 0:  # By default, it will process all the zip files
        for gpx_zip_file in Path(".").glob("01-runkeeper-data-export*.zip"):
            print(f"*** Processing {gpx_zip_file} ***")
            gpx_archive_with_zipfile(gpx_zip_file)
    elif len(args) == 1:
        filename = args[0]
        if not Path(filename).exists():
            raise FileNotFoundError(f"The filename '{filename}' should exist!")
        print(f"*** Processing {filename} ***")
        gpx_archive_with_zipfile(filename)
    else:
        print("gpx-archive only supports zero or one argument!")


def kml_generate_cmd():
    args = sys.argv[1:]
    if len(args) == 0:
        kml_generate()
    elif len(args) == 1:
        filter_type = args[0]
        kml_generate(filter_type=filter_type)
    else:
        print("kml-gen only supports zero or one argument!")


def kml_combine_cmd():
    args = sys.argv[1:]
    if len(args) == 0:
        print("Please input the name of the combined file!")
    elif len(args) == 1:
        kml_combine(args[0])
    else:
        print("kml-combine only supports one argument!")
