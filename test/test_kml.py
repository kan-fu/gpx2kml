import xml.etree.ElementTree as ET

from gpx2kml.gpx import GPX
from gpx2kml.kml import KML


def test_new_placemark_escapes_xml_characters(tmp_path):
    gpx_file = tmp_path / "escaped.gpx"
    gpx_file.write_text(
        """<?xml version='1.0' encoding='UTF-8'?>
<gpx xmlns='http://www.topografix.com/GPX/1/1'>
  <trk>
    <name>A &amp; B &lt;Run&gt;</name>
    <desc>Desc &amp; &lt;details&gt;</desc>
    <type>Walking</type>
    <trkseg>
      <trkpt lat='38.1' lon='-123.1' />
    </trkseg>
  </trk>
</gpx>
""",
        encoding="utf8",
    )

    placemark = KML.new_placemark(GPX(gpx_file))
    placemark_xml = ET.tostring(placemark, encoding="unicode")

    assert "A &amp; B &lt;Run&gt;" in placemark_xml
    assert "Desc &amp; &lt;details&gt;" in placemark_xml


def test_extract_latlon_returns_empty_without_trk(tmp_path):
    gpx_file = tmp_path / "no-track.gpx"
    gpx_file.write_text(
        """<?xml version='1.0' encoding='UTF-8'?>
<gpx xmlns='http://www.topografix.com/GPX/1/1'>
  <metadata>
    <name>No Track</name>
  </metadata>
</gpx>
""",
        encoding="utf8",
    )

    gpx = GPX(gpx_file)
    assert list(gpx.extract_latlon()) == []
