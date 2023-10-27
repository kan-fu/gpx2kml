from gpx2kml.util import gpx_archive_with_zipfile, kml_combine, kml_generate

gpx_archive_with_zipfile("01-runkeeper-data-export-26737881-2023-09-07-071211.zip")
kml_generate()
kml_combine("US_Roadtrip")
